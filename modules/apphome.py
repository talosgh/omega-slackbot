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
                ],
            },
        }
        return r
