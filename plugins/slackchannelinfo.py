import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class SlackChannelInfo(plugin_loader.Parser):
    _alias_ = "SlackChannelInfo"
    _version_ = "1.2"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        self.logger.info(f"Getting channel info for {kwargs.get("channel_id")}")
        try:
            response = self.app.client.conversations_info(kwargs.get("channel_id"))
            channel = response.get("channel", {})
            channelinfo = {
                "channel_id": channel.get("id", None),
                "channel_name": channel.get("name", None)
            }
            self.logger.info(f"Retrieved channel info for {channelinfo.get("channel_name")}")
        except Exception as e:
            self.logger.error(f"Failed to get channel info: {e}")
            return None
        return channelinfo
