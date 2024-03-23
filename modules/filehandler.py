import requests


class FileHandler:
    def __init__(self, app, event_data, log, app_config):
        self.log = log
        self.app = app
        self.event_data = event_data
        self.bot_token = app_config.SLACK_BOT_TOKEN

        self.user = self.event_data.user_id
        self.channel = self.event_data.channel_id

        self.file_id = self.event_data.file_id
        self.file_info = self.app.client.files_info(file=self.file_id)
        self.file_name = self.event_data.file_name
        self.file_url = self.event_data.file_url

        self.file = self.run()

    def download(self):
        try:
            self.download_filename = f"Downloads/{self.file_name}"
            r = requests.get(
                self.file_url,
                allow_redirects=True,
                headers={"Authorization": f"Bearer {self.bot_token}"},
            )
            with open(self.download_filename, "wb") as fd:
                fd.write(r.content)

            self.log.info(f"File saved as: {self.download_filename}")
            response_str = f"File received: {self.file_name}"
        except Exception as e:
            self.log.error(f"Error downloading file: {e}")
            response_str = f"Error downloading {self.file_name}: {e}"

        self.app.respond_quietly(self.user, self.channel, response_str)
        return self.download_filename

    def send(self, file):
        try:
            self.app.client.files_upload_v2(
                channel=self.channel,
                filename=file,
                file=file,
                title=file,
                initial_comment=None,
            )
            response_str = f"File uploaded: {self.file_name}"
        except Exception as e:
            self.log.error(f"Error uploading file: {e}")
            response_str = f"Error uploading {self.file_name}: {e}"

        self.app.respond_quietly(self.user, self.channel, response_str)
