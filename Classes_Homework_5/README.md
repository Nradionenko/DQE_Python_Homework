Homework5: News app. Run entire package or __main__.py file
1. PyInputPlus module needs to be installed to run this app: https://pypi.org/project/PyInputPlus/
2. Target file name, as well as all messages and a lot of other stuff is configured in configs.ini file. The file needs to be kept in the same directory as configloader module.
3. Target file will be stored in the same directory where __main__.py file is.
4. To execute the script one can run the Classes_Homework_5 directory in cmd: __main__.py should be picked up by default.
5. No specific text input validation is implemented except for input length.

Homework6: Modules. Run hometask6.py module
The following logic is implemented:
- user can pass path to source file (to read from) in cmd as an argument, i.e. python hometask6.py C:/Users/my_source_file.txt
- if no file path is passed, default path is used, which is path to 'source.txt', located in the same directory as hometask6.py. File name is configured in exec_utils/configs.ini
- file path is then verified: if exists, if is file, if file is not empty, if file.readlines() doesn't throw decode or typerror exceptions. Each issue is checked separately, errors returned. Errors configurable.
- if any of the above criteria is not met, user is asked to input path again. The same checks are performed against his input.
- when valid path is provided, user is asked for number of rows to write from this file. If number of rows > total rows in file, error is thrown
- user can choose how he wants selected rows to be normalized: ignore any potential proper names, leave anything that looks like title or upper as is or provide list of proper names that need to be capitalized irrespective of position in sentence
- selected rows are normalized according to normalization strategy chosen, and are written to the target file (configured in configs.ini)
- message showing how many rows from where to where were written is displayed
- user is asked if he wants to clone the source before deleting. If yes - source is cloned to the same directory, as running module, with name = source_name + current date-time
- source file is deleted.
