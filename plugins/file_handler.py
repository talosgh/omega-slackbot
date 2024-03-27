import modules.plugin_loader as plugin_loader
import os
from modules.logger import get_logger
from modules.database import Database
import requests


class FileHandler(plugin_loader.FileHandling):
    _alias_ = "FileHandler"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)
        self.app = kwargs.get("app")
        self.config = kwargs.get("config")
        self.bot_token = self.config.get("slack.bot_token")
        self.documents_path = self.config.get("omega.documents.directory", "Documents")
        self.download_path = self.config.get(
            "omega.documents.download_directory", "Downloads"
        )
        self.download_path = os.path.join(self.documents_path, self.download_path)

    def download(self, **kwargs):
        user = kwargs.get("user")
        file_name = kwargs.get("file_name")
        file_url = kwargs.get("file_url")
        download_folder = os.path.join(self.documents_path, self.download_path)
        os.makedirs(download_folder, exist_ok=True)
        download_filename = os.path.join(download_folder, file_name)
        try:
            response = requests.get(
                file_url,
                allow_redirects=True,
                headers={"Authorization": f"Bearer {self.bot_token}"},
            )
            response.raise_for_status()
            with open(download_filename, "wb") as file:
                file.write(response.content)

            self.logger.info(f"File saved as: {download_filename}")
            db = Database(self.config)
            query = "INSERT INTO doc_dump (file, user_id) VALUES (%s, %s)"
            params = (
                download_filename,
                user,
            )
            db.execute_query(query, params)
            self.logger.info(f"File saved to database: {download_filename}")
            return download_filename
        except Exception as e:
            self.logger.error(f"Error downloading file: {e}")
            return None

    def upload(self, **kwargs):
        channel = kwargs.get("channel")
        file_name = kwargs.get("file")
        try:
            self.app.client.files_upload_v2(
                channel=channel,
                filename=file_name,
                file=file_name,
                title=file_name,
                initial_comment=None,
            )
            self.logger.info(f"File uploaded: {file_name}")
        except Exception as e:
            self.logger.error(f"Error uploading {file_name}: {e}")
