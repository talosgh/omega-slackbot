import psycopg2
import sys


class Plugin:

    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.name = config["name"]
        self.version = config["version"]
        self.author = config["author"]
        self.github = config["github"]
        self.description = config["description"]
        self.app.event_handler.subscribe("identify", self.identify)
        self.app.event_handler.subscribe(
            "application_started", self.on_application_started
        )

        self.app.event_handler.subscribe("database_query", self.query)
        self.app.event_handler.subscribe("database_init", self.init_db)
        # self.init_db()

    def identify(self):
        self.app.event_handler.publish(
            "identify",
            name=self.name,
            version=self.version,
            author=self.suthor,
            github=self.github,
            description=self.description,
        )

    def on_application_started(self):
        self.app.event_handler.publish(
            "log_event",
            message=f"Plugin Started",
            level="INFO",
            plugin_name=self.name,
        )

    def init_db(self):
        try:
            self.conn = psycopg2.connect(
                host=self.app.app_config.db_host,
                port=self.app.app_config.db_port,
                dbname=self.app.app_config.db_name,
                user=self.app.app_config.db_user,
                password=self.app.app_config.db_pass,
            )
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            self.app.event_handler.publish(
                "log_event",
                message=f"Error connecting to database: {e}",
                level="ERROR",
                plugin_name=self.name,
            )
            sys.exit()

    def close(self):
        self.cur.close()
        self.conn.close()

    def query(self, query, params=None):
        try:
            self.curr.execute(query, params)

            if query.strip().lower().startswith("select"):
                results = self.curr.fetchall()
            else:
                self.conn.commit()
                results = None

        except psycopg2.Error as e:
            self.app.event_handler.publish(
                "log_event",
                message=f"Error querying database: {e}",
                level="ERROR",
                plugin_name=self.name,
            )
        return results
