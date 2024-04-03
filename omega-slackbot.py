#!.venv/bin/python
import slack_bolt as bolt
import json
import tempfile
import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pluginlib

import modules as omega


class OmegaSlackBot:
    def __init__(self):
        self.name = "APPLICATION"
        self.config = omega.OmegaConfiguration()
        self.logger = omega.get_logger(self.name)
        self.logger.info(f"Logger Initialized")
        self.temp_dir = tempfile.mkdtemp(prefix="omega_")
        self.logger.info(f"Temp Directory Created: {self.temp_dir}")
        self.db = omega.Database(self.config)
        self.initialize_plugins()
        self.logger.info(f"Creating Slack Instance")
        self.app = bolt.App(token=self.config.get("slack.bot_token"))
        self.app.use(self.catch_all_events_middleware())
        self.register_event_handlers()

    def __del__(self):
        self.logger.info(f"Deleting Temp Directory: {self.temp_dir}")
        os.rmdir(self.temp_dir)

    def initialize_plugins(self, path=None):
        from collections import OrderedDict

        transformed_dict = {}
        self.logger.info(f"Initializing Plugins")
        if path is None:
            path = f"{self.config.get('omega.plugins.directory', 'plugins/')}"
        self.loader = pluginlib.PluginLoader(paths=[path])
        self.plugins = self.loader.plugins

        for category, plugin_types in self.plugins.items():
            for plugin_name, plugin_class in plugin_types.items():
                alias = getattr(plugin_class, "_alias_", plugin_name)
                version = getattr(plugin_class, "_version_", "unknown")
                transformed_dict[alias] = version
        for plugin_alias, version in transformed_dict.items():
            self.logger.info(
                f"Loaded Plugin: {plugin_alias} v{version}"
            )  # Replace print with your logging as needed

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

    def add_block_options(self, modal, block_id, new_options):
        from copy import deepcopy

        updated_modal = deepcopy(modal)

        for block in updated_modal.get("blocks", []):
            if block.get("block_id") == block_id:
                block["element"]["options"] = new_options
                break
        return updated_modal

    def register_event_handlers(self):
        self.plugins.parser.FileToDatabase().parse(
            file="Documents/Downloads/sample.pdf", db=self.db
        )
        self.logger.info(f"Registering Event Handlers and Starting Omega Slackbot")

        @self.app.event("app_mention")
        def handle_message(context):
            event_data = context["event_data"]
            response_str = "Please don't pollute the channel with messages. I only respond to direct messages."
            self.respond_quietly(
                event_data.user_id, event_data.channel_id, response_str
            )

        @self.app.event("message")
        def handle_message_events(context):
            event_data = context["event_data"]
            print(event_data)
            for file_info in event_data["files"]:
                try:
                    download_filename = self.plugins.files.FileHandler(
                        app=self.app,
                        config=self.config,
                    ).download(
                        user=event_data["user"].get("full_name"),
                        file_name=file_info["name"],
                        file_url=file_info["url_private_download"],
                    )
                    filenames = self.plugins.parser.FileParser(
                        file=download_filename
                    ).parse()
                    for filename in getattr(filenames, "filenames", []):
                        self.plugins.parser.file_handler.send(filename)
                except Exception as e:
                    self.logger.error(f"Error processing file: {e}")
                zipfile = self.plugins.parser.Zipper().parse(
                    documents_directory=self.config.get("omega.documents.directory"),
                    filenames=filenames,
                    download_filename=download_filename,
                    user=event_data["user"].get("full_name"),
                )
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

        @self.app.view("doc_process_modal")
        def handle_modal_submission(ack, context):
            ack()

            # self.plugins.parser.DocProcess(context=context, app=self.app).process()

        @self.app.command("/invoice")
        def handle_doc_command(ack, context):
            ack()
            vendors = self.db.execute_query(query="SELECT * FROM vendors")
            vendor_options = [
                {
                    "text": {
                        "type": "plain_text",
                        "text": vendor[1],
                    },
                    "value": str(vendor[0]),
                }
                for vendor in vendors
            ]
            with open("slackblocks/invoice_process_modal.json", "r") as file:
                modal_json_str = file.read()
                modal_json = json.loads(modal_json_str)

            vendor_modal = self.add_block_options(modal_json, "vendor", vendor_options)
            self.app.client.views_open(
                trigger_id=context["event_data"]["command"].get("trigger_id"),
                view=vendor_modal,
            )

            self.vmodal = vendor_modal

        @self.app.action("vendor_select")
        def handle_vendor_selection(ack, body, action):
            ack()
            print(action)
            self.selected_vendor_name = action["selected_option"]["text"]["text"]
            self.selected_vendor_id = action["selected_option"]["value"]

            owners_query = """
            SELECT DISTINCT o.owner_id, o.owner
            FROM owners o 
            JOIN locations l ON o.owner_id = l.owner_id 
            WHERE l.vendor_id = %s
            """
            owners = self.db.execute_query(owners_query, (self.selected_vendor_id,))

            owner_options = [
                {
                    "text": {"type": "plain_text", "text": owner[1]},
                    "value": str(owner[0]),
                }
                for owner in owners
            ]

            self.omodel = self.add_block_options(self.vmodal, "client", owner_options)

            self.app.client.views_update(
                view_id=body["view"]["id"],
                hash=body["view"]["hash"],
                view=self.omodel,
            )

        @self.app.action("client_select")
        def handle_owner_selection(ack, body, action):
            ack()
            self.selected_owner_name = action["selected_option"]["text"]["text"]
            self.selected_owner_id = action["selected_option"]["value"]
            locations_query = """
            SELECT l.cw_id, l.site_name, l.street
            FROM locations l
            WHERE l.owner_id = %s AND l.vendor_id = %s
            ORDER BY l.site_name ASC, l.street ASC
            """
            locations = self.db.execute_query(
                locations_query, (self.selected_owner_id, self.selected_vendor_id)
            )

            # Format the locations into Slack-compatible select menu options
            location_options = [
                {
                    "text": {
                        "type": "plain_text",
                        "text": f"{location[1]} - {location[2]}",  # Concatenate site_name and street
                    },
                    "value": str(location[0]),  # Use cw_id as the value
                }
                for location in locations
            ]

            updated_modal = self.add_block_options(
                self.omodel, "location", location_options
            )

            self.app.client.views_update(
                view_id=body["view"]["id"],
                hash=body["view"]["hash"],
                view=updated_modal,
            )

        @self.app.view("doc_process")
        def handle_doc_process_submission(ack, body, view):
            self.logger.info(f"Processing Invoice Submission...")

            state = body["state"]
            user_id = body["user"]["id"]

            print(state)
            for file_info in state["files"]:
                try:
                    download_filename = self.plugins.files.FileHandler(
                        app=self.app,
                        config=self.config,
                    ).download(
                        user=state["user"].get("full_name"),
                        file_name=file_info["name"],
                        file_url=file_info["url_private_download"],
                    )
                    filenames = self.plugins.parser.FileParser(
                        file=download_filename
                    ).parse()
                    for filename in getattr(filenames, "filenames", []):
                        self.plugins.parser.file_handler.send(filename)
                except Exception as e:
                    self.logger.error(f"Error processing file: {e}")
                zipfile = self.plugins.parser.Zipper().parse(
                    documents_directory=self.config.get("omega.documents.directory"),
                    filenames=filenames,
                    download_filename=download_filename,
                    user=state["user"].get("full_name"),
                )
                self.respond_quietly(
                    state["user"].get("id"),
                    state["event"].get("channel_id"),
                    f"Files processed: {filenames}",
                )
                self.plugins.files.FileHandler(
                    app=self.app,
                    config=self.config,
                    file_name=zipfile,
                    file_url=zipfile,
                ).upload(
                    channel=state["event"].get("channel_id"),
                    file=zipfile,
                )
                os.remove(zipfile)

            ack()


if __name__ == "__main__":
    omegabot = OmegaSlackBot()
    handler = SocketModeHandler(
        omegabot.app, omegabot.config.get("slack.app_token")
    ).start()
