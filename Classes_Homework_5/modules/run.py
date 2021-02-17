from exec_utils.configloader import Config
from modules.input import Selection
from modules.file import Files
from modules.values import Values

cnf = Config()
s = Selection()
f = Files()

label1, label2, label3 = cnf.get_values("LABELS", "news_label"), cnf.get_values("LABELS", "ad_label"), cnf.get_values("LABELS", "recipe_label")
decor, decor_length = cnf.get_values("RESTRICTIONS", "n"), cnf.get_values("RESTRICTIONS", "count_n")


class Execute:
    def prepare_for_file(self):
        """Ask user for selection and then ask for all further details based on selected value.
        Combine input values into 1 section (=prepare for writing to the file)
        """
        selection = s.ask_for_selection(label1, label2, label3)
        val = Values(selection, decor, decor_length)
        if selection == label1:
            news = val.get_news()
            return news
        elif selection == label2:
            ad = val.get_ad()
            return ad
        elif selection == label3:
            recipe = val.get_recipe()
            return recipe

    def end_to_end(self):
        """Get formatted and prepared for write input.
        Write to the file.
        File name is configurable
        """
        file_name = cnf.get_values("PATHS", "target_file")
        text_for_file = self.prepare_for_file()
        f.write_file(text_for_file, file_name)
