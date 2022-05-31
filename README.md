# Software Documentation for Electric Wire Routing Optimization Software for Wire Routing in 3D Space for Aircraft Design
## Boeing / The University of Texas at Austin

This is a repository for COE 374 Senior Design Project. Our team worked with a Boeing respresentative to build an application that allows for the routing of multiple wires in open 3D space. 

---

## Setting up your environment on Windows:

Check if Python 3 is installed by running `python --version` from the command prompt.

If it is not yet installed, download and install python from <https://www.python.org/downloads/windows>.  Click on Python 3.7.0 and scroll down until you find the executable installer.

Clone this github repository to your local machine and navigate to the repository in command prompt by using the following commands: 'git clone https://github.com/RileyYlagan/Wire-Routing-Optimization-Project.git' and 'cd 'Wire-Routing-Optimization-Project'

Update pip using `python -m pip install --upgrade pip`.

Install virtualenv using `python -m pip install --user virtualenv`.

Create a new virtualenv in the cloned repository using `python -m venv venv`.

Activate the virtualenv using `.\venv\Scripts\activate`.

Install all necessary packages using `pip install -r requirements.txt`.

When you're done, deactivate the virtualenv using `deactivate`.

## Setting up your environment on MacOS or Windows:

Check if Python is installed by running `python3 --version`.

Clone the github repository to your local machine and navigate to the repository in command prompt.

Update pip using `python3 -m pip install --upgrade pip`.

Install virtualenv using `python3 -m pip install --user virtualenv`.

Create a new virtualenv in the cloned repository using `python3 -m venv venv`.

Source the virtual environment: `source venv/bin/activate`.

Update pip again to update pip inside the virtualenv: `pip install -U pip`  

Install requirements.txt: `pip install -r requirements.txt`  

## File Structure of Software
 The repository is laid out as shown below, where the main code is in the `EWRO` folder.
  
    .
    ├── EWRO                  
        ├── input                    
        ├── modules                    
        ├── output
        └── main.py
    ├── requirements.txt
    └── README.md

Inputs for the constraints and the input mesh are to be put into the folder labelled `input`. Examples for both inputs are located in the folder. The modules of code are split into `discretization.py` and `algorithm.py` and are executed in sequence through the `main.py`. Once the software is done running, the wires are put into a folder labelled with the project name within the `output` folder.

## Command Line Interactivity
The software can be ran with a simple command:
    
    python3 main.py -m <meshInput> -s <scaleFactor> -w <wireInput> -o <outputName>
Where the flag:
- `-m` is the mesh input (e.g Example_Maze.stl)*
- `-w` is the wire constraint input (e.g Example_Wire_Input.csv)
- `-s` is the scale factor of the mesh; default = 2
- `-o` is the project name

If needed, the `-h` flag can be used to see which flags correspond to the right user input.
Currently, the mesh input only works for mazes that have walls, have a floor, and are oriented with up in the positive z-direction. Formatting for the wire constraints can be seen in the example input. 

## Output
As mentioned previously, the wires will be individually saved in the project folder in `output`. A log detailing the time of each section of the software will be shown as the software is running and will also be saved in the project folder. The log also contains the distances if each wire and the total time ran.

In order to view the results of the software, a third party 3D mesh processing software, such as MeshLab, is recommended.




