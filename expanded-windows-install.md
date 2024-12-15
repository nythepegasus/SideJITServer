# "Dummy-proof" Installation

**Note-1** I added some [changes](#update-22-nov-2024) at the bottom. TL;DR: Updated to Python v13.3 to solve some errors I was getting. Check it out!

**Note-2** I added more information related to [using SideJITServer after an iOS Update](#update-14-dec-2024). 

**As of 14 Dec, 2024, using this guide, including the two notes above, SideJITServer works on iOS/iPadOS 18.2 (iPhone 16 Pro/iPad Pro 11" Gen 3)**

## Part I

### Python Pre-Install Notes 
	
i. Installing Python v3.11.x via [pyenv-win](https://github.com/pyenv-win/pyenv-win) (I installed 3.11.7 and it works fine)

ii. Probably best off nuking everything to do with python, python3, pip and pip3. Then start over and install correctly

iii. pyenv makes installing ANY future versions of python incredibly easy while maintaining correct PATH so you don't have weird errors

Following the steps in the github repo for pyenv-win.
[stuff in [] is my additional info. the rest is quoted.]

Quick start

1. Install pyenv-win in PowerShell. [Copy/paste into PowerShell]

    ```Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"```

    [Close PowerShell after the script above. Then...]

2. Reopen PowerShell

3. Run ```pyenv --version``` to check if the installation was successful.

4. Run ```pyenv install -l``` to check a list of Python versions supported by pyenv-win

5. Run ```pyenv install <version>``` to install the supported version
    
    5a. [I installed v3.11.7: ```pyenv install 3.11.7``` ]

6. Run pyenv global <version> to set a Python version as the global version

    6a. [ ```pyenv global 3.11.7``` in my case]

7. Check which Python version you are using and its path
```pyenv version```

    7a. [my output for python v3.11.7 -> ```3.11.7 (set by C:\Users\USERNAME\.pyenv\pyenv-win\version)``` ]

8. Check that Python is working
```python -c "import sys; print(sys.executable)"```

    8a. [my output for python v3.11.7 -> ```C:\Users\USERNAME\.pyenv\pyenv-win\versions\3.11.7\python.exe``` ]
	
You're done! WOW! Read the pyenv-win repo for more endless information on using pyenv...

## Part II

Install Time!

**I HIGHLY RECOMMEND USING CMD!** 

For whatever reason, Windows Terminal *would not work* for me. CMD worked the first try and on repeat tries! (And yes, I was running it in admin mode, duh)

Open CMD as admin by

i. Push ```Win-Key+R``` to bring up run. Type ```CMD``` in the search box DONT PRESS ENTER YET

ii. Hold ```Ctrl+Shift``` and then push ```Enter```

iii. You will see in the upper left corner it says "Administrator" and it will start you in the ```C:\Windows\System32``` directory

Instructions just ripped from [SideJITServer](https://github.com/nythepegasus/SideJITServer) repo. All credit to nythepegasus. I just omitted part of them and added a little to streamline for specific Windows install...

0. Download the latest SideJITServer from the [releases](https://github.com/nythepegasus/SideJITServer/releases)
   
1. (I just do this in the Windows system because it's easier for me) Create a SideJITServer directory (folder) somewhere. Perhaps ```C:\Users\USERNAME\SideJITServer``` (where USERNAME is your user...name.) In Windows CMD you make a directory just like Linux. eg: ```mkdir C:\Users\USERNAME\SideJITServer``` would make the example directory I mentioned. Obviously use your own username. Extract the SideJITServer.zip archive to your directory at the root level of it. So if you go into the example directory you will see files such as "requirements.txt" and "compose.yaml" and such. Cut/paste the files/folders if you need to. Or leave the dir structure messed up...up to you.
   
2. ```cd C:\Users\USERNAME\SideJITServer``` to get to the example directory inside your administrator CMD
   
3. Start setting up the virtual env 
   
   ```python3 -m venv venv```
   
4. Activate it 
   
   ```.\venv\Scripts\Activate.bat```

5. You should now see something like this in CMD
   
    ```(venv) C:\Users\USERNAME\SideJITServer>```
    
     that ```(venv)``` is important! Make sure it's there before the next step!
 
6. Now install the required packages 
 
   ```pip3 install -r requirements.txt```
   
7. That takes a minute or so to download a bunch of stuff. Then run 
  
    ```pip3 install SideJITServer```

    (If you got an error saying pip3 not found just change pip3 to pip)

8. Let's see if everything works (Make sure you're still inside venv!)
 
   run
    ```SideJITServer --version```

    my output:

    ```pymobiledevice3: 4.14.16```

    ```SideJITServer: 1.3.6```

Wow! PC side setup is complete! Get your iDevice ready

## Part III

Make sure your device is connected!

Make sure you're still inside the venv, if applicable! (If you followed this "guide" then it is applicable!)

**PROTIP** 
In the future, when you need to enable JIT 
 
 i. open your admin CMD prompt (Win+R -> type CMD -> hold Ctrl+Shift and push Enter)

 ii. type into the prompt
    ```C:\Users\USERNAME\SideJITServer\venv\Scripts\Activate.bat```

iii. You could even make a cute little shortcut or .bat file on your desktop or something... just make sure it runs CMD as admin!

1. If running JITServer for the first time or you need to re-pair, then run
   ```SideJITServer --pair```

   And wait a bit

2. Eventually you should see an output like
   
    ```Server started on http://<your-pc-IP>:8080```
    
    Obviously the IP will be dependent on your local network. It could be http://192.168.x.y:8080 or http://10.x.y.z:8080 (more than likely one of those two)

3. With that done, I will just point you to the repo guide to finish. Copied below from [here](https://github.com/nythepegasus/SideJITServer)

"Now thats done, Install [this](https://www.icloud.com/shortcuts/b0ffc9c3f0e74e7a8f8052c89fa322cf) shortcut

After that its gonna ask you to put in your device's UDID, Go to your PC and see your local ipaddress mine is 192.168.0.6:8080 and on your phone go to that (your local address) and copy the one that beside usbmux (example : 00001111-000A1100A11101A)

Now it's gonna ask you for SideJIT Server address! Just type in the address you use earlier to access device's UDID

for example : http://192.168.0.6:8080 (You must include the http and not include / at the end!)

Now run the shortcut!

It gonna ask you to allow to access your local ip address just click allow!

Now select the application that you want to give JIT access to and you're done! (might ask for notification. It is recommended that you allow so you see if the JIT fail or succeed)

Happy JITing! :3"

## Update 22-Nov-2024

I updated my phone/iPad to iOS/iPadOS 18.1.1 and was encountering some errors such as device "network lost" on the devices when trying to enable JIT. I also recently, since initially piecing together this guide, changed my home network. Some combo of these events was causing me errors and I couldn't get it to work. So, I chose the nuclear option... 

**WARNING** When you use Python 3.13 Windows will also require you to install Microsoft Visual C++ (MSVC) build tools. This is a MASSIVE install! 3GB, minimum! This is required because you have to literally build, yourself, part of the requirements for this project. With lower python versions other builds exist for certain things. If you use newer versions, this isn't always the case. So, you must build yourself. It takes longer and takes up disk space. This is Microsoft's fault because they don't seem to want people only installing SOME of the build tools... they want the whole thing. Just letting you know now.

Here's how I got it working again:

i. I went in and deleted the contents of the SideJITServer dir. In my case ```C:\Users\USERNAME\SideJITServer```

ii. I also deleted the pair files. Found in this directory by default ```C:\ProgramData\Apple\Lockdown```

iii. I decided to use the newest stable python, 3.13. ```pyenv install 3.13``` if you followed the original instructions and have pyenv installed (see how convenient it is???)

iv. Time for a fat install. You need to download the MS Visual Studio .exe from [here](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022). Download the free community version.

v. Run the .exe. Once it loads up you have to tell the program which components to install:

1. Under the first tab, "Workloads", Check the box for "Desktop development with C++"
   
2. On the right side there should be a checklist of things you are installing and are available. Make sure to also check the box for "Windows 11 SDK" (or Windows 10 if using that). It may already be check marked. If so, good, move on.

3. Here is what it looks like before hitting install (mine was already installed thus 0GB). The size should be over 3GB if you've never installed anything from Visual Studio build tools before.

![Screenshot 2024-11-22 120104](https://github.com/user-attachments/assets/c4bca988-580e-48f0-8a18-da74e717079f)
    
4. Just hit install (The "install while downloading" option is default and probably best to leave that on to speed things up)
    
5. Restarting is optional, but best to just do it.

vi. That's it. The rest of the guide is the same. With the newest python installed and the build tools installed, SideJITServer should reinstall fine. Then you just run SideJITServer the same as you did before but now it will be running with python 13.3. This cleared up issues for me and also confirmed that python 13.3 works with this version of SideJITServer.

## Update 14-Dec-2024

**Quick Setup Again After iOS Update**

For some reason, after an iOS update, the program throws a bunch of errors. There may be a more efficient solution here, but I've found the *easiest* solution is nuking the install and re-install.

### Preparation 

1. Find and delete any mention of iDevices and SideJITServer. I HIGHLY recommend [Everything](https://www.voidtools.com/)+[EverythingToolbar](https://github.com/srwi/EverythingToolbar) for this task and in general. The built-in Windows 10/11 search... isn't great. This tool is a big improvement. (Totally free as well) 
2. Download newest SideJITServer from [releases](https://github.com/nythepegasus/SideJITServer/releases)

### Quick Instructions

1. Extract release to ```C:\Users\USERNAME\SideJITServer```
2. Change directory ```cd C:\Users\USERNAME\SideJITServer```
3. Setup venv ```python3 -m venv venv```
4. Activate ```.\venv\Scripts\Activate.bat```
5. Install packages ```pip3 install -r requirements.txt```
6. Install SideJITServer ```pip3 install SideJITServer```
7. Check install is working ```SideJITServer --version```

Continue following [Guide: Part III](#part-iii)

Everything should be working again.
