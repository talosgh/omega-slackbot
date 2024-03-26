#!.venv/bin/python
import slack_bolt as bolt
import datetime
import os
from zipfile import ZipFile
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pluginlib

import modules as omega


class OmegaSlackBot:
    def __init__(self):
        self.name = "APPLICATION"
        self.config = omega.OmegaConfiguration()
        self.logger = omega.get_logger(self.name)
        self.logger.info(f"Logger Initialized")
        self.db = omega.Database(self.config)
        self.initialize_plugins()
        self.plugins.parser.Directory(
            paths=[
                self.config.get("omega.documents.directory"),
                self.config.get("omega.documents.download_directory"),
            ]
        ).parse(),
        self.logger.info(f"Creating Slack Instance")
        self.app = bolt.App(token=self.config.get("slack.bot_token"))
        self.app.use(self.catch_all_events_middleware())
        self.register_event_handlers()

    def initialize_plugins(self, path=None):
        self.logger.info(f"Initializing Plugins")
        if path is None:
            path = f"{self.config.get('omega.plugins.directory', 'plugins/')}"
        self.loader = pluginlib.PluginLoader(paths=[path])
        self.plugins = self.loader.plugins
        self.logger.info(f"Loaded Plugins: {self.plugins}")

    def catch_all_events_middleware(self):
        def middleware(context, body, next):
            event_data = self.plugins.eventlogger.EventLogger(
                body, self.app, self.db
            ).to_dict()
            self.plugins.Database
            context["event_data"] = event_data
            return next()

        return middleware

    def respond_quietly(self, user, channel, response_str):
        try:
            self.app.client.chat_postEphemeral(
                channel=channel,
                blocks=[
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": response_str},
                    }
                ],
                text=response_str,
                user=user,
            )
        except Exception as e:
            self.logger.error(
                f"Error responding to message in {channel} to {user}: {e}"
            )

    def register_event_handlers(self):

        self.logger.info(f"Registering Event Handlers and Starting Omega Slackbot")

        @self.app.event("app_mention")
        def handle_message(context):
            event_data = context["event_data"]
            response_str = "Please don't pollute the channel with messages. I only respond to direct messages."
            self.respond_quietly(
                event_data.user_id, event_data.channel_id, response_str
            )

        @self.app.event("message")
        def handle_message_events(ack, context):
            ack()
            event_data = context["event_data"]
            for file_info in event_data["files"]:
                try:
                    download_filename = self.plugins.files.FileHandler(
                        app=self.app,
                        config=self.config,
                        file_name=file_info["name"],
                        file_url=file_info["url_private_download"],
                    ).download()
                    # TODO move back into file handler
                    query = "INSERT INTO doc_dump (file, user_id) VALUES (%s, %s)"
                    params = (
                        download_filename,
                        event_data["user"].get("full_name"),
                    )
                    self.db.execute_query(query, params)
                    filenames = self.plugins.parser.FileParser(
                        file=download_filename
                    ).parse()
                    for filename in getattr(filenames, "filenames", []):
                        self.plugins.parser.file_handler.send(filename)
                except Exception as e:
                    self.logger.error(f"Error processing file: {e}")
                # TODO zip plugin
                unix_timestamp = (
                    datetime.datetime.timestamp(datetime.datetime.now()) * 1000
                )
                z = os.path.join(
                    self.config.get("omega.documents.directory"),
                    self.config.get("omega.documents.download_directory"),
                )
                zipfile = (
                    z
                    + event_data["user"].get("full_name")
                    + str(unix_timestamp)
                    + ".zip"
                )
                with ZipFile(zipfile, "w") as zip:
                    for filename in filenames:
                        zip.write(filename)
                        os.remove(filename)
                    zip.write(download_filename)
                    os.remove(download_filename)
                self.respond_quietly(
                    event_data["user"].get("id"),
                    event_data["event"].get("channel_id"),
                    f"Files processed: {filenames}",
                )
                self.plugins.files.FileHandler(
                    app=self.app,
                    config=self.config,
                    file_name=zipfile,
                    file_url=zipfile,
                ).upload(
                    channel=event_data["event"].get("channel_id"),
                    file=zipfile,
                )
                os.remove(zipfile)

        @self.app.event("file_created")
        def handle_file_created_events(context):
            return None

        @self.app.event("file_shared")
        def handle_file_shared(body):
            return None

        @self.app.event("app_home_opened")
        def handle_app_home_opened(context):
            homeview_handler = omega.AppHome(context, self.db)
            self.app.client.views_publish(**homeview_handler.homeview)


if __name__ == "__main__":
    omegabot = OmegaSlackBot()
    handler = SocketModeHandler(
        omegabot.app, omegabot.config.get("slack.app_token")
    ).start()
