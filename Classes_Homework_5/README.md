Homework5: News app. Run entire package or __main__.py file
1. PyInputPlus module needs to be installed to run this app: https://pypi.org/project/PyInputPlus/
2. Target file name, as well as all messages and a lot of other stuff is configured in configs.ini file. The file needs to be kept in the same directory as configloader module.
3. Target file will be stored in /Classes_Homework_5 file is.
4. To execute the script one can run the Classes_Homework_5 directory in cmd: __main__.py should be picked up by default.
5. No specific text input validation is implemented except for input length.
UPDATE: Running main.py you can select whether you want to input manually or from file. If manually - the above described steps will be used, if from file - module from hometask6 is used, but in this case you can't pass multiple files at a time

Homework6: Modules. Run fromfile.py module
The following logic is implemented:
- user can pass path to source file(s) (to read from) in cmd as an argument, i.e. python fromfile.py C:/Users/my_source_file.txt
- if no file path is passed, default path is used, which is path to 'source.txt', located in the same directory as hometask6.py. File name is configured in exec_utils/configs.ini
- file path is then verified: if exists, if is file, if file is not empty, if can be decoded
- if any of the above criteria is not met, user is asked to input path again. The same checks are performed against his input.
- when valid path is provided, user is asked to decide what normalization strategy to apply: ignore any potential proper names, leave anything that looks like title or upper as is or provide list of proper names that need to be capitalized irrespective of position in sentence
- text from source file(s) is normalized according to normalization strategy chosen, and are written to the target file (configured in configs.ini)
- source is cloned to the same directory, as running module, with name = source_name + _clone
- source file is deleted.
