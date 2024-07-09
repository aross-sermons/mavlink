# Drone Simulation Usage and Notes  
### Working Environment  
**Requirements**  
- Python2.7 running on a Linux-based machine. This project uses WSL with Ubuntu.  
- For organization, a virtual environment is recommended. Python2.7 does not come with venv. Use virtualenv as outlined below.  
- Pip packages: dronekit, dronekit-sitl  
- (Optional) Missionplanner software to view drone simulation.  
  
**Install Python2.7 on Ubuntu**  
1. Add deadsnakes Repository  
    `sudo apt install software-properties-common`  
    `sudo add-apt-repository ppa:deadsnakes/ppa`  
    `sudo apt update`  
2. Install Python2.7  
    `sudo apt install python2.7 python-pip`  
  
**Virtual Environment on Ubuntu**  
1. Install virtualenv  
    `python2.7 -m pip install virtualenv`  
2. Create Virtual Environment  
    `virtualenv -p python2.7 envname`  
3. Switch to Virtual Environment  
    `source /path/to/envname/bin/activate`  
4. (Optional) Leave Virtual Environment  
    `deactivate`  

**Installing Required Packages**  
    `python2.7 -m pip install dronekit dronekit-sitl`  
### Starting the Simulation  
**Code Execution**  
Run each command in a different terminal session. Remember to switch each session to the virtual environment if using.  
Once the simulation is started, the simulated vehicle listens at 127.0.0.1:5760. After port 5760 is connected to, it will listen to 5763, 5766, 5769, and so forth.  
1. Start Simulation  
    `dronekit-sitl copter --model=quad --home=38.21982,-85.7047507,0,0`  
    OR
    `sh start-sitl.sh`  
    This command will start a quad copter simulation at the given coordinates, altitude, and rotation (--home argument).  
2. (Optional) Connect Missionplanner  
    Open Missionplanner and in the top right corner select "tcp", "57600", and press "connect".  
    For host name/ip use: 127.0.0.1  
    For port use: 5760  
3. Run Mission Scripts  
    The directory dronekit_python_research has a default box_mission.py that can be used as an example.  
    Run this script or your own with `python2.7 scriptname.py` in a virtual environment.  
### Using quad_utils in a Script  
**What is quad_utils?**  
It's a simple library of wrappers that use dronekit and pymavlink to send commands to a remote vehicle.
### Script Notes  
**Python2.7 Restrictions**  
Because we have to use python2.7, some import statments in the source code need to be corrected. Specifically, if you encounter a syntax error in the ardupilotmega.py file, you must navigate to the code that references ardupilotmega.py and change the import statement from "from pymavlink.dialects.v10 import ardupilotmega" to "from pymavlink.dialects.v10.python2 import ardupilotmega".  
Some features of python3 are absent, like formatted print statements using the `print(f'My Var: {var}')` pattern.  
    
# Encryption Examples
### Working Environment
- Python3.12 running on a Linux-based machine. This project uses WSL with Ubuntu.  
- For organization, a virtual environment is recommended.  
- Pip packages: pycryptodome  
**Setting Up Virtual Environment**  
1. Install Python3.12 and venv
    `sudo apt install python3.12 python3.12-venv`
2. Make Virtual Environment  
    `python3.12 -m venv envname`  
3. Switch to Virtual Environment  
    `source /path/to/envname/bin/activate`  
4. (Optional) Leave Virtual Environment  
    `deactivate`  
**Installing Required Packages**  
    `pip install pycryptodome`  