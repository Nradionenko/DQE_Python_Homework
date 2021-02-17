from os.path import exists, isfile, getsize, splitext, basename
from re import split
from os import remove
from argparse import ArgumentParser as ap
import pyinputplus as pyip
import shutil
import datetime
import modules.Functions_Strings_Homework4 as s
from modules.file import Files
from exec_utils.configloader import Config


cnf = Config()
f = Files()


class WriteFromFile:
    def __init__(self, default_source, target_file):
        self.def_source = default_source
        self.target = target_file

    def parse_arguments(self):
        """Parse cmd argument. We expect user to provide path to source file to read from. If not provided, use default"""
        default_path = f.get_path(self.def_source)
        parser = ap(description='Provide full path to the source file.')
        parser.add_argument('path', nargs='?', const=1,
                            default=default_path,
                            help='full path to the source file')
        raw_source = parser.parse_args().path
        return raw_source

    def read_lines(self, user_path):
        """Open file, read line by line, return lines, close file"""
        with open(user_path, "r", encoding="utf-8") as file:
            rows = file.readlines()
            return rows

    def try_reading(self, user_path):
        """Return rows read from file OR print error message in case of exceptions"""
        read_err = cnf.get_values("ERRORS", "cannot_read")
        try:
            rows = self.read_lines(user_path)
            return rows
        except (UnicodeDecodeError, TypeError):
            print(read_err+"\n")

    def check_path(self, user_path):
        """Verify if path exists, isfile, is not empty and if it can be read. Errors configured in configs.ini"""
        err1, err2, err3 = cnf.get_values("ERRORS", "nonexist"), cnf.get_values("ERRORS", "nonfile"), cnf.get_values("ERRORS", "empty")
        if not exists(user_path):
            print(err1+"\n")
            return exists(user_path)
        elif not isfile(user_path):
            print(err2+"\n")
            return isfile(user_path)
        elif getsize(user_path) == 0:
            print(err3+"\n")
            return False
        else:
            rows_exist = self.try_reading(user_path)
            if rows_exist:
                return user_path, rows_exist
            else:
                return False

    def read_source_path(self):
        """If path provided as argument/default is not valid/is empty/is not readable, ask user to input another path"""
        raw_path = self.parse_arguments()
        inp_request = cnf.get_values("INPUTS", "filepath")
        proper_path = self.check_path(raw_path)  # check parsed/default path
        while not proper_path:
            inp_path = input(inp_request+"\n")
            proper_path = self.check_path(inp_path)
        else:
            return proper_path[0], proper_path[1]  # [0] - path, [1] - rows

    def text_by_rows(self, rows, cnt):
        """Return as many rows from text(=rows) as passed in arguments. Join rows into text"""
        selection = []
        for i in range(cnt):
            selection.append(rows[i])
        text = ''.join(selection)
        return text

    def prepare_text(self):
        """Ask user how many rows he wants to read and write, min 1 row. If rows provided > total rows - throw error, repeat."""
        user_path, rows = self.read_source_path()
        inp_request = cnf.get_values("INPUTS", "rows")
        error_msg = cnf.get_values("ERRORS", "maxlength")
        rows_in_range = False
        while not rows_in_range:
            try:
                cnt_rows_selected = pyip.inputInt(prompt=inp_request+"\n", min=1)
                raw_text = self.text_by_rows(rows, cnt_rows_selected)
                rows_in_range = True
                return user_path, raw_text, cnt_rows_selected
            except IndexError:
                print(error_msg+' '+f"{len(rows)}.\n")
                continue

    def normalize(self, text):
        """Ask user to select normalization strategy. Return normalized text"""
        choice1, choice2, choice3 = cnf.get_values("LABELS", "capital_all"), cnf.get_values("LABELS", "keep_titles"), cnf.get_values("LABELS", "keep_custom")
        patt1 = cnf.get_values("PATTERNS", "split_text")
        patt2 = cnf.get_values("PATTERNS", "split_sentence")
        patt3 = cnf.get_values("PATTERNS", "split_input")
        strategy = pyip.inputMenu(prompt=cnf.get_values("INPUTS", "normalize_strategy")+"\n",
                             choices=[choice1, choice2, choice3],
                             numbered=True)
        sentences = split(patt1, text)
        if strategy == choice1:
            result = s.capitalize_all(sentences)
        elif strategy == choice2:
            result = s.ignore_titles(sentences, patt2)
        elif strategy == choice3:
            user_names = pyip.inputStr(cnf.get_values("INPUTS", "proper_names")+"\n")
            proper_names = split(patt3, user_names)
            result = s.capitalize_custom(sentences, proper_names, patt2)
        return result

    def write(self):
        """Write normalized text to target file. Print info message to user with rows writeen source and target files."""
        success_msg = cnf.get_values("MESSAGES", "write_success")
        user_path, raw_text, cnt_rows_selected = self.prepare_text()
        fixed_text = self.normalize(raw_text)
        f.write_file(fixed_text, self.target)
        print(str(cnt_rows_selected)+' '+success_msg+' '+user_path+"\n")
        return user_path

    def end_to_end(self):
        """Run all steps, ask user if he'd like to clone the source file before deleting (if yes - clone with datetime to the same directory as this file). Remove the source file, print out message."""
        user_path = self.write()
        inp_msg = cnf.get_values("INPUTS", "clone_file")
        clone_msg = cnf.get_values("MESSAGES", "clone_success")
        delete_msg = cnf.get_values("MESSAGES", "delete_success")
        pyip.inputYesNo(inp_msg+"\n")
        if "yes":
            current_date = datetime.datetime.today().strftime(cnf.get_values("PATTERNS", "date_time_name"))
            source_name, source_ext = splitext(basename(user_path))
            cloned_name = source_name+'_'+str(current_date)+source_ext
            cloned_path = f.get_path(cloned_name)
            shutil.copyfile(user_path, cloned_path)
            print(clone_msg+" "+cloned_path+"\n")
        remove(user_path)
        print(user_path+" "+delete_msg)


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "source_file")
    default_target = cnf.get_values("PATHS", "target_file")
    wff = WriteFromFile(default_source, default_target)
    wff.end_to_end()
