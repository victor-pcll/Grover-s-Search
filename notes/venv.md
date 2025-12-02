# Virtual Environment Setup (venv)

To keep dependencies isolated and ensure reproducible experiments, it is recommended to work inside a Python virtual environment. A virtual environment allows you to install packages locally for this project without affecting your global Python installation.

Below are the commands to create, activate, and install the required dependencies:
```
python3 -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```
Once the environment is activated, any Python or pip command will use the local environment.