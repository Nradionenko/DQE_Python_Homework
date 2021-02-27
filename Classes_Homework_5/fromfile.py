import sys
import fileinput
from os import remove

import pyinputplus as pyip

import modules.Functions_Strings_Homework4 as s
from modules.file import Files
from exec_utils.configloader import Config


cnf = Config()
f = Files()


class WriteFromFile:
    def __init__(self, default_source, target_file):
        self.def_source = f.get_path(default_source)
        self.target = target_file

    def get_raw_source(self):
        """Get source path(s) from arguments passed, if none - use default"""
        files = sys.argv[1:]
        if not files:
            source = self.def_source
        else:
            source = files
        return source

    def choose_strategy(self):
        """Choose strategy for normalization to handle possible proper names (like London, Government etc):
        Option 1: capitalize text ignoring any potential proper names (this will turn London to london, for example)
        Option 2: don't touch anything that is capitalized or upper in source text, assuming these are proper names
        """
        choice1 = cnf.get_values("LABELS", "capital_all")
        choice2 = cnf.get_values("LABELS", "keep_titles")
        strategy = pyip.inputMenu(prompt=cnf.get_values("INPUTS", "normalize_strategy")+"\n",
                                  choices=[choice1, choice2],
                                  numbered=True
                                  )
        return strategy

    def normalize(self, text, strategy):
        """Normalize text based on selected strategy"""
        patt1 = cnf.get_values("PATTERNS", "split_text")
        if strategy == cnf.get_values("LABELS", "capital_all"):
            my_text = text.lower()
        elif strategy == cnf.get_values("LABELS", "keep_titles"):
            my_text = s.keep_titles(text)  # method from Functions strings module
        return s.capital_first(my_text, patt1)  # method from Functions strings module

    def verify_source(self, source):
        """Open and file(s), catch errors, return file path and text"""
        try:
            with fileinput.input(files=source) as fp:
                strategy = self.choose_strategy()
                text = []
                for line in fp:
                    text.append(self.normalize(line, strategy).strip())
                return source, '\n'.join(text)
        except UnicodeDecodeError:
            print(cnf.get_values("ERRORS", "cannot_read")+"\n")
            return None, None
        except OSError as err:
            print(err)
            return None, None

    def read_source(self, raw_source):
        """If source file returns no errors, return file path and text, else - ask user to input path to source file"""
        proper_source, result = self.verify_source(raw_source)  # check parsed/default path
        inp_request = cnf.get_values("INPUTS", "filepath")
        while not proper_source:
            inp_path = input(inp_request+"\n")
            proper_source, result = self.read_source(inp_path)
        else:
            return proper_source, result

    def write(self, text, source):
        """Write normalized text to target file. Print info message."""
        try:
            f.append_file(text, self.target)
            print(cnf.get_values("MESSAGES", "write_success") % (source, f.get_path(self.target)))
        except Exception as e:
            print("Couldn't write to target file.")
            print(e)

    def remove(self, proper_source):
        """Remove and print info message"""
        if proper_source != self.def_source:  # don't delete default source file
            if type(proper_source) is list:
                for file in proper_source:
                    remove(file)
            else:
                remove(proper_source)
            print(cnf.get_values("MESSAGES", "delete_success") % (proper_source))

    def file_full_flow(self):
        raw_source = self.get_raw_source()
        proper_source, text = self.read_source(raw_source)
        self.write(text, proper_source)
        self.remove(proper_source)


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "source_file")
    default_target = cnf.get_values("PATHS", "target_file")
    wff = WriteFromFile(default_source, default_target)
    wff.file_full_flow()
