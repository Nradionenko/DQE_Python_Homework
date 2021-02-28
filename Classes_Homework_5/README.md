Homework5: News app. Run entire package or __main__.py file
1. PyInputPlus module needs to be installed to run this app: https://pypi.org/project/PyInputPlus/
2. Target file name, as well as all messages and a lot of other stuff is configured in configs.ini file. The file needs to be kept in the same directory as configloader module.
3. Target file as all other files (except config) will be stored in /Classes_Homework_5/files folder.
4. To execute the script one can run the Classes_Homework_5 directory in cmd: __main__.py should be picked up by default.
5. No specific text input validation is implemented except for input length.
UPDATE: Running main.py you can select whether you want to input manually, from text file of from json. If manually - the above described steps will be used, if from file - module from hometask6 is used, but in this case you can't pass multiple files at a time

Homework6: Modules. Run fromfile.py + pass file(s) in cmd OR main.py and select "Write from file" on the first step (in this case default source is used)
The following logic is implemented:
- user can pass path to source file(s) (to read from) in cmd as an argument, i.e. python fromfile.py C:/Users/my_source_file.txt
- if no file path is passed, default path is used, which is path to 'source_text.txt', located in the /Classes_Homework_5/files. File name is configured in exec_utils/configs.ini
- file path is then verified: in any exceptions caught, user is asked to provide valid file path manually. The same checks are performed against his input.
- when valid path is provided, user is asked to decide what normalization strategy to apply: ignore any potential proper names or leave anything that looks like title
irrespective of position in sentence, i.e. 'I live in London' will be set to 'I live in london' in first case and to 'I live in London' in second.
- text from source file(s) is normalized according to normalization strategy chosen, and are written to the target file (configured in configs.ini)
- source file is deleted (unless source is default source).

Homework7: CSV. Run 'counts.py' module OR main.py (in the latter case you'll have to run the entire flow)
- You can configure target csv file names in congigs.ini
- By default, csv files will be written to /Classes_Homework_5/files.
- In 'words count' all alphanumeric characters separated by non-alphanumeric (except apostrophe and underscore, so "it's" is 1 words, as well as "my_file") are considered words, i.e. 20/02/2021 will be treated as 3 words. If this needs to be changed, please let me know.
- In 'letters count' only alphabetic characters are counted. Digits and special characters are ignored as they don't have upper case anyway.
- Both lists are sorted descending.

Homework8: JSON. Run fromjson.py + pass json path in cmd OR main.py and select "Write from json" on the first step:
- user can pass path to json file in cmd when running module (only 1 file expected), if no path  - default path is used (configured in configs.ini). Default json is in /Classes_Homework_5/files
- json is validated against schema.json (see in /Classes_Homework_5/files)
- if json is not valid or an file errors occur, user is asked to provide path to another json (until user provides proper file)
- json is parsed, values normalized, data formatted and then written to target file
- source file is removed (unless default)
