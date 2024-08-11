import configparser

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['API']['key']
google_key = config['GOOGLEAPI']['googleapi']