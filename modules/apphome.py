class AppHome:
    def __init__(self, event_data, db):
        self.db = db
        self.event_data = event_data
        self.user = self.event_data.user_id
        self.homeview = self.create_home()

        def create_home(self):
        import datetime

        doc_query = "SELECT * FROM documents"
        documents = self.db.execute_query(doc_query)

        if not documents:  # Checking for an empty list or None
            doc_list = [
                {
                    "text": {
                        "type": "plain_text",
                        "text": "No unreviewed documents found!",
                    },
                    "value": "no_documents",
                }
            ]
        else:
            doc_list = []
            for doc in documents:
                # Assuming doc[6] is a datetime object, formatting the timestamp
                timestamp = doc[6].strftime("%d-%m-%Y")
                doc_list.append({
                    "text": {
                        "type": "plain_text",
                        "text": f"{doc[1]} - Uploaded by {doc[7]} on {timestamp}",
                    },
                    "value": str(doc[5]),  # Ensure this is a string as required
                })

        # Define the home view structure with corrected section block for button
        home_view = {
            "user_id": self.user,
            "view": {
                "type": "home",
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "document_select",
                        "element": {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a document to review",
                            },
                            "options": doc_list,
                            "action_id": "document_select_action",
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Select a document to review",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This is a section block with a button.",
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Perform Action",
                            },
                            "value": "review",
                            "action_id": "review_button_action",
                        },
                    },
                ],
            },
        }
        return home_view