import yaml
import sys


class OmegaConfiguration:
    def __init__(self, config_path="config.yml"):
        try:
            with open(config_path, "r") as file:
                self.config = yaml.safe_load(file)
        except Exception as e:
            sys.exit(f"Error loading config file: {e}")

        # Validate configuration after loading
        self.validate_config()

        # Now that the config is validated, load properties
        self.load_properties()

    def get(self, path, default=None):
        """
        Retrieve a configuration value using a dot-separated path.
        Returns 'default' if the key is not found.
        """
        keys = path.split(".")
        value = self.config
        for key in keys:
            if value is not None and key in value:
                value = value[key]
            else:
                return default
        return value

    def load_properties(self):
        """
        Load properties from the configuration into the class instance.
        """
        self.SLACK_BOT_TOKEN = self.get("slack.bot_token")
        self.SLACK_APP_TOKEN = self.get("slack.app_token")
        self.db_host = self.get("omega.database.host")
        self.db_port = self.get("omega.database.port")
        self.db_name = self.get("omega.database.database")
        self.db_user = self.get("omega.database.user")
        self.db_pass = self.get("omega.database.password")
        self.doc_path = self.get("omega.documents.directory")
        self.doc_download_path = self.get("omega.documents.download_directory")
        self.log_path = self.get("omega.logger.directory")
        self.plugins_path = self.get("omega.plugins.directory")

    def validate_config(self):
        """
        Validate the loaded configuration to ensure all necessary keys are present.
        Raise an exception if any required configuration is missing.
        """
        required_keys = [
            "slack.bot_token",
            "slack.app_token",
            "omega.database.host",
            "omega.database.port",
            "omega.database.database",
            "omega.database.user",
            "omega.database.password",
            "omega.documents.directory",
            "omega.documents.download_directory",
            "omega.logger.directory",
            "omega.plugins.directory",
        ]
        missing_keys = [key for key in required_keys if self.get(key) is None]
        if missing_keys:
            raise ValueError(f"Missing configuration keys: {', '.join(missing_keys)}")
