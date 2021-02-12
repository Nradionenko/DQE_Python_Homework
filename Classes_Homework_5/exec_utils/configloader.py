from configparser import ConfigParser, ExtendedInterpolation
import os


class Config:
    configParser = ConfigParser(interpolation=ExtendedInterpolation())
    config_file_path = '\\'.join(os.path.realpath(__file__).split('\\')[0:-1]) + r'\configs.ini'  # identifies the same directory as this module.

    @classmethod
    def get_values(cls, section, attribute):
        """Get value from specified section from configs.ini."""
        cls.configParser.read(cls.config_file_path)
        return cls.configParser.get(section, attribute)
