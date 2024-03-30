import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class SlackEventInfo(plugin_loader.Parser):
    _alias_ = "SlackEventInfo"
    _version_ = "0.8"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        self.logger.info(f"Getting channel info for {kwargs.get("channel_id")}")
        try:
            response = self.app.client.conversations_info(kwargs.get("channel_id"))
            channel = response.get("channel", {})

        except Exception as e:
            self.logger.error(f"Failed to get event info: {e}")
            return None
        return {
            "channel_id": channel.get("id", None),
            "channel_name": channel.get("name", None)
        }
