from exec_utils.configloader import Config

cnf = Config()


class NoSectionsError(Exception):
    """Raised when no elements with tag = sectionLabel can be found in the source file"""
    def __init__(self, section_label):
        self.section = section_label
        self.message = cnf.get_values("ERRORS", "no_sections").format(s=self.section)+"\n"
        super().__init__(self.message)


class PastDate(Exception):
    """Raised when provided date is before the current date"""
    def __init__(self, my_date):
        self.my_date = my_date
        self.message = cnf.get_values("ERRORS", "past_date").format(date=my_date)+"\n"
        super().__init__(self.message)


class NoValue(Exception):
    """Raised when provided value is Falsy"""
    def __init__(self, section_label, element):
        self.section = section_label
        self.element = element
        self.message = cnf.get_values("ERRORS", "no_value") % (self.element, self.section)+"\n"
        super().__init__(self.message)


class InvalidNumber(Exception):
    """Raised when non-integer value is provided for calories section"""
    def __init__(self, section_label, my_value):
        self.sec = section_label
        self.val = my_value
        self.message = cnf.get_values("ERRORS", "wrong_num").format(s =self.sec, e=self.val)+"\n"
        super().__init__(self.message)


class Duplicate(Exception):
    """Raised when unique constraint is violated"""
    def __init__(self, section_label, value1, value2):
        self.table = section_label.lower()
        self.v1 = value1
        self.v2 = value2
        self.message = cnf.get_values("ERRORS", "duplicate").format(v1=self.v1, v2 =self.v2, t=self.table)+"\n"
        super().__init__(self.message)
