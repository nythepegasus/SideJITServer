# SideJITServer
This project allows you to start a server that wirelessly or via USB gives you JIT for iOS 17+ on Windows/macOS/Linux if you use the correct newer pymobiledevice3 version.

## How to get this running (Run with Administrator!)

### Option 1: Python install
```sh
python3 -m venv venv # Run inside SideJITServer directory!

# Activate Python venv

# macOS
. ./venv/bin/activate

# Windows but using Powershell
.\venv\Scripts\Activate.ps1

# Windows but using Command Prompt/CMD
.\venv\Scripts\Activate.bat

# Now let's install all the required packages! (Make sure you're still inside venv!)
# All OS
pip3 install -r requirements.txt
pip3 install SideJITServer
# If you got an error saying pip3 not found just change pip3 to pip

# Let's see if everything works (Make sure you're still inside venv!)
SideJITServer --version
# Output should show SideJITServer!
```

Or use PyPI
```sh
python3 -m venv venv
# Activate venv..

pip3 install SideJITServer
SideJITServer --help
```

### Option 2: Direct download (if available)
Go to the latest [GitHub Release](https://github.com/nythepegasus/SideJITServer/releases/latest) and check if there are executable downloads, such as `SideJITServer-windows-x86_64.exe`, depending on your OS and your architecture. If there is no attached executable, you might find one in the [GitHub Actions](https://github.com/nythepegasus/SideJITServer/actions/workflows/compile.yml?query=is%3Asuccess) if a recent build worked and did not expire.

Download the correct executable, and run it as Administrator from your terminal or Powershell following the directions below. If you are on Mac or Linux, you must first run `chmod +x ./(your downloaded .bin file)` before executing the file with sudo.

Python is not necessary for this approach.


# How to use SideJITServer?
- Make sure your device is connected!
- Make sure you're still inside the venv, if applicable!
- Common Knowledge
  
Now run `SideJITServer --pair` and on your PC make sure you click on Trust this PC!
Also it will show you a prompt to continue just type "y"

### Usage

#### MacOS

##### 1. Run the server

```sh
# First run
sudo SideJITServer --pair
# Consecutive runs once paired
sudo SideJITServer
```

You should see an output similar to this.

<img width="602" alt="image" src="https://github.com/user-attachments/assets/fef15573-5a51-4a20-ada3-074f1c7f9765">

##### 2. Install / Run the shortcut

<b><p align="center">Install [this](https://www.icloud.com/shortcuts/b0ffc9c3f0e74e7a8f8052c89fa322cf) shortcut❗</p></b>

After that it's going ask you to put on your device's UDID, Go to your PC and see your local ipaddress mine is `192.168.0.6:8080` and on your phone go to that (your local address) and copy the one beside `usbmux` (example : `00001111-000A1100A11101A`)

Now it's gonna ask you for `SideJIT` Server address! Just type in the address you used earlier to access the device's UDID

for example : `http://192.168.0.6:8080` <b>(You must include the http and not include / at the end!)</b>

Now run the shortcut!

It going to ask you to allow to access your local ip address just click allow!

Now select the application that you want to give JIT access to and you're done! (it might ask for notification permissions). 
It is recommended that you allow so you see if the JIT fail or succeed.

Happy JITing! :3
