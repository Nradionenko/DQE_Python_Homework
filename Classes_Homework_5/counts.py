from collections import Counter, defaultdict
import csv
from exec_utils.configloader import Config
from re import findall
from modules.file import Files

cnf = Config()
f = Files()


class Counts:
    def __init__(self, count_in_file, words_csv, letters_csv):
        self.source = count_in_file
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
        chars = [i for i in self.get_text() if i.isalpha()]
        all_letters = [char.lower() for char in chars if char.isalpha()]
        upper_letters = [char for char in chars if char.isupper() and char.isalpha()]
        return all_letters, upper_letters

    def letters_counts(self):
        """Count letters occurrence in list: return count of any occurrence, upper occurrence and total letters in list."""
        all_letters, upper_letters = self.letters()
        count_all, count_upper = Counter(all_letters), Counter(upper_letters)
        total = sum(count_all.values())
        return count_all, count_upper, total

    def dicts_by_letter_counts(self):
        """"Create list of dictionaries, where keys: letter, total count, upper count and % of all letters. Headers configurable."""
        count_all, count_upper, total = self.letters_counts()
        letter, tot, upper, perc = cnf.get_values("HEADERS", "letter"), cnf.get_values("HEADERS", "total"), cnf.get_values("HEADERS", "upper"), cnf.get_values("HEADERS", "perc")
        my_list = []
        for char in count_all.keys():
            if char.upper() not in count_upper.keys():
                my_list.append({letter: char,
                                tot: count_all[char],
                                upper: 0,
                                perc: str(round(count_all[char]*100/total,2))+'%'
                                })
            else:
                for upper_char in count_upper.keys():
                    if char.upper() == upper_char:
                        my_list.append({letter: char,
                                        tot: count_all[char],
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
        with open(words_file_path, 'w+', newline='', encoding="utf-8") as csv1, \
                open(letters_file_path,'w+', newline='', encoding="utf-8") as csv2:
            writer1 = csv.writer(csv1, delimiter='-')
            for word in words_dict:
                writer1.writerow(word)
            writer2 = csv.DictWriter(csv2, delimiter=',', fieldnames=list_of_letter_dicts[0].keys())  # column headers = keys from first dict in list
            writer2.writeheader()
            for dict in list_of_letter_dicts:
                writer2.writerow(dict)


if __name__=="__main__":
    c = Counts(cnf.get_values("PATHS", "target_file"), cnf.get_values("PATHS", "csv_words"), cnf.get_values("PATHS", "csv_letters"))
    c.write_csv()
