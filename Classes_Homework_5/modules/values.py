from exec_utils.configloader import Config
from modules.input import TextInput, DateInput, IntInput
from modules.dates import Dates

# instantiate classes
cnf = Config()
d = Dates(cnf.get_values("FORMATS", "date_format"), cnf.get_values("FORMATS", "date_time_format"))
t = TextInput(cnf.get_values("ERRORS", "long_text"), cnf.get_values("RESTRICTIONS", "max_size"))
di = DateInput(cnf.get_values("ERRORS", "past_date"), cnf.get_values("FORMATS", "date_format"), d.get_current_date())
msg1, msg2, msg3 = cnf.get_values("MESSAGES", "fitness1"), cnf.get_values("MESSAGES", "fitness2"), cnf.get_values("MESSAGES", "fitness3")
ii = IntInput(cnf.get_values("RESTRICTIONS", "cal_min"), cnf.get_values("RESTRICTIONS", "cal_max"), msg1, msg2, msg3)


class Values:
    def __init__(self, section, delimiter, delimiter_length):
        self.section = section
        self.n = delimiter  # decorator sign to separate sections. Needs to be configured, currently = '-'
        self.count_n = int(delimiter_length)  # decorator signs quantity to separate sections. Needs to be configured, currently = 30

    def decorate_section(func):
        """Decorator to add section name + '---' before and after each section"""
        def wrapper(*args):
            before = args[0].section + ' ' + args[0].n * (args[0].count_n - len(args[0].section)-1)
            after = args[0].n * args[0].count_n
            res = before + '\n' + func(*args) + '\n' + after
            return res
        return wrapper

    @decorate_section
    def get_news(self):
        """Collect input data for news section, format date and put all attributes together"""
        city = t.ask_for_text(cnf.get_values("INPUTS", "city_msg"))
        news_text = t.ask_for_text(cnf.get_values("INPUTS", "news_msg"))
        news_date = d.format_date_time(d.get_current_date())
        news = news_text + '\n' + city + ', ' + news_date
        return news

    @decorate_section
    def get_ad(self):
        """Collect input data for ad section.
        Format date, calculate days to expiry date, get messages from configs and put all attributes together.
        """
        ad_text = t.ask_for_text(cnf.get_values("INPUTS", "ad_msg"))
        expiry_date = di.ask_for_date(cnf.get_values("INPUTS", "ad_date"))
        formatted_exp_date = d.format_date(expiry_date)
        delta = d.days_delta(expiry_date)
        message_start, message_end = cnf.get_values("MESSAGES", "message_start"), cnf.get_values("MESSAGES", "message_end")
        ad = ad_text + '\n' + message_start + ' ' + formatted_exp_date + ', ' + str(delta) + ' ' + message_end
        return ad

    @decorate_section
    def get_recipe(self):
        """Collect input data for recipe section.
        Apply logic based on input value, get messages from configs and put all attributes together.
        """
        recipe_text = t.ask_for_text(cnf.get_values("INPUTS", "recipe_msg"))
        recipe_calories, fitness_message = ii.ask_for_int(cnf.get_values("INPUTS", "recipe_calories"))
        calories_measure = cnf.get_values("MESSAGES", "calories_measure")
        recipe = recipe_text+'\n'+str(recipe_calories)+' '+calories_measure+'\n'+fitness_message
        return recipe
