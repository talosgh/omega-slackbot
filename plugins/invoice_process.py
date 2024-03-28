import modules.plugin_loader as plugin_loader
from modules.logger import get_logger
from modules.database import Database


class InvoiceProcessor(plugin_loader.Parser):
    _alias_ = "InvoiceProcessor"
    _version_ = "0.1"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)
        self.app = kwargs.get("app")
        self.context = kwargs.get("context")
        self.db = Database()

    def parse(self, **kwargs):
        self.ack()
        body = kwargs.get("body")

        inputs = body["view"]["state"]["values"]

        uploaded_files = inputs["file_upload"]["input_block_id"][
            "file_input_action_id_1"
        ]["selected_files"]
        originator = inputs["block_id_for_originator"]["plain_text_input-action"][
            "value"
        ]
        document_type = inputs["block_id_for_document_type"]["radio_buttons-action"][
            "selected_option"
        ]["value"]
        vendor = inputs["block_id_for_vendor"]["static_select-action"][
            "selected_option"
        ]["value"]
        client = inputs["block_id_for_client"]["static_select-action"][
            "selected_option"
        ]["value"]
        location = inputs["block_id_for_location"]["static_select-action"][
            "selected_option"
        ]["value"]
        document_id = inputs["block_id_for_document_id"]["plain_text_input-action"][
            "value"
        ]
        scope_description = inputs["block_id_for_scope_description"][
            "plain_text_input-action"
        ]["value"]
        total_price = inputs["block_id_for_total_price"]["number_input-action"]["value"]

        if not originator.strip():
            self.logger.error("Originator cannot be empty.")
            return {
                "errors": [
                    {
                        "name": "block_id_for_originator",
                        "error": "Originator cannot be empty.",
                    }
                ]
            }

        self.logger.info(f"Uploaded files: {uploaded_files}")
        self.logger.info(f"Originator: {originator}")
        self.logger.info(f"Document Type: {document_type}")
        self.logger.info(f"Vendor: {vendor}")
        self.logger.info(f"Client: {client}")
        self.logger.info(f"Location: {location}")
        self.logger.info(f"Document ID: {document_id}")
        self.logger.info(f"Scope/Description: {scope_description}")
        self.logger.info(f"Total Price: {total_price}")
