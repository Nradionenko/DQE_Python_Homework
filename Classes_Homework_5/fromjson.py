import argparse
from jsonschema import validate, ValidationError, SchemaError
from json import load, JSONDecodeError

from counts import Counts
from exec_utils.configloader import Config
from fromfile import WriteFromFile
from modules.combine import Combine
from modules.dates import Dates
from modules.exceptions import PastDate, NoValue
from modules.file import Files
from modules.input import DateInput
from modules.run import Execute

cnf = Config()
cnt = Counts(cnf.get_values("PATHS", "target_file"), cnf.get_values("PATHS", "csv_words"), cnf.get_values("PATHS", "csv_letters"))
dte = Dates()
di = DateInput(cnf.get_values("ERRORS", "past_date"),
               cnf.get_values("PATTERNS", "date_format"),
               dte.get_current_date())
e = Execute()
f = Files()

label1, label2, label3 = cnf.get_values("LABELS", "news_label"), \
                         cnf.get_values("LABELS", "ad_label"), \
                         cnf.get_values("LABELS", "recipe_label")
decor, decor_length = cnf.get_values("RESTRICTIONS", "n"), \
                      cnf.get_values("RESTRICTIONS", "count_n")
city, txt, date, cal = cnf.get_values("PROPERTIES", "city"), \
                       cnf.get_values("PROPERTIES", "text"), \
                       cnf.get_values("PROPERTIES", "date"), \
                       cnf.get_values("PROPERTIES", "kcal")


class FromJson(WriteFromFile):  # inherit methods from WriteFromFile in fromfile.py.
    def parse(self):
        """Get path to json from command line, take from configs if not provided"""
        parser = argparse.ArgumentParser(description="Process source file.")
        parser.add_argument("path", type=str, nargs="?",
                            default=self.def_source,
                            help="full path to file.")
        args = parser.parse_args()
        return args.path

    def get_schema(self):
        """Get expected schema to validate json. Schema file name is in configs, expected path = root package/../files folder"""
        schema_path = f.get_path(cnf.get_values("PATHS", "json_schema"))
        with open(schema_path, "r") as s:
            return load(s)

    def get_value(self, my_section, my_property):
        """Get property value in certain dictionary (=my_section) by certain key (=my_property)"""
        if str(my_section[my_property]).strip():
            return my_section[my_property]
        else:
            raise NoValue(my_section, my_property)

    def news_values(self, my_dict):
        """Extract/generate values related to News section"""
        n_city = self.get_value(my_dict, city)
        n_text = self.get_value(my_dict, txt)
        n_date = dte.format_date(dte.get_current_date(), cnf.get_values("PATTERNS", "date_time_text"))
        return n_city, n_text, n_date

    def ad_values(self, my_dict):
        """Extract/generate values related to Private ad section"""
        a_text = self.get_value(my_dict, txt)
        a_date = self.get_value(my_dict, date)  # string date value from JSON
        # format string date from json to datetime.date:
        exp_date = dte.str_to_date(a_date, cnf.get_values("PATTERNS", "date_format"))
        return a_text, exp_date, a_date

    def recipe_values(self, my_dict):
        """Extract/generate values related to Recipe section"""
        r_text = self.get_value(my_dict, txt)
        r_cal = self.get_value(my_dict, cal)
        fit_tip = e.get_fitness_message(r_cal)
        return r_text, r_cal, fit_tip

    def normalize_json(self, my_json, strategy):
        """Normalize JSON before parsing it"""
        for key in my_json.keys():
            for dct in my_json[key]:
                for key2 in dct.keys():
                    if isinstance(dct[key2], str):
                        dct[key2] = self.normalize(dct[key2], strategy)
        return my_json

    def process_json(self, normalized_json):
        """Extract sections values from json, combine them into pre-formatted text and write to db"""
        final_text = ''
        db_values = []
        for key in normalized_json.keys():  # json keys = arrays names, in our case - News, Ad or Recipe
            com = Combine(key, decor, decor_length)
            for d in normalized_json[key]:  # each section in json has list of dictionaries with section properties (i.e. News has city and text etc)
                if key == label1:  # label1 = News, label2 = Ad, label3 = Recipe. Configured in configs.ini
                    n_city, n_text, n_date = self.news_values(d)
                    final_text += com.get_news(n_city, n_text, n_date)+'\n\n'
                    db_values.append([key, n_city, n_text, n_date])
                elif key == label2:
                    a_text, exp_date, a_date = self.ad_values(d)
                    di.raise_if_past(exp_date)  # check if date is not in the past
                    final_text += com.get_ad(a_text, exp_date, a_date)+'\n\n'
                    db_values.append([key, a_text, a_date])
                elif key == label3:
                    r_text, r_cal, fit_tip = self.recipe_values(d)
                    final_text += com.get_recipe(r_text, r_cal, fit_tip)+'\n\n'
                    db_values.append([key, r_text, r_cal, fit_tip])
        return final_text.rstrip(), db_values

    def verify_source(self, source):
        """Verify if source is valid + validate source json against schema"""
        schema = self.get_schema()
        try:
            with open(source, "r", encoding="utf-8") as file:
                my_json = load(file)
                validate(my_json, schema)
                strategy = self.choose_strategy()
                normalized = self.normalize_json(my_json, strategy)
                text, db_values = self.process_json(normalized)
                return source, text, db_values
        except SchemaError:
            print(cnf.get_values("ERRORS", "schema_err"))
            return None, None, None
        except (OSError, ValidationError, JSONDecodeError, AttributeError, IndexError,
                KeyError, ValueError, PastDate, NoValue) as err:
            print(err)
            return None, None, None


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "json_source")
    default_target = cnf.get_values("PATHS", "target_file")
    fj = FromJson(default_source, default_target)
    raw_source = fj.parse()
    fj.file_full_flow(raw_source)  # inherited from WriteFromFile
    cnt.write_csv()
