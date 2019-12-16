# Plotting Picarro Data

## Instalation
Install python3

Libraries used:
- Pandas
- Xlrd
- Matplotlib

## Using pipenv and virtual environment (recommended)
Install pipenv

    pip3 install pipenv --user

find the user directory used by pip3:

    python -m site --user-base

Add the user directory in the PATH environment variable


Clone the repository and execute inside the directory of the repository

    git clone https://github.com/ceordonez/Picarro_read_data.git

    pipenv shell

You can change the version of python3 installed in your PC changing the Pipfile

Then install the libraries requires 

    pipenv install


## Quick manual

### Using pipenv
Before run the program excecute in the folder of the program
    pipenv shell

### All users

Configurate the config\_file.py document

Execute python main.py or double click (only windows users) in the main.py file to run the program. 

Left mouse bottom to make zoom to the plot

Scroll bottom to select region to get the statistics.

Always gives the statistics of the last action.
