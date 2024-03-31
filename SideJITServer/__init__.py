import atexit
import click
import socket
import logging
import inquirer3
import multiprocessing
from time import sleep
from flask import Flask

from pymobiledevice3.remote.common import TunnelProtocol
from pymobiledevice3.exceptions import AlreadyMountedError
from pymobiledevice3.usbmux import select_devices_by_connection_type
from pymobiledevice3.lockdown import LockdownClient, create_using_usbmux
from pymobiledevice3.services.installation_proxy import InstallationProxyService
from pymobiledevice3.services.mobile_image_mounter import auto_mount_personalized
from pymobiledevice3.services.dvt.instruments.process_control import ProcessControl
from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
from pymobiledevice3.tunneld import get_tunneld_devices, TUNNELD_DEFAULT_ADDRESS, TunneldRunner

from pymobiledevice3._version import __version__ as pymd_ver
from SideJITServer._version import __version__


devs = []
app = Flask(__name__)
logging.basicConfig(level=logging.WARNING)


class App:
    __slots__ = ('name', 'bundle', 'pid')

    def __init__(self, name: str, bundle: str, pid: int = -1):
        self.name = name
        self.bundle = bundle 
        self.pid = pid

    def __repr__(self):
        return f"App<'{self.name}', {self.pid}>"

    def asdict(self):
        return {"name": self.name, "bundle": self.bundle, "pid": self.pid}

class Device:
    __slots__ = ('handle', 'name', 'udid', 'apps')

    def __init__(self, handle, name: str, udid: str, apps: list[App]):
        self.handle = handle
        self.name = name
        self.udid = udid
        self.apps = apps

    def __repr__(self):
        return f"Device<'{self.udid}', {self.apps}>"

    def refresh_apps(self) -> "Device":
        apps = InstallationProxyService(lockdown=self.handle).get_apps()
        apps = {apps[app]['CFBundleDisplayName']: app for app in apps if 'Entitlements' in apps[app]
                and 'get-task-allow' in apps[app]['Entitlements'] and apps[app]['Entitlements']['get-task-allow']}
        self.apps = [App(name, bundle) for name, bundle in apps.items()]
        return self

    def launch_app(self, bundle_id: str, sus: bool = False) -> int:
        with DvtSecureSocketProxyService(lockdown=self.handle) as dvt:
            process_control = ProcessControl(dvt)
            return process_control.launch(bundle_id=bundle_id, arguments={},
                                          kill_existing=False, start_suspended=sus,
                                          environment={})

    def enable_jit(self, name: str):
        apps = [a for a in self.apps if a.name == name or a.bundle == name]
        if len(apps) == 0:
            return f"Could not find {name!r}!"
        app = apps[0]

        if app.pid > 0 and app.pid == self.launch_app(app.bundle):
            return f"JIT already enabled for {name!r}!"

        debugserver = \
        (host, port) = \
        self.handle.service.address[0], self.handle.get_service_port('com.apple.internal.dt.remote.debugproxy')

        app.pid = self.launch_app(app.bundle, True)

        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        logging.info(f"Connecting to [{host}]:{port}")
        s.connect(debugserver)

        s.sendall(b'$QStartNoAckMode#b0')
        logging.info(f"StartNoAckMode: {s.recv(4).decode()}")

        s.sendall(b'$QSetDetachOnError:1#f8')
        logging.info(f"SetDetachOnError: {s.recv(8).decode()}")

        logging.info(f"Attaching to process {app.pid}..")
        s.sendall(f'$vAttach;{app.pid:x}#38'.encode())
        out = s.recv(16).decode()
        logging.info(f"Attach: {out}")

        if out.startswith('$T11thread') or '+' in out:
            s.sendall(b'$D#44')
            new = s.recv(16)
            if any(x in new for x in (b'$T11thread', b'$OK#00', b'+')):
                logging.info("Process continued and detached!")
                logging.info(f"JIT enabled for process {app.pid} at [{host}]:{port}!")
            else:
                logging.info(f"Failed to detach process {app.pid}")
        else:
            logging.info(f"Failed to attach process {app.pid}")

        s.close()
        return f"Enabled JIT for {app.name!r}!"

    def asdict(self):
        return {self.name: [a.asdict() for a in self.apps]}


