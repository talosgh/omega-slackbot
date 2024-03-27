class AppHome:
    def __init__(self, event_data, db):
        self.db = db
        self.event_data = event_data
        self.user = self.event_data.user_id
        self.homeview = self.create_home()

    def create_home(self):
        r = {
            "user_id": self.user,
            "view": {
                "type": "home",
                "blocks": [
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Hello",
                                },
                                "value": "hello",
                                "action_id": "hello",
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Goodbye",
                                },
                                "value": "goodbye",
                                "action_id": "goodbye",
                            },
                        ],
                    },
                    {
                        "type": "input",
                        "block_id": "input_block_id",
                        "label": {"type": "plain_text", "text": "Upload Files"},
                        "element": {
                            "type": "file_input",
                            "action_id": "file_input_action_id_1",
                            "filetypes": ["pdf"],
                            "max_files": 5,
                        },
                    },
                ],
            },
        }
        return r

    def create_dropdown(self, data):
        l = []
        for row in data:
            l.append(row[1])
        return l
