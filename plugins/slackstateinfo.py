import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class SlackStateInfo(plugin_loader.Parser):
    _alias_ = "SlackStateInfo"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        self.logger.info(f"Getting state info for modal submission")
        try:
            view = kwargs.get("view")

        except Exception as e:
            self.logger.error(f"Failed to get channel info: {e}")
            return None
        return {
            "user_id": view["user"].get("id", None),
            "view_id": view["view"].get("id", None),
            "callback_id": view["view"].get("callback_id", None),
        }
