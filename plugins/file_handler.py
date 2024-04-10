import modules.plugin_loader as plugin_loader
import os
from modules.logger import get_logger
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
        self.download_folder = os.path.join(self.documents_path, self.download_path)

    def download(self, **kwargs):
        """
        Download a file from a URL
        :param file_url: URL of the file to download
        :return: Path to the downloaded file
        """
        from urllib.parse import urlparse
        import tempfile

        file_url = kwargs.get("file_url")
        file_name = os.path.basename(urlparse(file_url).path)
        temp_dir = tempfile.mkdtemp()

        try:
            response = requests.get(
                file_url,
                allow_redirects=True,
                headers={"Authorization": f"Bearer {self.bot_token}"},
            )
            response.raise_for_status()

            with open(os.path.join(temp_dir, file_name), "wb+") as f:
                f.write(response.content)
            self.logger.info(f"Data written to temporary file: {temp_dir}/{file_name}")
            return os.path.join(temp_dir, file_name), temp_dir

        except Exception as e:
            self.logger.error(f"Error downloading file: {e}")
            return None

    def upload(self, **kwargs):
        """
        Upload a file to a Slack channel
        :param channel: Slack channel ID
        :param file: Path to file to upload
        """
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
