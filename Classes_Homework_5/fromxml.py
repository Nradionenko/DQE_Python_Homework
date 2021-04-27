import xml.etree.ElementTree as ET

from counts import Counts
from modules.combine import Combine
from modules.dates import Dates
from modules.file import Files
from modules.input import DateInput
from exec_utils.configloader import Config
from fromjson import FromJson
from modules.exceptions import NoSectionsError, PastDate, NoValue
from modules.run import Execute

# instantiate classes
cnf = Config()
cnt = Counts(cnf.get_values("PATHS", "target_file"), cnf.get_values("PATHS", "csv_words"), cnf.get_values("PATHS", "csv_letters"))
f = Files()
e = Execute()
dte = Dates()
di = DateInput(cnf.get_values("ERRORS", "past_date"),
               cnf.get_values("PATTERNS", "date_format"),
               dte.get_current_date())

# declare variables
label1, label2, label3 = cnf.get_values("LABELS", "news_label"), \
                         cnf.get_values("LABELS", "ad_label"), \
                         cnf.get_values("LABELS", "recipe_label")
decor, decor_length = cnf.get_values("RESTRICTIONS", "n"), \
                      cnf.get_values("RESTRICTIONS", "count_n")
label, city, txt, date, cal = cnf.get_values("PROPERTIES", "label"), \
                              cnf.get_values("PROPERTIES", "city"), \
                              cnf.get_values("PROPERTIES", "text"), \
                              cnf.get_values("PROPERTIES", "date"), \
                              cnf.get_values("PROPERTIES", "kcal")


class FromXML(FromJson):  # inherit methods from FromJson in fromjson.py.
    def get_xml(self, file_path):
        """Parse xml by path"""
        doc = ET.parse(file_path)
        return doc

    def get_sections(self, file_path):
        """Split xml by keyword into sections, in our case "sectionLable"""
        doc = self.get_xml(file_path)
        sections = doc.findall('./'+label)  # find all elements with sectionLabel tag
        if sections:
            return sections
        else:
            raise NoSectionsError(label)

    def get_element(self, my_section, my_label, my_tag, strategy):
        """Get element value by tag name, i.e. London by 'sectionCity'"""
        try:
            element = my_section.find('./'+my_tag).text
            if element.strip():
                elm_text = element.strip()
                return self.normalize(elm_text, strategy)
            else:
                raise NoValue(my_label, my_tag)
        except AttributeError:
            print(cnf.get_values("ERRORS", "no_element") % (my_tag, my_label)+"\n")
            return None

    def get_attr(self, my_section):
        """Get section name, in our case - News, Ad or Recipe"""
        attribute = my_section.attrib['name']
        return attribute

    def news_values(self, my_sect, my_label, strat):
        """Get and normalize values for news section"""
        n_city = self.get_element(my_sect, my_label, city, strat)
        n_text = self.get_element(my_sect, my_label, txt, strat)
        n_date = dte.format_date(dte.get_current_date(), cnf.get_values("PATTERNS", "date_time_text"))
        return n_city, n_text, n_date

    def ad_values(self, my_sect, my_label, strat):
        """Get and normalize values for private ad section"""
        a_text = self.get_element(my_sect, my_label, txt, strat)
        a_date = self.get_element(my_sect, my_label, date, strat)
        exp_date = dte.str_to_date(a_date, cnf.get_values("PATTERNS", "date_format"))  # format to datetime.date
        di.raise_if_past(exp_date)
        return a_text, exp_date, a_date

    def recipe_values(self, my_sect, my_label, strat):
        """Get and normalize values for recipe section"""
        r_text = self.get_element( my_sect, my_label, txt, strat)
        r_cal = self.get_element( my_sect, my_label, cal, strat)
        fit_tip = e.get_fitness_message(r_cal)
        return r_text, r_cal, fit_tip

    def process_xml(self, my_section, strat):
        """Within each section format values for file + insert them to db"""
        section_label = self.get_attr(my_section)
        com = Combine(section_label, decor, decor_length)  # instantiate Combine class which puts together and decorates sections based on city/text/date etc attributes
        if section_label == label1:  # label1 = "News"
            n_city, n_text, n_date = self.news_values(my_section, section_label, strat)
            return com.get_news(n_city, n_text, n_date)+'\n\n', [section_label, n_city, n_text, n_date]
        elif section_label == label2:  # label2 = "Ad"
            a_text, exp_date, a_date = self.ad_values(my_section, section_label, strat)
            return com.get_ad(a_text, exp_date, a_date)+'\n\n', [section_label, a_text, a_date]
        elif section_label == label3:  # label3 = "Recipe"
            r_text, r_cal, fit_tip = self.recipe_values(my_section, section_label, strat)
            return com.get_recipe(r_text, r_cal, fit_tip)+'\n\n', [section_label, r_text, r_cal, fit_tip]

    def verify_source(self, my_path):
        """Try opening and parsing the file, if any errors - raise exceptions"""
        try:
            sections = self.get_sections(my_path)
            strategy = self.choose_strategy()
            text_values = []
            db_values = []
            for section in sections:
                processed_text, values = self.process_xml(section, strategy)
                if processed_text:
                    text_values.append(processed_text)
                    db_values.append(values)
            self.raise_if_empty(text_values)  # if list is empty, raise error
            final_text = ''.join(text_values).rstrip()  # join list of formatted sections back into text
            return my_path, final_text, db_values
        except (OSError, ValueError, ET.ParseError, NoSectionsError,
                PastDate, NoValue) as e:
            print(e)
            return None, None, None
        except AttributeError:
            print(cnf.get_values("ERRORS", "cannot_parse"))
            return None, None, None
        except KeyError:
            print(cnf.get_values("ERRORS", "no_attr")+"\n")
            return None, None, None
        except TypeError:
            pass
            return None, None, None


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "xml_source")
    default_target = cnf.get_values("PATHS", "target_file")
    fx = FromXML(default_source, default_target)
    raw_source = fx.parse()  # parse method is inherited from FromJson
    fx.file_full_flow(raw_source)  # method inherited from FromJson->WriteFromFile
    cnt.write_csv()
