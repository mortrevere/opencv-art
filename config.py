import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

WIDTH = int(config["output"]["w"])
HEIGHT = int(config["output"]["h"])
