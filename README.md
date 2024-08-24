# SideJITServer
This project allows you to start a server that wirelessly or via USB gives you JIT for iOS 17+ on Windows/macOS (Linux if you use the correct newer pymobiledevice3 version and are on iOS 17.4+)

## Prerequisites 

- Python 3.10+ (All OS) you can download it from [here](https://www.python.org/downloads/) (Make sure you clicked "Add Python to PATH")
- iTunes (Windows Only) download it from [here](https://www.apple.com/itunes/download/win64/)

## How to get this running (Run with Administrator!)

### Option 1: PyPi Method 

Open Terminal on Windows or macOS (you may need to use CMD on Windows) and run these commands:

```
# Now you need to run these commands (not the ones with the #):

# Setup venv
python3 -m venv venv 

# Now we need to Activate it

# macOS and Linux
. ./venv/bin/activate

# Windows but using Powershell
.\venv\Scripts\Activate.ps1

# Windows but using Command Prompt/CMD
.\venv\Scripts\Activate.bat

# Now let's install all the required packages! (Make sure you're still inside venv!)

# All OS
pip3 install SideJITServer

# If you got an error saying pip3 not found just change pip3 to pip

# Let's see if everything works (Make sure you're still inside venv!)
SideJITServer --version
# Output should show SideJITServer!
```

### Option 2: Direct download (if available)
Go to the latest [GitHub Release](https://github.com/nythepegasus/SideJITServer/releases/latest) or if it doesn't exist you can get it from [nightly.link](https://nightly.link/nythepegasus/SideJITServer/actions/runs/10502911845/Windows%20Build.zip) and check if there are executable downloads, such as `SideJITServer-windows-x86_64.exe`, depending on your OS and your architecture.

Download the correct executable, and run it as Administrator from your terminal or Powershell following the directions below. If you are on Mac or Linux, you must first run `chmod +x ./(your downloaded .bin file)` before executing the file with sudo.

Python is not necessary for this approach.


# How to use SideJITServer?
- Make sure your device is connected!
- Make sure you're still inside the venv, if applicable!
- Common Knowledge
  
Now run `SideJITServer` and on your PC make sure you click on Trust this PC! 

After the first time running `SideJITServer` you shouldnt need your Device to be plugged in only on the same Wi-Fi Network or Over Ethernet

Now thats done, If you use SideStore (you will need to be on the [Nightly](https://github.com/SideStore/SideStore/releases/tag/nightly)) then you do not need all this, it should automatically detect it. if not then you will need to input the SideJITServer address into SideStore Settings

If you do not use SideStore continue, Install [this](https://www.icloud.com/shortcuts/b0ffc9c3f0e74e7a8f8052c89fa322cf) shortcut


After that its gonna ask you to put on your device's UDID, Go to your PC and see your local ipaddress mine is `192.168.0.6:8080` and on your phone go to that (your local address) and copy the one that beside usbmux (example : 00001111-000A1100A11101A)

Now it's gonna ask you for SideJITServer address! Just type in the address you use earlier to access device's UDID

for example : `http://192.168.0.6:8080` (You must include the http and not include / at the end!)

Now run the shortcut!

It gonna ask you to allow to access your local ip address just click allow!

Now select the application that you want to give JIT access to and you're done! (might ask for notification. It is recommended that you allow so you see if the JIT fail or succeed)

Happy JITing! :3
