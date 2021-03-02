from exec_utils.configloader import Config
from modules.input import Selection, TextInput, DateInput, IntInput
from modules.dates import Dates
from modules.file import Files
from modules.combine import Combine


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
label1, label2, label3 = cnf.get_values("LABELS", "news_label"), \
                         cnf.get_values("LABELS", "ad_label"), \
                         cnf.get_values("LABELS", "recipe_label")
decor, decor_length = cnf.get_values("RESTRICTIONS", "n"), \
                      cnf.get_values("RESTRICTIONS", "count_n")


class Execute:
    def prepare_for_file(self):
        """Ask user for selection and then ask for all further details based on selected value.
        Combine input values into 1 section (=prepare for writing to the file)
        """
        selection = s.ask_for_selection(label1, label2, label3)
        com = Combine(selection, decor, decor_length)
        if selection == label1:
            city = t.ask_for_text(cnf.get_values("INPUTS", "city_msg"))
            news_text = t.ask_for_multiline().rstrip()
            final_text = com.get_news(city, news_text)
        elif selection == label2:
            ad_text = t.ask_for_text(cnf.get_values("INPUTS", "ad_msg"))
            expiry_date = di.ask_for_date(cnf.get_values("INPUTS", "ad_date"))
            final_text = com.get_ad(ad_text, expiry_date)
        elif selection == label3:
            recipe_text = t.ask_for_text(cnf.get_values("INPUTS", "recipe_msg"))
            recipe_calories = ii.ask_for_int(cnf.get_values("INPUTS", "recipe_calories"))
            final_text = com.get_recipe(recipe_text, recipe_calories)
        return final_text

    def manual_flow(self):
        """Get formatted and prepared for write input.
        Write to the file.
        File name is configurable
        """
        file_name = cnf.get_values("PATHS", "target_file")
        text_for_file = self.prepare_for_file()
        f.append_file(text_for_file, file_name)
