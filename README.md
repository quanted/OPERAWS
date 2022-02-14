# OPERAWS
Web service wrapper for OPERA - a free and open source QSAR tool for predicting physicochemical properties and environmental fate endpoints

Deploying OPERAWS with Windows Task Scheduler:

Install Git for Windows: https://git-scm.com/download/win

Install Python 3 onto the computer.

Download and install OPERA application:
	
Install link: https://github.com/kmansouri/OPERA/releases

Extract the zip file, and run “OPERA2.3_mcr_Installer.exe”. Once finished, make sure the application is installed at “C:\Program Files\OPERA”.

On the Windows VM, pull down the OPERAWS repository:

git pull https://github.com/quanted/OPERAWS
cd OPERAWS
git checkout dev

The following steps Open Windows Task Scheduler application and select “Create Task…” in the right-hand column labeled “Task Scheduler Library.”

Below are a series of screenshots that shows the task settings.

A Python process should spin up after creating the task:

TODO: Add screenshot images to this README.
