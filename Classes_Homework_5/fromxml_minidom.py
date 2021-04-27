import xml.dom.minidom
from xml.parsers.expat import ExpatError

from modules.combine import Combine
from modules.dates import Dates
from modules.file import Files
from modules.input import DateInput
from exec_utils.configloader import Config
from fromjson import FromJson

# instantiate classes
cnf = Config()
f = Files()
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
        """Parse xml by pass"""
        doc = xml.dom.minidom.parse(file_path)
        return doc

    def get_sections(self, file_path):
        """Split xml by keyword into sections, in our case "sectionLable"""
        doc = self.get_xml(file_path)
        sections = doc.getElementsByTagName(label)
        return sections

    def get_elements(self, my_section, my_tag):
        """Get element value by tag name, i.e. London by 'sectionCity'"""
        element = my_section.getElementsByTagName(my_tag)[0].firstChild.nodeValue
        return element

    def process_xml(self, section):
        com = Combine(section.getAttribute("name"), decor, decor_length)
        if section.getAttribute("name") == label1:  # label1 = "News"
            news_text, news_city = self.get_elements(section, txt), self.get_elements(section, city)
            return com.get_news (news_city, news_text)+'\n\n'
        elif section.getAttribute("name") == label2:  # label2 = "Ad"
            ad_text = self.get_elements(section, txt)
            ad_date = dte.str_to_date(self.get_elements(section, date), cnf.get_values("PATTERNS", "date_format"))
            di.raise_if_past(ad_date)
            return com.get_ad (ad_text, ad_date)+'\n\n'
        elif section.getAttribute("name") == label3:  # label3 = "Recipe"
            rec_text = self.get_elements(section, txt)
            rec_cal = self.get_elements(section, cal)
            return com.get_recipe(rec_text, rec_cal)+'\n\n'
        else:
            pass

    def verify_source(self, my_path):
        try:
            sections = self.get_sections(my_path)
            temp_l = [x for x in map(self.process_xml, sections) if x]
            self.raise_if_empty(temp_l)
            final_text = ''.join(temp_l).rstrip()
            return final_text, my_path
        except (OSError, ExpatError, ValueError) as e:
            print(e)
            return None, None
        except (IndexError, AttributeError, TypeError):
            print(cnf.get_values("ERRORS", "cannot_parse"))
            return None, None

    def xml_full_flow(self, raw_source):
        text, proper_source = self.read_source(raw_source)  # this method is inherited from FromFile class in fromfile.py. It validates file and structure and asks user to input path until proper file is provided
        normalized_text = self.normalize(text, self.choose_strategy())
        self.write(normalized_text, proper_source)
        self.remove(proper_source)


if __name__ == "__main__":
    default_source = cnf.get_values("PATHS", "xml_source")
    default_target = cnf.get_values("PATHS", "target_file")
    fx = FromXML(default_source, default_target)
    raw_source = fx.parse()
    fx.xml_full_flow(raw_source)
