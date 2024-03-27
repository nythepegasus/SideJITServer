from flask import Flask, g
from subprocess import Popen, PIPE

from pymobiledevice3.tunneld import get_tunneld_devices
from pymobiledevice3.services.installation_proxy import InstallationProxyService
from pymobiledevice3.services.dvt.instruments.process_control import ProcessControl
from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService


import socket

app = Flask(__name__)

devs = []
apps = {}

class App:
    def __init__(self, name: str, bundle: str, pid: int = -1):
        self.name = name
        self.bundle = bundle 
        self.pid = pid

    def __repr__(self):
        return f"App<'{self.name}', {self.pid}>"

    def asdict(self):
        return {"name": self.name, "bundle": self.bundle, "pid": self.pid}

class Device:
    def __init__(self, handle, name: str, udid: str, apps: list[App]):
        self.handle = handle
        self.name = name
        self.udid = udid
        self.apps = apps

    def __repr__(self):
        return f"Device<'{self.udid}', {self.apps}>"

    def asdict(self):
        return {self.name: [a.asdict() for a in self.apps]}


def get_dev_apps(device):
    apps = InstallationProxyService(lockdown=device).get_apps()
    return {apps[app]['CFBundleDisplayName']: app for app in apps if 'Entitlements' in apps[app] and 'get-task-allow' in apps[app]['Entitlements'] and apps[app]['Entitlements']['get-task-allow']}


def launch_app(device, bundle_id: str):
    with DvtSecureSocketProxyService(lockdown=device) as dvt:
        process_control = ProcessControl(dvt)
        pid = process_control.launch(bundle_id=bundle_id, arguments={},
                                     kill_existing=False, start_suspended=False,
                                     environment={})
        return pid

def enable_jit(device, app: str):
    debugserver_host, debugserver_port = device.service.address[0], device.get_service_port('com.apple.internal.dt.remote.debugproxy')

    pid = launch_app(device, app)

    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    debugserver_address = (debugserver_host, debugserver_port)
    print("Connecting to " + str(debugserver_address))
    s.connect(debugserver_address)

    s.sendall('$QStartNoAckMode#b0'.encode())
    print("StartNoAckMode: " + s.recv(1024).decode())

    s.sendall('$QSetDetachOnError:1#f8'.encode())
    print("SetDetachOnError: " + s.recv(1024).decode())

    print(f"Attaching to process {pid}..")
    pid_hex = format(int(sys.argv[1]), 'x')
    s.sendall(f'$vAttach;{pid_hex}#38'.encode())
    print("Attach: " + s.recv(1024).decode())

    if out.startswith('$T11thread'):
        s.sendall('$D#44'.encode())
        if s.recv(1024).decode() == '$OK#00':
            print("\nProcess continued and detached!")
            print(f"JIT enabled for process {pid} at {debugserver_address}!")
        else:
            print(f"Failed to detach process {pid}")
    else:
        print(f"Failed to attach process {pid}")

    s.close()
    return pid


@app.route("/")
def devices():
    global devs
    return [d.udid for d in devs]

@app.route("/re")
def refresh_devices():
    global devs
    devs = []
    for dev in get_tunneld_devices():
        apps = []
        for name, bundle in get_dev_apps(dev).items():
            apps.append(App(name, bundle))
        devs.append(Device(dev, dev.name, dev.udid, apps))
    return "Refreshed!"

@app.route("/<device>/")
def get_apps(device):
    global devs
    dev = [d for d in devs if d.udid == device]
    if len(dev) != 1:
        return "Could not find device!"
    dev = dev[0]
    return [a.asdict() for a in dev.apps]

@app.route("/<device>/re")
def refresh_apps(device):
    global devs
    dev = [d for d in devs if d.udid == device]
    if len(dev) != 1:
        return "Could not find device!"
    dev = dev[0]
    apps = []
    for name, bundle in get_dev_apps(dev.handle).items():
        apps.append(App(name, bundle))
    dev.apps = apps
    return "Refreshed app list!"

@app.route("/<device>/<name>")
def enable_jit_for_app(device, name):
    global devs
    dev = [d for d in devs if d.udid == device]
    if len(dev) != 1:
        return "Could not find device!"
    dev = dev[0]
    app = [a for a in dev.apps if a.name == name]
    bundles = [a for a in dev.apps if a.bundle == name]
    if len(app) != 1 and len(bundles) != 1:
        return f"Could not find {app!r}"
    if len(app) == 1:
        app = app[0]
    else:
        app = bundles[0]

    if app.pid == -1:
        app.pid = enable_jit(dev.handle, app.bundle)
    else:
        pid = launch_app(dev.handle, app.bundle)
        if pid != app.pid:
            app.pid = enable_jit(dev.handle, app.bundle)
        else:
            return f"JIT already enabled for {app.name!r}!"

    return f"Enabled JIT for {app.name!r}!"


if __name__ == '__main__':
    for dev in get_tunneld_devices():
        apps = []
        for name, bundle in get_dev_apps(dev).items():
            apps.append(App(name, bundle))
        devs.append(Device(dev, dev.name, dev.udid, apps))

    app.run(host='0.0.0.0', port=8080, debug=True)
