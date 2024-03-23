# REQUIRED IMPORTS CAN GO HERE


class Plugin:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.name = config["name"]
        self.version = config["version"]
        self.app.event_handler.subscribe("identify", self.identify)
        self.app.event_handler.subscribe(
            "application_started", self.on_application_started
        )
        self.app.event_handler.subscribe("identify", self.identify)

    def identify(self):
        self.app.event_handler.publish(
            "identify",
            name=self.name,
            version=self.version,
            author=self.config["author"],
            github=self.config["github"],
            description=self.config["description"],
        )

    def on_application_started(self):
        self.app.event_handler.publish(
            "log_event",
            message=f"Plugin Started",
            level="INFO",
            plugin_name=self.name,
        )
