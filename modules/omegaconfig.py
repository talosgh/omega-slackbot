import yaml
import sys


class OmegaConfiguration:
    def __init__(self):
        try:
            with open("config.yml", "r") as file:
                config = yaml.safe_load(file)
        except Exception as e:
            sys.exit(f"Error loading config file: {e}")

        self.SLACK_BOT_TOKEN = config["slack"]["bot_token"]
        self.SLACK_APP_TOKEN = config["slack"]["app_token"]
        self.db_host = config["omega"]["modules"]["database"]["host"]
        self.db_port = config["omega"]["modules"]["database"]["port"]
        self.db_name = config["omega"]["modules"]["database"]["database"]
        self.db_user = config["omega"]["modules"]["database"]["user"]
        self.db_pass = config["omega"]["modules"]["database"]["password"]
        self.doc_path = config["omega"]["documents"]["directory"]
        self.doc_download_path = config["omega"]["documents"]["download_directory"]

        self.fmt = config["omega"]["modules"]["logger"]["format"]
        self.level = config["omega"]["modules"]["logger"]["level"]
        self.dfmt = config["omega"]["modules"]["logger"]["date_format"]