def refresh_devs():
    global devs
    devs = []
    for dev in get_tunneld_devices():
        try:
            auto_mount_personalized(dev)
        except AlreadyMountedError:
            pass
        devs.append(Device(dev, dev.name, dev.udid, []).refresh_apps())

def get_device(udid: str):
    global devs
    d = [d for d in devs if d.udid == udid]
    return None if len(d) != 1 else d[0]

@app.route("/")
def devices():
    global devs
    if len(devs) == 0:
        return {"ERROR": "Could not find any device!"}
    return {d.name: d.udid for d in devs}

@app.route("/re/")
def refresh_devices():
    refresh_devs()
    return {"OK": "Refreshed!"}

@app.route("/<device>/")
def get_apps(device):
    dev = get_device(device)
    if dev:
        return [a.asdict() for a in dev.apps]
    return {"ERROR": "Could not find device!"}

@app.route("/<device>/re/")
def refresh_apps(device):
    dev = get_device(device)
    if dev is None:
        return {"Error": "Could not find device!"}
    dev.refresh_apps()
    return {"OK": "Refreshed app list!"}

@app.route("/<device>/<name>/")
def enable_jit_for_app(device, name):
    dev = get_device(device)
    if dev is None:
        return "Could not find device!"
    return dev.enable_jit(name)

def start_tunneld_proc():
    TunneldRunner.create(TUNNELD_DEFAULT_ADDRESS[0], TUNNELD_DEFAULT_ADDRESS[1],
                         protocol=TunnelProtocol('quic'), usb_monitor=True, wifi_monitor=True)

def prompt_device_list(device_list: list):
    device_question = [inquirer3.List('device', message='choose device', choices=device_list, carousel=True)]
    try:
        result = inquirer3.prompt(device_question, raise_keyboard_interrupt=True)
        return result['device']
    except KeyboardInterrupt:
        raise Exception()

@click.command()
@click.option('-p', '--port', default=8080, help='Set the server port')
@click.option('-e', '--version', is_flag=True, default=False, help='Prints the versions of pymobiledevice3 and SideJITServer')
@click.option('-d', '--debug', is_flag=True, default=False, help='Enables debug output of the flask server')
@click.option('-t', '--timeout', default=10, help='The number of seconds to wait for the pymd3 admin tunnel')
@click.option('-v', '--verbose', default=0, count=True, help='Increase verbosity (-v for INFO, -vv for DEBUG)')
@click.option('-y', '--pair', is_flag=True, default=False, help='Alternate pairing mode, will wait to pair to 1 device')
def start_server(verbose, timeout, port, debug, pair, version):
    if version:
        click.echo(f"pymobiledevice3: {pymd_ver}" + "\n" + f"SideJITServer: {__version__}")
        return

    if pair:
        click.echo("Attempting to pair to a device! (Ctrl+C to stop)")
        devices = select_devices_by_connection_type(connection_type='USB')
        while len(devices) == 0:
            devices = select_devices_by_connection_type(connection_type='USB')
            click.echo("No devices..")
            sleep(3)

        create_using_usbmux()
        devices = [create_using_usbmux(serial=device.serial, autopair=False) for device in devices]
        print(devices)
        if len(devices) > 1:
            dev = prompt_device_list(devices)
        else:
            dev = devices[0]
        dev.pair()
        if "y" not in input("Continue? [y/N]: ").lower():
            return

    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    verbosity_level = min(len(log_levels) - 1, verbose)
    logging.getLogger().setLevel(log_levels[verbosity_level])

    tunneld = multiprocessing.Process(target=start_tunneld_proc)
    tunneld.start()

    atexit.register(tunneld.terminate)

    sleep(timeout)

    refresh_devs()

    app.run(host='0.0.0.0', port=port, debug=debug)
