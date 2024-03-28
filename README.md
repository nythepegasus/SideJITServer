# SideJITServer
This project allows you to start a server that wirelessly gives you JIT for iOS 17+ on Windows/macOS. Linux support depends on a [kernel patch](https://github.com/doronz88/pymobiledevice3/issues/566#issuecomment-1850486679).


To get it going: (run this in an admin terminal if you're on Windows)
```sh
python3 -m venv venv

# If you're on macOS/Linux
. ./venv/bin/activate
# If you're on Windows using PowerShell
.\venv\Scripts\Activate.ps1
# CMD
.\venv\Scripts\Activate.bat

# All
pip3 install -r requirements.txt
# Windows
.\venv\Scripts\python3.exe main.py
# macOS
sudo python3 -m SideJITServer --help
```

Or with PyPI:
```
python3 -m venv venv
# Activate venv..

pip3 install SideJITServer
SideJITServer --help
```

Here is the [Shortcut](https://www.icloud.com/shortcuts/b0ffc9c3f0e74e7a8f8052c89fa322cf) that goes along with this.
