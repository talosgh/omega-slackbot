import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class MessageEvent(plugin_loader.SlackEvent):
    _alias_ = "MessageEvent"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)
        self.context = kwargs.get("context")
        event_data = kwargs.get(self.context["event_data"])

    def react(self):
        self.t = ""
        pass
