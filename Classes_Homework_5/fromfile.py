import sys
import fileinput
from os import path, remove
from re import split
from shutil import copy

import pyinputplus as pyip

import modules.Functions_Strings_Homework4 as s
from modules.file import Files
from exec_utils.configloader import Config


cnf = Config()
f = Files()


class WriteFromFile:
    def __init__(self, default_source, target_file):
        self.def_source = default_source
        self.target = target_file

    def get_raw_source(self):
        """Get source path(s) from arguments passed, if none - use default"""
        files = sys.argv[1:]
        default = f.get_path(self.def_source)
        if not files:
            source = default
        else:
            source = files
        return source

    def read_source(self, source):
        """Read file(s), catch errors, return file path and text"""
        with fileinput.input(files=source, openhook=fileinput.hook_encoded("utf-8")) as fp:
            try:
                text = []
                for line in fp:
                    if fp.isfirstline() and fp.lineno() > 1:
                        text.append('\n'+line.strip())
                    else:
                        text.append(line.strip())
                if not text:
                    print(cnf.get_values("ERRORS", "empty")+"\n")
                    return None, None
                else:
                    result = '\n'.join(text)
                    return source, result
            except UnicodeDecodeError:
                print(cnf.get_values("ERRORS", "cannot_read")+"\n")
                return None, None
            except (FileNotFoundError, OSError) as err:
                print(err)
                return None, None

    def verify_source(self):
        """If source file returns no errors, return file path and text, else - ask user to input path to source file"""
        raw_source = self.get_raw_source()
        proper_source, result = self.read_source(raw_source)  # check parsed/default path
        inp_request = cnf.get_values("INPUTS", "filepath")
        while not proper_source:
            inp_path = input(inp_request+"\n")
            proper_source, result = self.read_source(inp_path)
        else:
            return proper_source, result

    def choose_strategy(self):
        """Choose strategy for normalization to handle possible proper names (like London, Government etc):
        Option 1: capitalize text ignoring any potential proper names (this will turn London to london, for example)
        Option 2: don't touch anything that is capitalized or upper in source text, assuming these are proper names
        Option 3: ask user to provide list of words which will be capitalized irrespective of their position in sentence
        """
        choice1 = cnf.get_values("LABELS", "capital_all")
        choice2 = cnf.get_values("LABELS", "keep_titles")
        choice3 = cnf.get_values("LABELS", "keep_custom")
        strategy = pyip.inputMenu(prompt=cnf.get_values("INPUTS", "normalize_strategy")+"\n",
                                  choices=[choice1, choice2, choice3],
                                  numbered=True
                                  )
        return strategy

    def normalize(self, text):
        """Normalize text based on selected strategy"""
        strategy = self.choose_strategy()
        patt1 = cnf.get_values("PATTERNS", "split_text")
        patt2 = cnf.get_values("PATTERNS", "split_input")
        if strategy == cnf.get_values("LABELS", "capital_all"):
            my_text = text.lower()
        elif strategy == cnf.get_values("LABELS", "keep_titles"):
            my_text = s.keep_titles(text)
        elif strategy == cnf.get_values("LABELS", "keep_custom"):
            user_propers = pyip.inputStr(cnf.get_values("INPUTS", "proper_names")+"\n")
            titles = split(patt2, user_propers)
            my_text = s.keep_custom(text, titles)
        return s.capital_first(my_text, patt1)

    def clone(self, file):
        """Clone file to the same directory it exists in with '_clone' added to the name"""
        file_name, file_ext = path.splitext(path.basename(file))
        clone_path = path.join(path.dirname(file),file_name+"_clone"+file_ext)
        copy(file, clone_path)
        return clone_path

    def write_and_remove(self):
        """Write normalized text to target file. Print info message. Clone source file and then remove."""
        proper_source, text = self.verify_source()
        fixed_text = self.normalize(text)
        f.write_file(fixed_text, self.target)
        if type(proper_source) is list:
            clone_path = []
            for file in proper_source:
                clone_path.append(self.clone(file))
                remove(file)
        else:
            clone_path = self.clone(proper_source)
            remove(proper_source)
        print(cnf.get_values("MESSAGES", "write_success") % (f.get_path(self.target), proper_source))
        print(cnf.get_values("MESSAGES", "delete_success") % (proper_source, clone_path))


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "source_file")
    default_target = cnf.get_values("PATHS", "target_file")
    wff = WriteFromFile(default_source, default_target)
    wff.write_and_remove()
