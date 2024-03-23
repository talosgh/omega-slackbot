from datetime import datetime


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


class EventLogger:
    def __init__(self, log, body, app, db):
        self.body = body
        self.app = app
        self.db = db
        self.log = log

        if "user" in self.body["event"]:
            self.user_id = self.body["event"]["user"]
        elif "user_id" in self.body["event"]:
            self.user_id = self.body["event"]["user_id"]
        if "channel" in self.body["event"]:
            self.channel_id = self.body["event"]["channel"]
        elif "channel_id" in self.body["event"]:
            self.channel_id = self.body["event"]["channel_id"]

        self.event_type = self.body["event"]["type"]
        self.event_ts = datetime.fromtimestamp(self.body["event"]["event_ts"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        if "text" in self.body["event"]:
            self.event_text = self.body["event"]["text"]

        if "files" in self.body["event"]:
            self.file_id = self.body["event"]["files"][0]["id"]
            self.file_info = self.app.client.files_info(file=self.file_id)
            self.file_name = self.body["event"]["files"][0]["name"]
            self.file_url = self.body["event"]["files"][0]["url_private_download"]
            self.file_type = self.body["event"]["files"][0]["filetype"]
            self.file_size = self.body["event"]["files"][0]["size"]

        self.user_data = self.app.client.users.profile_get(user=self.user_id)
        self.user_fname = self.data["profile"]["first_name"]
        self.user_lname = self.data["profile"]["last_name"]
        self.user_fullname = self.data["profile"]["real_name"]
        self.user_email = self.data["profile"]["email"]

    def log_event(self):
        params = (
            self.body,
            self.event_type,
            self.event_ts,
            self.event_text,
            self.user_id,
            self.channel_id,
            self.file_id,
            self.file_name,
            self.file_url,
            self.file_type,
            self.file_size,
            self.user_fname,
            self.user_lname,
            self.user_fullname,
            self.user_email,
        )
        query = "INSERT INTO slack_event_log (event_body, event_type, event_ts, event_text, user_id, channel_id, file_id, file_name, file_url, file_type, file_size, user_fname, user_lname, user_fullname, user_email) VALUES (%s, %s, %d, %s, %s, %s, %s, %s, %s, %s, %d, %s, %s, %s, %s);"
        self.db.query(query, params)
        self.log.info(
            f"Logged event: {self.event_type} from {self.user_fullname} in {self.channel_id} at {self.event_ts}"
        )
        return None
