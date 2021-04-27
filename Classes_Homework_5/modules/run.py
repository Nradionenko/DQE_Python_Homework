import sqlite3 as sql

from exec_utils.configloader import Config
from modules.input import Selection, TextInput, DateInput, IntInput
from modules.dates import Dates
from modules.file import Files
from modules.combine import Combine
from modules.dbconnect import DBconnection
from modules.exceptions import Duplicate, PastDate, InvalidNumber
from modules.logging import Log

cnf = Config()
s = Selection()
f = Files()
d = Dates()
t = TextInput(cnf.get_values("ERRORS", "long_text"),
              cnf.get_values("RESTRICTIONS", "max_size"))
di = DateInput(cnf.get_values("ERRORS", "past_date"),
               cnf.get_values("PATTERNS", "date_format"),
               d.get_current_date())
ii = IntInput(cnf.get_values("RESTRICTIONS", "cal_min"))
lg = Log(cnf.get_values("PATHS", "log_file"))

label1, label2, label3 = cnf.get_values("LABELS", "news_label"), \
                         cnf.get_values("LABELS", "ad_label"), \
                         cnf.get_values("LABELS", "recipe_label")
decor, decor_length = cnf.get_values("RESTRICTIONS", "n"), \
                      cnf.get_values("RESTRICTIONS", "count_n")


class Execute:
    def news_values(self):
        """Pick values for news section"""
        n_city = t.ask_for_text(cnf.get_values("INPUTS", "city_msg")).strip().capitalize()
        n_txt = t.ask_for_text(cnf.get_values("INPUTS", "news_msg")).strip().capitalize()
        n_date = d.format_date(d.get_current_date(), cnf.get_values("PATTERNS", "date_time_text"))
        return n_city, n_txt, n_date

    def ad_values(self):
        """Pick values for Private ad section"""
        a_txt = t.ask_for_text(cnf.get_values("INPUTS", "ad_msg")).strip().capitalize()
        a_date = di.ask_for_date(cnf.get_values("INPUTS", "ad_date"))
        date_format = cnf.get_values("PATTERNS", "date_format")
        formatted = d.format_date(a_date, date_format)
        return a_txt, a_date, formatted

    def get_fitness_message(self, user_num):
        """Generates app message for random section (recipes) based on values
        provided (based on calories of the recipe).
        Min, max values as well as messages are configurable.
        """
        fitness_tip1 = cnf.get_values("MESSAGES", "fitness1")
        fitness_tip2 = cnf.get_values("MESSAGES", "fitness2")
        fitness_tip3 = cnf.get_values("MESSAGES", "fitness3")
        try:
            if int(user_num) == int(cnf.get_values("RESTRICTIONS","cal_min")):
                summary = fitness_tip1
            elif int(user_num) < int(cnf.get_values("RESTRICTIONS","cal_max")):
                summary = fitness_tip2
            else:
                summary = fitness_tip3
            return summary
        except ValueError:
            raise InvalidNumber(label3, user_num)

    def recipe_values(self):
        """Pick values for Recipe section"""
        r_txt = t.ask_for_text(cnf.get_values("INPUTS", "recipe_msg")).strip().capitalize()
        r_cal = ii.ask_for_int(cnf.get_values("INPUTS", "recipe_calories"))
        fit_tip = self.get_fitness_message(r_cal)
        return r_txt, r_cal, fit_tip

    def prepare_for_file(self):
        """Ask user for selection. Combine values within each section for file + insert to db
        """
        selection = s.ask_for_selection(label1, label2, label3)
        com = Combine(selection, decor, decor_length)
        if selection == label1:
            news_city, news_text, news_date = self.news_values()
            return selection, com.get_news(news_city, news_text, news_date), [news_city, news_text, news_date]
        elif selection == label2:
            ad_text, ad_date, formatted = self.ad_values()
            return selection, com.get_ad(ad_text, ad_date, formatted), [ad_text, formatted]
        elif selection == label3:
            rec_txt, rec_cal, fit_tip = self.recipe_values()
            return selection, com.get_recipe(rec_txt, rec_cal, fit_tip), [rec_txt, rec_cal, fit_tip]

    def write_to_db(self, selection, values):
        db = DBconnection(cnf.get_values("PATHS", "db_name"))
        db.create_table(selection)
        if selection == label1:
            try:
                db.go(cnf.get_values("SQL", "insert_news"), (values[0], values[1], values[2]))
                # lg.write_log(cnf.get_values("MESSAGES", "db_write").format
                #              (s=selection, t=selection.lower(), v1=values[0], v2=values[1], src="manual input"))
            except sql.IntegrityError:
                raise Duplicate(selection, values[0], values[1])
        elif selection == label2:
            try:
                db.go(cnf.get_values("SQL", "insert_ad"), (values[0], values[1]))
                # lg.write_log(cnf.get_values("MESSAGES", "db_write").format
                #              (s=selection, t=selection.lower(), v1=values[0], v2=values[1], src="manual input"))
            except sql.IntegrityError:
                raise Duplicate(selection, values[0], values[1])
        elif selection == label3:
            try:
                db.go(cnf.get_values("SQL", "insert_recipe"), (values[0], values[1], values[2]))
                # lg.write_log(cnf.get_values("MESSAGES", "db_write").format
                #              (s=selection, t=selection.lower(), v1=values[0], v2=values[1], src="manual input"))
            except sql.IntegrityError:
                raise Duplicate(selection, values[0], values[1])
        db.curs.close()

    def manual_flow(self):
        """Get formatted and prepared for write input.
        Write to the file.
        Write to db.
        """
        file_name = cnf.get_values("PATHS", "target_file")
        selection, text_for_file, values = self.prepare_for_file()
        f.append_file(text_for_file, file_name)
        lg.write_log(cnf.get_values("MESSAGES", "file_write").format(txt=text_for_file, src="manual input"))
        self.write_to_db(selection, values)
        lg.write_log(cnf.get_values("MESSAGES", "db_write").format
                             (s=selection, t=selection.lower(), v1=values[0], v2=values[1], src="manual input"))
