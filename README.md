# Battleship

## Installation for Development
1. [Install Python3+](https://www.python.org/downloads/) 
2. Create a virtual environment
   - In the root directory of the repository, execute the following command: `python3 -m venv <venv_path>`
     - This will create a directory with the path `<venv_path>` relative to the current working directory of the terminal
     - For more information, view the [python documentation](https://docs.python.org/3/library/venv.html)
3. Activate the Virtual Environment 
   - On Windows: 
     - `.\<venv_path>\Scripts\activate`
   - On Mac/Linux: 
     - `source ./<venv_path>/bin/activate`
4. Install Dependencies
   - With the Virtual Environment activated, execute `pip install -r requirements.txt` to install all dependencies for the project

## Starting the Game
To start the game for development, ensure the virtual environment is activated and execute `python3 main.py` from the root directory of the project.