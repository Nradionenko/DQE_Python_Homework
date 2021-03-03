import sys
import fileinput
import re
from os import remove

import pyinputplus as pyip

import modules.Functions_Strings_Homework4 as s
from modules.file import Files
from modules.combine import Combine
from modules.dates import Dates
from modules.input import DateInput
from exec_utils.configloader import Config

cnf = Config()
f = Files()
d = Dates()
di = DateInput(cnf.get_values("ERRORS", "past_date"),
               cnf.get_values("PATTERNS", "date_format"),
               d.get_current_date())
decor, decor_length = cnf.get_values("RESTRICTIONS", "n"), \
                      cnf.get_values("RESTRICTIONS", "count_n")
# property names (the same as in JSON)
section, city, text, date, calories = cnf.get_values("PROPERTIES", "label"), \
                                      cnf.get_values("PROPERTIES", "city"), \
                                      cnf.get_values("PROPERTIES", "text"), \
                                      cnf.get_values("PROPERTIES", "date"), \
                                      cnf.get_values("PROPERTIES", "kcal")
# names of sections (the same as for manual input and JSON)
label1, label2, label3 = cnf.get_values("LABELS", "news_label"), \
                         cnf.get_values("LABELS", "ad_label"), \
                         cnf.get_values("LABELS", "recipe_label")


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

    def get_sections(self, file_text):
        """Split text into sections (by sectionLabel word), returns list of sections"""
        sections = [i for i in (re.split(section+r':\s', file_text)) if i]
        return sections

    def get_properties(self, my_str):
        """Find properties in section and create a list of them in order of appearance"""
        properties = list(map(lambda x: x+':', [city, text, date, calories]))
        sorted_prop = [i for i in my_str.split() if i in properties]  # list of properties in order of occurrence
        return sorted_prop

    def get_value(self, my_str, start):
        """Get value by property name and ending"""
        sorted_properties = self.get_properties(my_str)
        if start == sorted_properties[-1]:  # if property is the last in the section
            value = my_str[my_str.find(start)+len(start):]  # find value right after property name
        else:
            end = sorted_properties[sorted_properties.index(start)+1]  # end = next property
            value = my_str[my_str.find(start)+len(start):my_str.find(end)]  # find value between property name and next property name
        return value.strip()

    def parse_file(self, file_text):
        sections = self.get_sections(file_text)  # split text into sections (by Section keyword)
        final_text = ''
        for section in sections:
            com = Combine(section.split()[0], decor, decor_length)
            if section.split()[0] == label1:
                news_city = self.get_value(section, city+':')
                news_text = self.get_value(section, text+':')
                final_text += com.get_news(news_city, news_text)+'\n\n'
            elif section.split()[0] == label2:
                ad_text = self.get_value(section, text+':')
                # convert date passed as string to datetime.date
                ad_date = d.str_to_date(self.get_value(section, date+':'), cnf.get_values("PATTERNS", "date_format"))
                # check if date is not in the past
                di.raise_if_past(ad_date)
                final_text += com.get_ad(ad_text, ad_date)+'\n\n'
            elif section.split()[0] == label3:
                rec_text = self.get_value(section, text+':')
                rec_calories = self.get_value(section, calories+':')
                final_text += com.get_recipe(rec_text, rec_calories)+'\n\n'
        return final_text.rstrip()

    def raise_if_empty(self, my_str):
        """Verify the string is not empty"""
        if not my_str:
            raise OSError(cnf.get_values("ERRORS", "empty"))

    def verify_source(self, source):
        """Open and try to parse file(s), catch errors, return file path and text"""
        try:
            with fileinput.input(files=source) as fp:
                file_text = []
                for line in fp:
                    file_text.append(line.strip())
            parsed_text = self.parse_file('\n'.join(file_text))
            self.raise_if_empty(parsed_text)
            return source, parsed_text
        except UnicodeDecodeError:
            print(cnf.get_values("ERRORS", "cannot_read")+"\n")
            return None, None
        except (OSError, ValueError) as err:
            print(err)
            return None, None

    def read_source(self, raw_source):
        """If source file returns no errors, return file path and text, else - ask user to input path to source file"""
        proper_source, result = self.verify_source(raw_source)  # check path passed by user/default path first
        inp_request = cnf.get_values("INPUTS", "filepath")
        while not proper_source:  # if any errors occur with initial source, ask user to input another path as long as it doesn't meet the requirements
            inp_path = input(inp_request+"\n")
            proper_source, result = self.verify_source(inp_path)
        else:
            return proper_source, result

    def choose_strategy(self):
        """Choose strategy for normalization to handle possible proper names (like London, Government etc):
        Option 1: capitalize text ignoring any potential proper names (this will turn London to london, for example)
        Option 2: don't touch anything that is capitalized in source text, assuming these are proper names
        """
        choice1 = cnf.get_values("LABELS", "capital_all")
        choice2 = cnf.get_values("LABELS", "keep_titles")
        strategy = pyip.inputMenu(prompt=cnf.get_values("INPUTS", "normalize_strategy")+"\n",
                                  choices=[choice1, choice2],
                                  numbered=True
                                  )
        return strategy

    def normalize(self, parsed_text, strategy):
        """Normalize text based on selected strategy"""
        patt1 = cnf.get_values("PATTERNS", "split_text")
        if strategy == cnf.get_values("LABELS", "capital_all"):
            my_text = parsed_text.lower()
        elif strategy == cnf.get_values("LABELS", "keep_titles"):
            my_text = s.keep_titles(parsed_text)  # method from Functions strings module
        return s.capital_first(my_text, patt1)  # method from Functions strings module

    def write(self, formatted_text, source):
        """Write normalized text to target file. Print info message."""
        try:
            f.append_file(formatted_text, self.target)
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

    def file_full_flow(self, raw_source):
        proper_source, parsed_text = self.read_source(raw_source)
        normalized_text = self.normalize(parsed_text, self.choose_strategy())
        self.write(normalized_text, proper_source)
        self.remove(proper_source)


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "source_file")
    default_target = cnf.get_values("PATHS", "target_file")
    wff = WriteFromFile(default_source, default_target)
    raw_source = wff.get_raw_source()
    wff.file_full_flow(raw_source)
    # source, text = wff.verify_source(raw_source)
    # print(text)
    # print(wff.get_sections(text))

# with open(r'C:\Users\Nadiia_Radionenko\PycharmProjects\DQE_Python_Course\Classes_Homework_5\files\source_text.txt', "r") as f:
#     reader = f.read()
#     # print(reader)
#
# sections = wff.get_sections(text)
# # print(sections)
# properties = list(map(lambda x: x+':', [city, text, date, calories]))
# print([city, text, date, calories])
# for i in sections:
#     # print(i)
#     # print(wff.get_properties(i))
#     if i.split()[0] == 'Recipe':
#         # print(i)
#         properties = list(map(lambda x: x+':', [city, text, date, calories]))
#         print(properties)
        # sorted_prop = [i for i in my_str.split() if i in properties]
        # print(wff.get_properties(i))
        # print(wff.get_value(i, calories+':'))
    # print('---')
