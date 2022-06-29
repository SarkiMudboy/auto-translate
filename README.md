# auto-translate
This is an automation script that takes a text file in english and uses the Google translate and DeepL API to translate it to any preffered language.

Installation

# Install pip

You can install pip to ensure you have the latest version. It’s recommended to use the system pip to bootstrap a user installation of pip:

python3 -m pip install --user --upgrade pip

python3 -m pip --version

# Installing virtualenv

virtualenv is used to manage Python packages for different projects. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects. You can install virtualenv using pip.

py -m pip install --user virtualenv

# create a virtual env

To create a virtual environment, go to your project’s directory and run venv. If you are using Python 2, replace venv with virtualenv in the below commands.
py -m venv env

# activate

.\env\Scripts\activate

# run the script

- Type ‘python app.py’. This will run the script and prompt you to enter a file path. This is the 
directory to where the txt file is. (i.e. ‘C:\Users\Abdul\Desktop\resources\tr-texts\BroueTrotsky-all.txt’).

- Next it will prompt you to enter the file language, enter the language.

- After pressing enter, it will display ‘cleaning....’. This means it is cleaning up the text file.

- If successful it will show ‘Your file has been saved at (language).json, ‘language’ here is a 
placeholder for whatever language you entered above i.e. ‘french.json’.

- Next it will show ‘translating...’. This means it has began translating.

- Because the python package version is not very stable, It will have to translate in chunks, if 
success you will see ‘trans_french_01 saved!, trans_french_02 saved!, trans_french_03 saved! 
etc.’ printed, this just means its saving the chunks. You should see these files in the scripts 
directory, If everything runs perfectly the script will not complain.

- The script is set to retry the translation on the affected chunk 4 times before breaking. 
