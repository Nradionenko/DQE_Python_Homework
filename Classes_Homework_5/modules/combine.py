from exec_utils.configloader import Config
from modules.dates import Dates

# instantiate classes
cnf = Config()
d = Dates()


class Combine:
    def __init__(self, section, delimiter, delimiter_length):
        self.section = section
        self.n = delimiter  # decorator sign to separate sections. Needs to be configured, currently = '-'
        self.count_n = int(delimiter_length)  # decorator signs quantity to separate sections. Needs to be configured, currently = 30

    def decorate_section(func):
        """Decorator to add section name + '---' before and after each section"""
        def wrapper(*args):
            # i.e., section = 'News', n = '-', count_n = 30. args[0] = self
            before = args[0].section + ' ' + args[0].n * (args[0].count_n - len(args[0].section)-1)
            after = args[0].n * args[0].count_n
            res = before + '\n' + func(*args) + '\n' + after
            return res
        return wrapper

    @decorate_section
    def get_news(self, city, news_text, news_date):
        """Collect input data for news section, format date and put all attributes together"""
        news = news_text + '\n' + city + ', ' + news_date
        return news

    @decorate_section
    def get_ad(self, ad_text, expiry_date, formatted):
        """Collect input data for ad section.
        Format date, calculate days to expiry date, get messages from configs and put all attributes together.
        """
        delta = d.days_delta(expiry_date)
        ad_summary = cnf.get_values("MESSAGES", "ad_summary")
        ad = ad_text + '\n' + ad_summary % (formatted, str(delta))
        return ad

    @decorate_section
    def get_recipe(self, recipe_text, recipe_calories, fitness_tip):
        """Collect input data for recipe section.
        Apply logic based on input value, get messages from configs and put all attributes together.
        """
        calories_measure = cnf.get_values("MESSAGES", "calories_measure")
        recipe = recipe_text+'\n'+str(recipe_calories)+' '+calories_measure+'\n'+fitness_tip
        return recipe
