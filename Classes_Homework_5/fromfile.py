import fileinput
from os import remove
import re
import sqlite3 as sql
import sys

import pyinputplus as pyip

from counts import Counts
from exec_utils.configloader import Config
from modules.combine import Combine
from modules.dates import Dates
from modules.dbconnect import DBconnection
from modules.exceptions import NoSectionsError, NoValue, PastDate, Duplicate, InvalidNumber
import modules.Functions_Strings_Homework4 as s
from modules.file import Files
from modules.input import DateInput
from modules.logging import Log
from modules.run import Execute


cnf = Config()
f = Files()
cnt = Counts(cnf.get_values("PATHS", "target_file"), cnf.get_values("PATHS", "csv_words"), cnf.get_values("PATHS", "csv_letters"))
d = Dates()
e = Execute()
di = DateInput(cnf.get_values("ERRORS", "past_date"),
               cnf.get_values("PATTERNS", "date_format"),
               d.get_current_date())
db = DBconnection(cnf.get_values("PATHS", "db_name"))
lg = Log(cnf.get_values("PATHS", "log_file"))

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

    def check_value(self, label, my_str, start):
        value = self.get_value(my_str, start)
        if value:
            return value
        else:
            raise NoValue(label, start)

    def news_values(self, section):
        """Extract values for News section"""
        n_city = self.check_value(label1, section, city+':')
        n_txt = self.check_value(label1, section, text+':')
        n_date = d.format_date(d.get_current_date(), cnf.get_values("PATTERNS", "date_time_text"))
        return n_city, n_txt, n_date

    def ad_values(self, section):
        """Extract values for Private ad section"""
        a_txt = self.check_value(label2, section, text+':')
        formatted = self.check_value(label2, section, date+':')
        a_date = d.str_to_date(formatted, cnf.get_values("PATTERNS", "date_format"))
        return a_txt, a_date, formatted

    def recipe_values(self, section):
        """Extract values for Recipe section"""
        r_txt = self.check_value(label3, section, text+':')
        r_cal = self.check_value(label3, section, calories+':')
        fit_tip = e.get_fitness_message(r_cal)
        return r_txt, r_cal, fit_tip

    def parse_file(self, sections):
        """Prepare article sections for file. Return section name + attributes for each section to be late used for db"""
        final_text = ''
        values = []
        for section in sections:
            db.create_table(section.split()[0])
            com = Combine(section.split()[0], decor, decor_length)
            if section.split()[0] == label1:
                n_city, n_txt, n_date = self.news_values(section)
                final_text += com.get_news(n_city, n_txt, n_date)+'\n\n'
                values.append([section.split()[0], n_city, n_txt, n_date])
            elif section.split()[0] == label2:
                a_txt, a_date, formatted = self.ad_values(section)
                final_text += com.get_ad(a_txt, a_date, formatted)+'\n\n'
                # check if date is not in the past
                di.raise_if_past(a_date)
                values.append([section.split()[0], a_txt, formatted])
            elif section.split()[0] == label3:
                r_txt, r_cal, fit_tip = self.recipe_values(section)
                final_text += com.get_recipe(r_txt, r_cal, fit_tip)+'\n\n'
                values.append([section.split()[0], r_txt, r_cal, fit_tip])
        return final_text.rstrip(), values

    def write_to_db(self, section):
        """
        Creates tables, inserts values, checks for duplicates, writes logs

        section = list of values for each section in the following order: section label (News etc), section attributes

        """
        db.create_table(section[0])  # first element in section list is section name, like News/Ad/Recipe
        if section[0] == label1:
            try:
                db.go(cnf.get_values("SQL", "insert_news"), (section[1], section[2], section[3]))
            except sql.IntegrityError:
                raise Duplicate(section[0], section[1], section[2])
            except KeyError as err:
                print(err)
        elif section[0] == label2:  # Private ad
            try:
                db.go(cnf.get_values("SQL", "insert_ad"), (section[1], section[2]))
            except sql.IntegrityError:
                raise Duplicate(section[0], section[1], section[2])
            except KeyError as err:
                print(err)
        elif section[0] == label3:  # Recipe
            try:
                db.go(cnf.get_values("SQL", "insert_recipe"), (section[1], section[2], section[3]))
            except sql.IntegrityError:
                raise Duplicate(section[0], section[1], section[2])
            except KeyError as err:
                print(err)

    def raise_if_empty(self, my_str):
        """Verify the string is not empty"""
        if not my_str:
            raise NoSectionsError(section)

    def verify_source(self, source):
        """Open and try to parse and normalize file(s), catch errors, return file path and parsed normalized text"""
        try:
            with fileinput.input(files=source) as fp:
                file_text = []
                for line in fp:
                    file_text.append(line.strip())
            sections = self.get_sections('\n'.join(file_text))
            parsed_text, values = self.parse_file(sections)
            self.raise_if_empty(parsed_text)
            normalized = self.normalize(parsed_text, self.choose_strategy())
            return source, normalized, values
        except UnicodeDecodeError:
            print(cnf.get_values("ERRORS", "cannot_read")+"\n")
            return None, None, None
        except (OSError, NoSectionsError, NoValue, PastDate, InvalidNumber) as err:
            print(err)
            return None, None, None

    def read_source(self, raw_source):
        """If source file returns no errors, return file path and text, else - ask user to input path to source file"""
        proper_source, final_text, db_values = self.verify_source(raw_source)  # check path passed by user/default path first
        inp_request = cnf.get_values("INPUTS", "filepath")
        while not proper_source:  # if any errors occur with initial source, ask user to input another path as long as it doesn't meet the requirements
            inp_path = input(inp_request+"\n")
            proper_source, final_text, db_values = self.verify_source(inp_path)
        else:
            return proper_source, final_text, db_values

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
        f.append_file(formatted_text, self.target)
        lg.write_log(cnf.get_values("MESSAGES", "file_write").format(txt=formatted_text, src=source))

    def remove(self, proper_source):
        """Remove and print info message"""
        if proper_source != self.def_source:  # don't delete default source file
            if isinstance(proper_source, list):
                for file in proper_source:
                    remove(file)
            else:
                remove(proper_source)
            lg.write_log(cnf.get_values("MESSAGES", "delete_success") % proper_source)

    def file_full_flow(self, raw_source):
        proper_source, normalized_text, db_values = self.read_source(raw_source)
        self.write(normalized_text, proper_source)
        self.remove(proper_source)
        for section in db_values:
            try:
                self.write_to_db(section)
                lg.write_log(cnf.get_values("MESSAGES", "db_write").format
                             (s=section[0], t=section[0].lower(), v1=section[1], v2=section[2], src=proper_source))
            except (sql.DatabaseError, Duplicate, KeyError) as err:
                print(err)
        db.curs.close()


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "source_file")
    default_target = cnf.get_values("PATHS", "target_file")
    wff = WriteFromFile(default_source, default_target)
    raw_source = wff.get_raw_source()
    wff.file_full_flow(raw_source)
    cnt.write_csv()
