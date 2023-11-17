# CRM - Geotab Integration

This script purpose is to update the odometer field of the vehicles on RDA's CRM ("Vehículos" module), getting the data from the Geotab's system

# Instalation for a development environment
## Dependencies
The main dependency is Python, the minimal version required is 3.7 but the recomended one is 3.11.

For the other dependencies (libraries) needed by the code, you must execute:
```
pip install -r requirements-dev.txt
```
## .env file
You need to create a .env file with the same structure of .env.example file, but need to replace the "XXXXXXXXXXXXXX" for the corrects values.

## Pre-commit
For better dev practices it's recommended to instalar pre-commit.
The python library was installed in the previus step, but it's needed to install it in the git hooks folder. To do this you need to run:
```
pre-commit install
```
this tool is automatically executed when you try to do a git commit, if there are some error on the code, as unused variables, the commit will fail, otherwise will be done correctly.
You can run this with the below command:
```
pre-commit run -a
```
# Execution
To run the program with:
```
python main.py
```
You can see the output on the corriesponding log file on the folder "logs"
