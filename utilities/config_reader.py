import configparser
import os.path

class ConfigReader:

     _config = configparser.ConfigParser()

     config_path = os.path.join(
         os.path.dirname(os.path.dirname(__file__)),
         "config",
         "config.ini"
     )

     _config.read(config_path)

     @staticmethod
     def get_base_url():
         return ConfigReader._config.get("DEFAULT", "base_url")

     @staticmethod
     def get_browser():
         return ConfigReader._config.get("DEFAULT", "browser")

     @staticmethod
     def get_implicit_wait():
         return  ConfigReader._config.get("DEFAULT", "implicit_wait")

     @staticmethod
     def get_explicit_wait():
         return ConfigReader._config.get("DEFAULT", "explicit_wait")