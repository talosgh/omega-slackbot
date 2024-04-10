import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class SlackStateInfo(plugin_loader.Parser):
    _alias_ = "SlackStateInfo"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        """Get state information from Slack
        Args:
            view (dict): View object
        Returns:
            dict: State information
        """

        self.logger.info(f"Getting state info for modal submission")
        f = []
        try:
            view = kwargs.get("view")

            for file in view["state"]["values"]["file_upload"]:
                f.append(
                    {
                        "id": file["view"]["state"]["values"]["file_upload"][
                            "files"
                        ].get("id", None),
                        "name": file["view"]["state"]["values"]["file_upload"][
                            "files"
                        ].get("name", None),
                        "url": file["view"]["state"]["values"]["file_upload"][
                            "files"
                        ].get("url_private", None),
                    }
                )

            file_info = {
                "user_id": view["user"].get("id", None),
                "view_id": view["view"].get("id", None),
                "callback_id": view["view"].get("callback_id", None),
                "files": f,
                "originator": view["view"]["state"]["values"]["originator"][
                    "plain_text_input_action"
                ].get("value", None),
                "vendor_name": view["view"]["state"]["values"]["vendor"][
                    "vendor_select"
                ]["selected_option"]["text"].get("text", None),
                "vendor_id": view["view"]["state"]["values"]["vendor"]["vendor_select"][
                    "selected_option"
                ].get("value", None),
                "client_name": view["view"]["state"]["values"]["client"][
                    "client_select"
                ]["selected_option"]["text"].get("text", None),
                "client_id": view["view"]["state"]["values"]["client"]["client_select"][
                    "selected_option"
                ].get("value", None),
                "location": view["view"]["state"]["values"]["location"][
                    "location_select"
                ]["selected_option"]["text"].get("text", None),
                "location_id": view["view"]["state"]["values"]["location"][
                    "location_select"
                ]["selected_option"].get("value", None),
                "document_number": view["view"]["state"]["values"]["doc_id"][
                    "plain_text_input_action"
                ].get("value", None),
                "scope_description": view["view"]["state"]["values"]["scope"][
                    "plain_text_input_action"
                ].get("value", None),
                "cost": view["view"]["state"]["values"]["cost"][
                    "number_input_action"
                ].get("value", None),
            }
            self.logger.info(f"Retrieved state info for {file_info.get('view_id')}")
        except Exception as e:
            self.logger.error(f"Failed to get modal state info: {e}")
            return None
        return file_info
