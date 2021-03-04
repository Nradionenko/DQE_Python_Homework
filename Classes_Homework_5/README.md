Homework5: News app. Run entire package or __main__.py file
1. Target file name, as well as all messages and a lot of other stuff is configured in configs.ini file. The file needs to be kept in the same directory as configloader module.
3. Target file as all other files (except config) will be stored in /Classes_Homework_5/files folder.
4. No specific text input validation is implemented except for input length.
UPDATE: Running main.py you can select whether you want to input manually, from text file of from json. If manually - the above described steps will be used, if from file - module from hometask6 is used, but in this case you can't pass multiple files at a time

Homework6: Modules. Run fromfile.py + pass file(s) in cmd OR run main.py and select "Write from file" on the first step
The following logic is implemented:
- user can pass one or multiple files when running the module
- if no files are passed, default path is used
- each of these files is validated whether it exists and can be read + whether is can be parsed according to expected keywords in text
- if any of the files fail validation, user is asked to provide alternative filepath manually until he provides a file that meets all requirements
- file(s) are parsed to extract values for article sections, sections are combined, text is normalized
- text is written to target file, source file(s) removed, unless default file was used as source.

Homework7: CSV. Run 'counts.py' module OR main.py (in the latter case you'll have to run the entire flow)
- You can configure target csv file names in congigs.ini
- By default, csv files will be written to /Classes_Homework_5/files.
- In 'words count' all alphanumeric characters separated by non-alphanumeric (except apostrophe and underscore, so "it's" is 1 words, as well as "my_file") are considered words, i.e. 20/02/2021 will be treated as 3 words. If this needs to be changed, please let me know.
- In 'letters count' only alphabetic characters are counted. Digits and special characters are ignored as they don't have upper case anyway.
- Both lists are sorted descending.

Homework8: JSON. Run fromjson.py + pass json path in cmd OR main.py and select "Write from json" on the first step:
- user can provide path to json file in cmd when running module (only 1 file expected), if no path  - default path is used (configured in configs.ini). Default json is in /Classes_Homework_5/files
- json is validated against schema.json (see in /Classes_Homework_5/files)
- if json is not valid or any file errors occur, user is asked to provide path to another json (until user provides proper file)
- json is parsed, values normalized, data formatted and then written to target file
- source file is removed (unless default)

Homework9: XML. Run fromxml.py + pass xml path in cmd OR main.py and select "Write from xml" on the first step
Key methods inherited from FromJson, basic logic is the same
