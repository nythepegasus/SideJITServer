# SideJIT
This is still in development, but this is the current state of it.

To get it going, run this in an admin terminal or as sudo:
```sh
python3 -m pymobiledevice3 remote tunneld
```

Then ensure you create a virtual environment in this directory and run the server:
```sh
python3 -m venv venv

# If you're on macOS/Linux
. .venv/bin/activate
# If you're on Windows
.\venv\Scripts\Activate.ps1

pip3 install -r requirements.txt
python3 main.py
```

Here is the [Shortcut](https://www.icloud.com/shortcuts/b0ffc9c3f0e74e7a8f8052c89fa322cf) that goes along with this.
