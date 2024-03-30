import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class SlackUserInfo(plugin_loader.Parser):
    _alias_ = "SlackUserInfo"
    _version_ = "1.2"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        self.logger.info(f"Getting user info for {self.kwargs.get('user_id')}")
        try:
            response = self.app.client.users_profile_get(
                user=self.kwargs.get("user_id")
            )
            userdata = response.get("profile", {})
            userinfo = {
                "user_id": userdata.get("id", None),
                "user_fname": userdata.get("first_name", None),
                "user_lname": userdata.get("last_name", None),
                "user_fullname": userdata.get("real_name", None),
                "user_email": userdata.get("email", None),
            }
            self.logger.info(f"Retrieved user info for {userinfo.get("user_fullname")}")
        except Exception as e:
            self.logger.error(f"Failed to get user info: {e}")
            return None
        return userinfo
