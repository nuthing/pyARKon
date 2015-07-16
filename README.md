[RCON] pyARKon - Windows Desktop Client (OPEN-SOURCE)
Tool used to manage ARK: Survival Evolved servers using python. It's also possible to use a mobile device with this script to manage your server even more remotly! It's a bit technical, but the possibility is there and shouldn't be much code to change.

[]> Windows XP/7/8/10
Download v1.5.2[github.com] [.zip]
Download the pyARKon-v1.5.2-win32.zip, and extract it to a folder on your computer.
Browse to the folder and launch the pyarkon.exe

[]> Want to compile from source?
Download and install python 2.7
Download and install py2exe
Download the latest stable version of pyARKon from the github source link bellow.

Edit setup.py and remove the # from the following two lines:
#import py2exe
#console=["pyarkon.py"],

Then cd to the directory you downloaded the source and run:
python setup.py py2exe
