{
    "type": "modal",
    "callback_id": "doc_process_modal",
    "title": {"type": "plain_text", "text": "Document Processing", "emoji": True},
    "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
    "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
    "blocks": [
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
        {"type": "divider"},
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "plain_text_input-action",
            },
            "label": {"type": "plain_text", "text": "Originator", "emoji": True},
        },
        {
            "type": "input",
            "element": {
                "type": "radio_buttons",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Invoice",
                            "emoji": True,
                        },
                        "value": "invoice",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Proposal",
                            "emoji": True,
                        },
                        "value": "proposal",
                    },
                ],
                "action_id": "radio_buttons-action",
            },
            "label": {"type": "plain_text", "text": "Document Type", "emoji": True},
        },
        {"type": "divider"},
        {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a vendor",
                    "emoji": True,
                },
                "options": [
                    {"text": {"type": "plain_text", "text": "24-Hour"}, "value": "1"},
                    {"text": {"type": "plain_text", "text": "Admiral"}, "value": "2"},
                    {
                        "text": {"type": "plain_text", "text": "Associated-ELV"},
                        "value": "3",
                    },
                    {"text": {"type": "plain_text", "text": "DC-ELV"}, "value": "4"},
                    {
                        "text": {"type": "plain_text", "text": "Delaware-ELV"},
                        "value": "5",
                    },
                    {"text": {"type": "plain_text", "text": "ELCON"}, "value": "6"},
                    {"text": {"type": "plain_text", "text": "Fujitec"}, "value": "7"},
                    {
                        "text": {"type": "plain_text", "text": "Islamorada-ELV"},
                        "value": "8",
                    },
                    {"text": {"type": "plain_text", "text": "Kone"}, "value": "9"},
                    {"text": {"type": "plain_text", "text": "Liberty"}, "value": "10"},
                    {
                        "text": {"type": "plain_text", "text": "Liftech-ELV"},
                        "value": "11",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Mitsubishi"},
                        "value": "12",
                    },
                    {"text": {"type": "plain_text", "text": "Mowrey"}, "value": "13"},
                    {"text": {"type": "plain_text", "text": "Murphy"}, "value": "14"},
                    {
                        "text": {"type": "plain_text", "text": "Next-Level"},
                        "value": "15",
                    },
                    {"text": {"type": "plain_text", "text": "Nouveau"}, "value": "16"},
                    {"text": {"type": "plain_text", "text": "Oracle"}, "value": "17"},
                    {"text": {"type": "plain_text", "text": "Otis"}, "value": "18"},
                    {
                        "text": {"type": "plain_text", "text": "PS-Marcato"},
                        "value": "19",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Pine State-ELV"},
                        "value": "20",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Precision"},
                        "value": "21",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "San Francisco Elevator",
                        },
                        "value": "22",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Schindler"},
                        "value": "23",
                    },
                    {"text": {"type": "plain_text", "text": "Skyline"}, "value": "24"},
                    {
                        "text": {"type": "plain_text", "text": "Specialized"},
                        "value": "25",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Star Elevator"},
                        "value": "26",
                    },
                    {"text": {"type": "plain_text", "text": "TAKA"}, "value": "27"},
                    {"text": {"type": "plain_text", "text": "TEC"}, "value": "28"},
                    {"text": {"type": "plain_text", "text": "TEI"}, "value": "29"},
                    {"text": {"type": "plain_text", "text": "TK"}, "value": "30"},
                    {"text": {"type": "plain_text", "text": "VTS"}, "value": "31"},
                    {"text": {"type": "plain_text", "text": "Unknown"}, "value": "999"},
                ],
                "action_id": "vendor_select",
            },
            "label": {"type": "plain_text", "text": "Vendor", "emoji": True},
        },
        {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a client",
                    "emoji": True,
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "*plain_text option 0*",
                            "emoji": True,
                        },
                        "value": "value-0",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "*plain_text option 1*",
                            "emoji": True,
                        },
                        "value": "value-1",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "*plain_text option 2*",
                            "emoji": True,
                        },
                        "value": "value-2",
                    },
                ],
                "action_id": "client_select",
            },
            "label": {"type": "plain_text", "text": "Client", "emoji": True},
        },
        {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a location",
                    "emoji": True,
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "*plain_text option 0*",
                            "emoji": True,
                        },
                        "value": "value-0",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "*plain_text option 1*",
                            "emoji": True,
                        },
                        "value": "value-1",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "*plain_text option 2*",
                            "emoji": True,
                        },
                        "value": "value-2",
                    },
                ],
                "action_id": "location_select",
            },
            "label": {"type": "plain_text", "text": "Location", "emoji": True},
        },
        {"type": "divider"},
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "plain_text_input-action",
            },
            "label": {"type": "plain_text", "text": "Document ID", "emoji": True},
        },
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "plain_text_input-action",
            },
            "label": {
                "type": "plain_text",
                "text": "Scope / Description",
                "emoji": True,
            },
        },
        {
            "type": "input",
            "element": {
                "type": "number_input",
                "is_decimal_allowed": False,
                "action_id": "number_input-action",
            },
            "label": {"type": "plain_text", "text": "Total Price", "emoji": True},
        },
        {"type": "divider"},
    ],
}
