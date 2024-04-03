import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class SlackFileInfo(plugin_loader.Parser):
    _alias_ = "SlackFileInfo"
    _version_ = "1.2"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)
        self.files = []

    def parse(self, **kwargs):
        self.logger.info(f"Getting file info for {kwargs.get('file_id')}")
        try:
            file_info_response = self.app.client.files_info(file=kwargs.get("file_id"))
            file_info = file_info_response.get("file", {})
            self.files.append(
                {
                    "id": file_info.get("id", None),
                    "name": file_info.get("name", None),
                    "mimetype": file_info.get("mimetype", None),
                    "url_private": file_info.get("url_private", None),
                    "filetype": file_info.get("filetype", None),
                    "size": file_info.get("size", None),
                }
            )
            self.logger.info(f"Retrieved file info for {file_info.get('name')}")
        except Exception as e:
            self.logger.error(f"Failed to get user info: {e}")
            return None
        return self.files
