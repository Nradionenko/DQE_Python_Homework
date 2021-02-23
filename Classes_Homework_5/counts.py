from collections import Counter
import csv
from exec_utils.configloader import Config
from re import findall
from modules.file import Files

cnf = Config()
f = Files()


class Counts:
    def __init__(self, count_in_file, words_csv, letters_csv):
        self.source = count_in_file  # use this file as source for counts
        self.words_csv = words_csv
        self.letters_csv = letters_csv

    def get_text(self):
        """Open and read file"""
        path = f.get_path(self.source)
        with open(path, "r", encoding="utf-8") as file:
            my_text = file.read()
        return my_text

    def words(self):
        """Split text into words"""
        text = self.get_text()
        words_list = findall(r'\b[\w\']+\b', text.lower())
        return words_list

    def words_count(self):
        """Count words occurrence in list"""
        words_list = self.words()
        words_count = Counter(words_list).most_common()
        return words_count

    def letters(self):
        """Take string and create list of all letters (lower everything) and list of upper letters"""
        letters = [i for i in self.get_text() if i.isalpha()]
        all_lower = [char.lower() for char in letters if char.isalpha()]
        upper_letters = [char for char in letters if char.isupper() and char.isalpha()]
        return all_lower, upper_letters

    def letters_counts(self):
        """Count letters occurrence in list: return count of any occurrence, upper occurrence and total letters in list."""
        all_lower, upper_letters = self.letters()
        count_lower, count_upper = Counter(all_lower), Counter(upper_letters)
        total = sum(count_lower.values())
        return count_lower, count_upper, total

    def dicts_by_letter_counts(self):
        """"Create list of dictionaries, where keys: letter, total count, upper count and % of all letters. Headers configurable."""
        count_all, count_upper, total = self.letters_counts()
        letter, all, upper, perc = cnf.get_values("HEADERS", "letter"), cnf.get_values("HEADERS", "total"), cnf.get_values("HEADERS", "upper"), cnf.get_values("HEADERS", "perc")
        my_list = []
        for char in count_all.keys():  # for every letter in text
            if char.upper() not in count_upper.keys():  # if upper version of this letter doesn't exist
                my_list.append({letter: char,
                                all: count_all[char],
                                upper: 0,
                                perc: str(round(count_all[char]*100/total,2))+'%'
                                })
            else:
                for upper_char in count_upper.keys():
                    if char.upper() == upper_char:
                        my_list.append({letter: char,
                                        all: count_all[char],
                                        upper: count_upper[upper_char],
                                        perc: str(round(count_all[char]*100/total,2))+'%'
                                        })
        sorted_list = sorted(my_list, key=lambda k: k['perc'], reverse=True)
        return sorted_list

    def write_csv(self):
        """"Write 2 csvs: from words and from letters. In letters: take dict keys as headers"""
        words_dict = self.words_count()
        list_of_letter_dicts = self.dicts_by_letter_counts()
        words_file_path, letters_file_path = f.get_path(self.words_csv), f.get_path(self.letters_csv)
        with open(words_file_path, 'w+', newline='', encoding="utf-8") as words_csv, \
                open(letters_file_path,'w+', newline='', encoding="utf-8") as letters_csv:
            words_writer = csv.writer(words_csv, delimiter='-')
            for word in words_dict:
                words_writer.writerow(word)
            letters_writer = csv.DictWriter(letters_csv, delimiter=',', fieldnames=list_of_letter_dicts[0].keys())  # column headers = keys from first dict in list
            letters_writer.writeheader()
            for dict in list_of_letter_dicts:
                letters_writer.writerow(dict)


if __name__ == "__main__":
    c = Counts(cnf.get_values("PATHS", "target_file"), cnf.get_values("PATHS", "csv_words"), cnf.get_values("PATHS", "csv_letters"))
    c.write_csv()
