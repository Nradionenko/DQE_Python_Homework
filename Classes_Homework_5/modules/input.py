import pyinputplus as pyip
import re
from exec_utils.configloader import Config

cnf = Config()


class Selection:
    def ask_for_selection(self, label1, label2, label3):
        """Initial input of section selection (news, ad or recipe).
        All sections are configurable in configs.ini.
        """
        section = pyip.inputMenu(prompt=cnf.get_values("INPUTS", "section")+"\n", choices=[label1, label2, label3], numbered=True)
        return section


class Proceed:
    def __init__(self, msg1, msg2):
        self.choice = msg1
        self.final_msg = msg2

    def next_steps(self):
        """Ask user whether she/he wants to proceed after section is added"""
        decision = pyip.inputYesNo(self.choice + '\n')
        return decision

    def goodbye(self):
        """Say goodbye to user if he/she doesn't want to proceed"""
        print(self.final_msg)


class TextInput:
    def __init__(self, error_text, max_size):
        self.error_text = error_text
        self.max_size = max_size

    def ask_for_text(self, input_text):
        """Ask for text input + raise error if text too long.
        Message for input, error message and max size are configurable.
        inputStr checks for empty string and won't allow it"""
        proper_text = False
        while not proper_text:
            try:
                user_input_text = pyip.inputStr(input_text+'\n')
                self.raise_if_too_long(user_input_text)
                proper_text = True
                return user_input_text.strip()
            except Exception as error_message:
                print(error_message)
                continue

    def raise_if_too_long(self, user_text):
        """Check input size vs max size and raise exception"""
        if len(user_text) > int(self.max_size):
            raise Exception (self.error_text)


class DateInput:
    def __init__(self, error_msg, req_format, compared_date):
        self.error_msg = error_msg
        self.format = req_format
        self.compared_date = compared_date

    def ask_for_date(self, input_msg):
        """Ask for date input and throw error if date is in the past.
        Message, error message and required format are configurable.
        Required format is also converted to 'readable' for user message (ie %d%m%y is shown as dd-mm-yy).
        inputDate checks date format, empty string + converts string input into date format.
        """
        proper_date = False
        while not proper_date:
            try:
                user_input_date = pyip.inputDate(self.readable_format(input_msg)+'\n', formats=[self.format])
                self.raise_if_past(user_input_date)
                proper_date = True
                return user_input_date
            except Exception as error_message:
                print(error_message)
                continue

    def readable_format(self, msg):
        """This function translates 'technical' date/datetime format into human-readable one.
        This is to make app more flexible: we configure date format once and then re-use it for user message.
        """
        rep = {"%d": "dd", "%m": "mm", "%B": "Month", "%b": "Mon", "%y": "yy", "%Y": "yyyy", "%H": "HH24", "%M": "MI"}
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], msg)
        return text

    def raise_if_past(self, user_date):
        """Compare input date to pre-defined date. In our case - to current date"""
        if user_date < self.compared_date.date():
            raise Exception (self.error_msg)


class IntInput:
    def __init__(self, min_value, max_value, msg1, msg2, msg3):
        self.min = int(min_value)
        self.max = int(max_value)
        self.fitness_tip_1 = msg1
        self.fitness_tip_2 = msg2
        self.fitness_tip_3 = msg3

    def ask_for_int(self, input_msg):
        """Asks for user input of type int (for random section, which is Recipe in my case and int = calories).
        Min acceptable value is configurable.
        """
        calories = pyip.inputInt(input_msg+'\n', min=self.min)
        fitness_tip = self.get_fitness_message(calories)
        return calories, fitness_tip

    def get_fitness_message(self, user_num):
        """Generates app message for random section (recipes) based on values
        provided (based on calories of the recipe).
        Min, max values as well as messages are configurable.
        """
        if user_num == self.min:
            summary = self.fitness_tip_1
        elif user_num < self.max:
            summary = self.fitness_tip_2
        else:
            summary = self.fitness_tip_3
        return summary
