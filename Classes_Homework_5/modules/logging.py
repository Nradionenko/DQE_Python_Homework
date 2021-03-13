import logging

from exec_utils.configloader import Config
from modules.file import Files

cnf = Config()
f = Files()


class Log:
    def __init__(self, file_name):
        self.app_name = cnf.get_values("LABELS", "app_name")
        self.logfile = f.get_path(file_name)

    def logger(self):
        my_logger = logging.getLogger(self.app_name)
        my_logger.setLevel(logging.DEBUG)
        return my_logger

    @staticmethod
    def log_format():
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def log_file(self):
        logger = self.logger()
        fh = logging.FileHandler(self.logfile)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.log_format())
        if not logger.handlers:
            logger.addHandler(fh)
        return logger

    def write_log(self, my_message):
        logger = self.log_file()
        logger.info(my_message)

