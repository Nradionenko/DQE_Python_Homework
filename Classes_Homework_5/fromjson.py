import argparse
from jsonschema import validate, ValidationError, SchemaError
from json import load, JSONDecodeError

from modules.combine import Combine
from modules.dates import Dates
from modules.file import Files
from modules.input import DateInput
from exec_utils.configloader import Config
from fromfile import WriteFromFile

cnf = Config()
f = Files()
dte = Dates()
di = DateInput(cnf.get_values("ERRORS", "past_date"),
               cnf.get_values("PATTERNS", "date_format"),
               dte.get_current_date())

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

    def process_json(self, json):
        """Extract sections values from json and combine them into pre-formatted text"""
        final_text = ''
        for key in json.keys():  # json keys = arrays names, in our case - News, Ad or Recipe
            com = Combine(key, decor, decor_length)
            for d in json[key]:  # each section in json has list of dictionaries with section properties (i.e. News has city and text etc)
                if key == label1:  # label1 = News, label2 = Ad, label3 = Recipe. Configured in configs.ini
                    final_text += com.get_news(d[city], d[txt])+'\n\n'
                elif key == label2:
                    expiry_date = dte.str_to_date(d[date], cnf.get_values("PATTERNS", "date_format"))  # format string date from json to datetime.date
                    di.raise_if_past(expiry_date)  # check if date is not in the past
                    final_text += com.get_ad(d[txt], expiry_date)+'\n\n'
                elif key == label3:
                    final_text += com.get_recipe(d[txt], d[cal])+'\n\n'
        return final_text.rstrip()

    def verify_source(self, source):
        """Verify if source is valid + validate source json against schema"""
        schema = self.get_schema()
        try:
            with open(source, "r", encoding="utf-8") as file:
                my_json = load(file)
                validate(my_json, schema)
                text = self.process_json(my_json)
                return text, source
        except SchemaError as e:
            print(cnf.get_values("ERRORS", "schema_err"))
            return None, None
        except (OSError, ValidationError, JSONDecodeError, KeyError, AttributeError, ValueError) as e:
            print(e)
            return None, None

    def json_full_flow(self, raw_source):
        text, proper_source = self.read_source(raw_source)  # this method is inherited from FromFile class in fromfile.py. It validates file and structure and asks user to input path until proper file is provided
        normalized_text = self.normalize(text, self.choose_strategy())
        self.write(normalized_text, proper_source)
        self.remove(proper_source)


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "json_source")
    default_target = cnf.get_values("PATHS", "target_file")
    fj = FromJson(default_source, default_target)
    raw_source = fj.parse()
    fj.json_full_flow(raw_source)
