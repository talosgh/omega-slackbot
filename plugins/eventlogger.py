import modules.plugin_loader as plugin_loader
import json
from datetime import datetime


from modules.logger import get_logger


class EventLogger(plugin_loader.EventLogger):
    _alias_ = "EventLogger"
    _version_ = "1.0"

    def __init__(self, body, app, db):
        self.logger = get_logger(self._alias_)
        self.body = body
        self.app = app
        self.db = db
        self.files_info = []

        self.event_type = None
        self.event_ts = None
        self.event_text = None
        self.user_id = None
        self.channel_id = None
        self.user_fname = None
        self.user_lname = None
        self.user_fullname = None
        self.user_email = None
        self.command_trigger_id = None

        if "event" in self.body:
            self.parse_event()
            if "user" in self.body.get("event", {}):
                self.parse_user()
            if "files" in self.body.get("event", {}):
                self.parse_files()
        elif "command" in self.body:
            self.parse_command()

        self.log_event()

    def parse_channel(self):
        response = self.app.client.conversations_info(channel=self.channel_id)
        channel = response.get("channel", {})
        self.channel_id = channel.get("id", "")
        self.channel_name = channel.get("name", "")

    def parse_event(self):
        if self.body.get("event", {}):
            event = self.body.get("event", {})
            self.user_id = event.get("user") or event.get("user_id")
            self.channel_id = event.get("channel") or event.get("channel_id")
            self.event_type = event.get("type")
            self.event_ts = datetime.fromtimestamp(
                float(event.get("event_ts", 0))
            ).strftime("%Y-%m-%d %H:%M:%S")
            self.event_text = event.get("text", "")
        else:
            self.logger.warning("No valid event provided")

    def parse_user(self):
        response = self.app.client.users_profile_get(user=self.user_id)
        profile = response.get("profile", {})
        self.user_fname = profile.get("first_name", "")
        self.user_lname = profile.get("last_name", "")
        self.user_fullname = profile.get("real_name", "")
        self.user_email = profile.get("email", "")

    def parse_command(self):
        self.event_type = self.body.get("command", "")
        self.user_id = self.body.get("user_id", "")
        if self.user_id:
            self.parse_user()
        self.channel_id = self.body.get("channel_id", "")
        self.event_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.command_trigger_id = self.body.get("trigger_id", "")

    def parse_files(self):
        self.has_files = False
        self.files_info = []

        # Check for multiple files
        files = self.body.get("event", {}).get("files", [])
        if files:
            self.has_files = True
            for file in files:
                self.process_file(file)

        # Check for a single file
        elif "file" in self.body.get("event", {}):
            self.has_files = True
            file = self.body["event"]["file"]
            self.process_file(file)

    def process_file(self, file):
        file_id = file.get("id")
        file_info_response = self.app.client.files_info(file=file_id)
        file_info = file_info_response.get("file", {})
        self.files_info.append(
            {
                "id": file_id,
                "name": file_info.get("name"),
                "url_private_download": file_info.get("url_private_download"),
                "filetype": file_info.get("filetype"),
                "size": file_info.get("size"),
            }
        )

    def log_event(self):
        body_json = json.dumps(self.body)
        files_json = json.dumps(self.files_info)
        params = (
            body_json,
            self.event_type,
            self.event_ts,
            self.event_text,
            self.user_id,
            self.channel_id,
            files_json,
            self.user_fname,
            self.user_lname,
            self.user_fullname,
            self.user_email,
        )
        query = """INSERT INTO slack_event_log 
                   (event_body, event_type, event_ts, event_text, user_id, 
                    channel_id, files_info, user_fname, user_lname, 
                    user_fullname, user_email) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        self.db.execute_query(query, params)
        self.logger.info(
            f"Logged event: {self.event_type} from {self.user_fullname} in channel {self.channel_id} at {self.event_ts}"
        )
        return None

    def to_dict(self):
        if self.files_info is None:
            self.files_info = {}
        return {
            "event": {
                "type": self.event_type,
                "timestamp": self.event_ts,
                "text": self.event_text,
                "channel_id": self.channel_id,
            },
            "command": {
                "trigger_id": self.command_trigger_id,
            },
            "user": {
                "id": self.user_id,
                "first_name": self.user_fname,
                "last_name": self.user_lname,
                "full_name": self.user_fullname,
                "email": self.user_email,
            },
            "files": self.files_info,
        }
