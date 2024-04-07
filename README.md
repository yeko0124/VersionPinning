# VersionPinning -> Personal Project 
(2024.03 / for a month)
USD file version pinning for Houdini users (artists).
<br>When an artist works, versions of the USD file can be easily viewed, and information about the versions can be easily checked.

## Main Function
1. Upload Database Automatically
   - Easily store information about version files in a database through customized USD ROP nodes on Houdini.
2. Visualize Version Information
   - MVC: You can check the file name, file path, author (artist), reference note, upload date, etc., of the version file through a table view.
   - In particular, you can see which files are currently connected to the final version through a green indicator.
3. Convenient File Access
   - You can conveniently access the version through the 'sublayer node' by selecting the version from the combo box and pressing the reload button.
4. Detach Version Notifications
   - Notify only when the version is updated via Discord.

---
## Code Dependency
<img width="500" alt="code_dependency" src="https://github.com/yeko0124/VersionPinning/assets/155792229/25959aff-7e85-4bf7-811a-6b3d7db7c755">

---
## Demonstration
### 1. Pinning
![pinning_demon](https://github.com/yeko0124/VersionPinning/assets/155792229/a647f9bf-37bc-49e8-9e8a-ac528fb3a69e)


### 2. Update on database and Alarm on Discord
![alarm_demon](https://github.com/yeko0124/VersionPinning/assets/155792229/8f90e086-268e-4640-8b05-bb4d90be6808)

---
## Install
1. Download zip file or use git pull to get files.
2. To run mysql in houdini, You need to follow some procedures.
   * Enter the path that comes out when you type **'hou.homeHoudiniDirectory()'** in the Houdini Python script.
   * Create **scripts** directory and create **123.py** in scripts directory that you created now.
   * Write this code in 123.py
      ```python
     import site
     site.addsitedir('hou.homeHoudiniDirectory()/scripts/site-packages')
     ```
   * Move **site-package** directory to **scripts** directory that you made. So, you need unzip the site-package zip file.
   * You must also change the password in the **libs/db.py** file.
3. Move **Lop** directory to same path where the **scripts** directory located.
   * The third line of the **'usd_rop_OnCreated.py'** file, which is located in Lop directory, requires you to change the path.
4. If you need, install qtawesome.
   ```$ pip install qtawesome```
5. Add to the Python panel and edit the interface to enter the code below.
   ```python
   from hutil.Qt import QtWidgets

   import site
   import importlib
   import pathlib

   path = site.addsitedir("Path to the folder where 'main_table_version.py' is located")

   import main_table_version

   importlib.reload(main_table_version)

   def onCreateInterface():
   global c
   c = main_table_version.VersionTable()
   return c

   def onDestroyInterface():
   global c
   del c
   
6. Done! (If you have any problem, let me know)
