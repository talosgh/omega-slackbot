#!.venv/bin/python
import slack_bolt as bolt
import json
import os
from zipfile import ZipFile
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pluginlib
from pandas import DataFrame

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
        for p in self.plugins:
            self.logger.info(f"Loaded Plugin: {p}")

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

    def replace_block_options(self, original_modal, label_text_to_match, new_options):
        from copy import deepcopy

        updated_modal = deepcopy(original_modal)

        # Iterate through the blocks to find the target block by its label text
        for block in updated_modal.get("blocks", []):
            # Check if this block is an input with a static_select element
            if (
                block.get("type") == "input"
                and block.get("element", {}).get("type") == "static_select"
            ):
                # Now, check if the label's text matches the provided label_text_to_match
                if block.get("label", {}).get("text") == label_text_to_match:
                    # Found the block, now update its options
                    block["element"]["options"] = new_options
                    break  # Assuming only one block matches, we can break out of the loop

        return updated_modal

    def add_initial_option(self, original_modal, label_text_to_match, text, value):
        from copy import deepcopy

        updated_modal = deepcopy(original_modal)

        # Iterate through the blocks to find the target block by its label text
        for block in updated_modal.get("blocks", []):
            # Check if this block is an input with a static_select element
            if (
                block.get("type") == "input"
                and block.get("element", {}).get("type") == "static_select"
            ):
                # Now, check if the label's text matches the provided label_text_to_match
                if block.get("label", {}).get("text") == label_text_to_match:
                    # Found the block, now update its options
                    block["element"]["initial_option"] = {
                        "text": {
                            "type": "plain_text",
                            "text": text,
                            "emoji": True,
                        },
                        "value": value,
                    }
                    break  # Assuming only one block matches, we can break out of the loop

        return updated_modal

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

        @self.app.command("/doc")
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
            with open("slackblocks/docprocess_modal.json", "r") as file:
                modal_json_str = file.read()
                modal_json = json.loads(modal_json_str)

            vendor_modal = self.replace_block_options(
                modal_json, "Vendor", vendor_options
            )
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

            updated_modal = self.replace_block_options(
                self.vmodal, "Client", owner_options
            )
            self.omodel = self.add_initial_option(
                updated_modal,
                "Vendor",
                self.selected_vendor_name,
                self.selected_vendor_id,
            )

            self.app.client.views_update(
                view_id=body["view"]["id"],
                hash=body["view"]["hash"],
                view=self.omodel,
            )

        @self.app.action("client_select")
        def handle_owner_selection(ack, body, action):
            ack()
            print(action)
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

            updated_modal = self.replace_block_options(
                self.omodel, "Location", location_options
            )

            self.lmodel = self.add_initial_option(
                updated_modal,
                "Client",
                self.selected_owner_name,
                self.selected_owner_id,
            )

            self.app.client.views_update(
                view_id=body["view"]["id"],
                hash=body["view"]["hash"],
                view=self.lmodel,
            )

        @self.app.action("hello")
        def handle_hello(ack):
            ack()
            print("Hello")


if __name__ == "__main__":
    omegabot = OmegaSlackBot()
    handler = SocketModeHandler(
        omegabot.app, omegabot.config.get("slack.app_token")
    ).start()
