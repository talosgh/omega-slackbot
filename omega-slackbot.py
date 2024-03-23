import slack_bolt as bolt
from slack_bolt.adapter.socket_mode import SocketModeHandler

import modules as omega


class OmegaSlackBot:
    def __init__(self):
        self.app_config = omega.OmegaConfiguration()
        self.log = omega.Logger(self.app_config).get_logger()
        # self.db = omega.Database(self.log, self.app_config)
        self.app_directories = omega.Directories(
            self.log, (self.app_config.doc_path, self.app_config.doc_download_path)
        )
        self.app = bolt.App(token=self.app_config.SLACK_BOT_TOKEN)

        self.event_handler = omega.PluginEventManager(self)
        self.plugin_manager = omega.PluginManager(self, plugins_path="plugins/")

        self.event_handler.subscribe("plugin_data_event", self.handle_plugin_data)
        self.event_handler.subscribe("log_event", self.handle_plugin_log_event)
        self.event_handler.subscribe("identify", self.handle_plugin_identify)

        self.start_omega()

    def handle_plugin_identify(self, **kwargs):
        self.log.info(
            f"Plugin Information: {kwargs['name']} Version: {kwargs['version']}"
        )
        self.log.info(f"Author: {kwargs['author']} GitHub: {kwargs['github']}")
        self.log.info(f"Description: {kwargs['description']}\n")

    def handle_plugin_log_event(self, message, level, plugin_name):
        level = level.upper()
        if level == "ERROR":
            self.log.error(f"[PLUGIN ({plugin_name})] {message}")
        elif level == "DEBUG":
            self.log.debug(f"[PLUGIN ({plugin_name})] {message}")
        elif level == "WARNING":
            self.log.warning(f"[PLUGIN ({plugin_name})] {message}")
        else:
            self.log.info(f"[PLUGIN ({plugin_name})] {message}")

    def handle_plugin_data(self, data, context):
        plugin_name = context["plugin_name"]
        event_type = context["event_type"]
        self.log.info(
            f"Received data from {plugin_name} in response to {event_type}: {data}"
        )

    def plugins_initialize(self):
        self.plugin_manager.load_plugins()
        self.log.info("Application started. Notifying plugins...")
        self.event_handler.publish("application_started")
        plugins_info = self.plugin_manager.get_plugins_info()
        for plugin_info in plugins_info:
            self.log.info("Plugin Information:")
            self.log.info(
                f"Plugin: {plugin_info['name']} Version: {plugin_info['version']}"
            )
            self.log.info(
                f"Author: {plugin_info['author']} GitHub: {plugin_info['github']}"
            )
            self.log.info(f"Description: {plugin_info['description']}\n")
        return None

    def plugins_send_event(self, event_name, *args, **kwargs):
        self.event_handler.publish(event_name, *args, **kwargs)

    def start_omega(self):

        self.db = self.plugins_send_event("initialize_db")

        @self.app.event("app_mention")
        def handle_message(body):
            event_data = omega.EventLogger(self.log, body, self.app, self.db)
            self.plugins_send_event(body["event"]["type"])
            response_str = "Please don't pollute the channel with messages. I only respond to direct messages."
            self.respond_quietly(
                event_data.user_id, event_data.channel_id, response_str
            )

        @self.app.event("message")
        def handle_message_events(body):
            event_data = omega.EventLogger(self.log, body, self.app, self.db)
            self.plugins_send_event(body["event"]["type"])
            if "files" in body["event"]:
                file_handler = omega.FileHandler(
                    self.app, event_data, self.log, self.app_config
                )
                parse_handler = self.plugins_send_event(
                    "parse_file", file="Documents/sample.pdf"
                )
                for f in parse_handler.filenames:
                    omega.FileHandler.send(self, f)
                query = "INSERT INTO doc_dump (file, text, user_id) VALUES (%s, %s, %s)"
                params = (
                    parse_handler.file,
                    parse_handler.text,
                    event_data.user_fullname,
                )
                query_result = self.plugins_send_event(
                    "database_query", query=query, params=params
                )
                # self.db.query(query, params)
            else:
                self.log.info("Received a direct message")

        @self.app.command("/invoice")
        def invoice_command(ack, body):
            ack("invoice command received")
            event_data = omega.EventLogger(self.log, body, self.app, self.db)
            self.plugins_send_event(body["event"]["type"])

        @self.app.event("file_created")
        def handle_file_created_events(body, logger):
            event_data = omega.EventLogger(self.log, body, self.app, self.db)
            self.plugins_send_event(body["event"]["type"])

        @self.app.event("file_shared")
        def handle_file_shared(ack, body):
            event_data = omega.EventLogger(self.log, body, self.app, self.db)
            self.plugins_send_event(body["event"]["type"])

        @self.app.event("app_home_opened")
        def handle_app_home_opened(ack, body):
            event_data = omega.EventLogger(self.log, body, self.app, self.db)
            self.plugins_send_event(body["event"]["type"])
            homeview_handler = omega.AppHome(event_data, self.db)
            self.app.client.views_publish(homeview_handler.homeview)

    def respond_quietly(self, user, channel, response_str):
        try:
            self.app.client.chat_postEphemeral(
                channel=channel,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": response_str,
                        },
                    }
                ],
                text=response_str,
                user=user,
            )
        except Exception as e:
            self.log.error(f"Error responding to message: {e}")


if __name__ == "__main__":
    omegabot = OmegaSlackBot()
    omegabot.plugins_initialize()
    handler = SocketModeHandler(
        omegabot.app, omegabot.app_config.SLACK_APP_TOKEN
    ).start()
    handler.start()
