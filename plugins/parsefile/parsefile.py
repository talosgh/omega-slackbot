import fitz
import pandas as pd


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
        self.app.event_handler.subscribe("parse_file", self.parse_event)
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

    def parse_event(self, file):
        self.file = file
        event_context = {"plugin_name": self.name, "event_type": "parse_request"}
        data = self.parse()
        self.app.event_handler.publish("plugin_data_event", data, event_context)

    def parse(self):
        self.app.event_handler.publish(
            "log_event",
            message=f"Beginning Parsing of {self.file}",
            level="INFO",
            plugin_name=self.name,
        )
        self.filenames = []
        with fitz.open(f"{self.file}") as doc:
            with open(f"{self.file}.txt", "w") as f:
                for page in doc:
                    self.text = page.get_text("text", flags=34)
                    tables = page.find_tables()
                    if len(tables.tables) > 0:
                        for t in tables.tables:
                            df = pd.DataFrame()
                            df = t.to_pandas()
                            df.to_csv(f"{self.file}_table{t}.csv")
                            f.write(df.to_markdown(tablefmt="grid") + "\n\n")
                            self.filenames.append(f"{self.file}_table{t}.csv")
                f.write(self.text)
            self.filenames.append(f"{self.file}.txt")
        self.app.event_handler.publish(
            "log_event",
            message=f"Completed parsing {self.file}",
            level="INFO",
            plugin_name=self.name,
        )
        data = {"filenames": self.filenames}
        data["text"] = self.text
        return data
