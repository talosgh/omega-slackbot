{
    "type": "view_submission",
    "team": {"id": "T0331TJV7", "domain": "gravityholdings"},
    "user": {
        "id": "UGFL0UGGN",
        "username": "tj.theesfeld",
        "name": "tj.theesfeld",
        "team_id": "T0331TJV7",
    },
    "api_app_id": "A06KV1TBUEQ",
    "token": "Qbah0gCbFZIlV5s3cWf3BRDc",
    "trigger_id": "6862236807559.3103936993.04e3e1fa9aa227cec72ca40ac9d3d06e",
    "view": {
        "id": "V06RPRV95E1",
        "team_id": "T0331TJV7",
        "type": "modal",
        "blocks": [
            {
                "type": "input",
                "block_id": "file_upload",
                "label": {"type": "plain_text", "text": "Upload Files", "emoji": True},
                "optional": False,
                "dispatch_action": False,
                "element": {
                    "type": "file_input",
                    "action_id": "file_input_action_id_1",
                    "filetypes": ["pdf"],
                    "max_files": 5,
                    "max_file_size_bytes": 10000000,
                },
            },
            {"type": "divider", "block_id": "fpLig"},
            {
                "type": "input",
                "block_id": "originator",
                "label": {"type": "plain_text", "text": "Originator", "emoji": True},
                "optional": False,
                "dispatch_action": False,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                    "dispatch_action_config": {
                        "trigger_actions_on": ["on_enter_pressed"]
                    },
                },
            },
            {"type": "divider", "block_id": "klLcC"},
            {
                "type": "input",
                "block_id": "vendor",
                "label": {"type": "plain_text", "text": "Vendor", "emoji": True},
                "optional": False,
                "dispatch_action": True,
                "element": {
                    "type": "static_select",
                    "action_id": "vendor_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a vendor",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "24-Hour",
                                "emoji": True,
                            },
                            "value": "1",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Admiral",
                                "emoji": True,
                            },
                            "value": "2",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Associated-ELV",
                                "emoji": True,
                            },
                            "value": "3",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "DC-ELV",
                                "emoji": True,
                            },
                            "value": "4",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Delaware-ELV",
                                "emoji": True,
                            },
                            "value": "5",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "ELCON",
                                "emoji": True,
                            },
                            "value": "6",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Fujitec",
                                "emoji": True,
                            },
                            "value": "7",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Islamorada-ELV",
                                "emoji": True,
                            },
                            "value": "8",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Kone",
                                "emoji": True,
                            },
                            "value": "9",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Liberty",
                                "emoji": True,
                            },
                            "value": "10",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Liftech-ELV",
                                "emoji": True,
                            },
                            "value": "11",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Mitsubishi",
                                "emoji": True,
                            },
                            "value": "12",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Mowrey",
                                "emoji": True,
                            },
                            "value": "13",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Murphy",
                                "emoji": True,
                            },
                            "value": "14",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Next-Level",
                                "emoji": True,
                            },
                            "value": "15",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Nouveau",
                                "emoji": True,
                            },
                            "value": "16",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Oracle",
                                "emoji": True,
                            },
                            "value": "17",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Otis",
                                "emoji": True,
                            },
                            "value": "18",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "PS-Marcato",
                                "emoji": True,
                            },
                            "value": "19",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Pine State-ELV",
                                "emoji": True,
                            },
                            "value": "20",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Precision",
                                "emoji": True,
                            },
                            "value": "21",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "San Francisco Elevator",
                                "emoji": True,
                            },
                            "value": "22",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Schindler",
                                "emoji": True,
                            },
                            "value": "23",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Skyline",
                                "emoji": True,
                            },
                            "value": "24",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Specialized",
                                "emoji": True,
                            },
                            "value": "25",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Star Elevator",
                                "emoji": True,
                            },
                            "value": "26",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "TAKA",
                                "emoji": True,
                            },
                            "value": "27",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "TEC",
                                "emoji": True,
                            },
                            "value": "28",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "TEI",
                                "emoji": True,
                            },
                            "value": "29",
                        },
                        {
                            "text": {"type": "plain_text", "text": "TK", "emoji": True},
                            "value": "30",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "VTS",
                                "emoji": True,
                            },
                            "value": "31",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Unknown",
                                "emoji": True,
                            },
                            "value": "999",
                        },
                    ],
                },
            },
            {
                "type": "input",
                "block_id": "client",
                "label": {"type": "plain_text", "text": "Client", "emoji": True},
                "optional": False,
                "dispatch_action": True,
                "element": {
                    "type": "static_select",
                    "action_id": "client_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a client",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "EOS Hospitality",
                                "emoji": True,
                            },
                            "value": "12",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Nuveen",
                                "emoji": True,
                            },
                            "value": "24",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Starwood Capital Group",
                                "emoji": True,
                            },
                            "value": "30",
                        },
                    ],
                },
            },
            {
                "type": "input",
                "block_id": "location",
                "label": {"type": "plain_text", "text": "Location", "emoji": True},
                "optional": False,
                "dispatch_action": False,
                "element": {
                    "type": "static_select",
                    "action_id": "location_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a location",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Rosslyn Overlook - 1616 North Fort Myer Drive",
                                "emoji": True,
                            },
                            "value": "493",
                        }
                    ],
                },
            },
            {"type": "divider", "block_id": "XVd6O"},
            {
                "type": "input",
                "block_id": "doc_id",
                "label": {"type": "plain_text", "text": "Document ID", "emoji": True},
                "optional": False,
                "dispatch_action": False,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                    "dispatch_action_config": {
                        "trigger_actions_on": ["on_enter_pressed"]
                    },
                },
            },
            {
                "type": "input",
                "block_id": "scope",
                "label": {
                    "type": "plain_text",
                    "text": "Scope / Description",
                    "emoji": True,
                },
                "optional": False,
                "dispatch_action": False,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                    "multiline": True,
                    "dispatch_action_config": {
                        "trigger_actions_on": ["on_enter_pressed"]
                    },
                },
            },
            {
                "type": "input",
                "block_id": "cost",
                "label": {"type": "plain_text", "text": "Total Price", "emoji": True},
                "optional": False,
                "dispatch_action": False,
                "element": {
                    "type": "number_input",
                    "action_id": "number_input-action",
                    "is_decimal_allowed": False,
                },
            },
            {"type": "divider", "block_id": "Fbg0j"},
        ],
        "private_metadata": "",
        "callback_id": "doc_process",
        "state": {
            "values": {
                "file_upload": {
                    "file_input_action_id_1": {
                        "type": "file_input",
                        "files": [
                            {
                                "id": "F06RL4U69M4",
                                "created": 1711627229,
                                "timestamp": 1711627229,
                                "name": "29n-130sfpp-6cars-CIBSE-UP-80-20-20.pdf",
                                "title": "29n-130sfpp-6cars-CIBSE-UP-80-20-20.pdf",
                                "mimetype": "application/pdf",
                                "filetype": "pdf",
                                "pretty_type": "PDF",
                                "user": "UGFL0UGGN",
                                "user_team": "T0331TJV7",
                                "editable": False,
                                "size": 1093938,
                                "mode": "hosted",
                                "is_external": False,
                                "external_type": "",
                                "is_public": False,
                                "public_url_shared": False,
                                "display_as_bot": False,
                                "username": "",
                                "url_private": "https://files.slack.com/files-pri/T0331TJV7-F06RL4U69M4/29n-130sfpp-6cars-cibse-up-80-20-20.pdf",
                                "url_private_download": "https://files.slack.com/files-pri/T0331TJV7-F06RL4U69M4/download/29n-130sfpp-6cars-cibse-up-80-20-20.pdf",
                                "media_display_type": "unknown",
                                "thumb_pdf": "https://files.slack.com/files-tmb/T0331TJV7-F06RL4U69M4-a45984aad9/29n-130sfpp-6cars-cibse-up-80-20-20_thumb_pdf.png",
                                "thumb_pdf_w": 909,
                                "thumb_pdf_h": 1285,
                                "permalink": "https://gravityholdings.slack.com/files/UGFL0UGGN/F06RL4U69M4/29n-130sfpp-6cars-cibse-up-80-20-20.pdf",
                                "permalink_public": "https://slack-files.com/T0331TJV7-F06RL4U69M4-a8ea6a2cc6",
                                "comments_count": 0,
                                "shares": {},
                                "channels": [],
                                "groups": [],
                                "ims": [],
                                "has_more_shares": False,
                                "has_rich_preview": False,
                                "file_access": "visible",
                            }
                        ],
                    }
                },
                "originator": {
                    "plain_text_input-action": {
                        "type": "plain_text_input",
                        "value": "asd",
                    }
                },
                "vendor": {
                    "vendor_select": {
                        "type": "static_select",
                        "selected_option": {
                            "text": {
                                "type": "plain_text",
                                "text": "ELCON",
                                "emoji": True,
                            },
                            "value": "6",
                        },
                    }
                },
                "client": {
                    "client_select": {
                        "type": "static_select",
                        "selected_option": {
                            "text": {
                                "type": "plain_text",
                                "text": "Nuveen",
                                "emoji": True,
                            },
                            "value": "24",
                        },
                    }
                },
                "location": {
                    "location_select": {
                        "type": "static_select",
                        "selected_option": {
                            "text": {
                                "type": "plain_text",
                                "text": "Rosslyn Overlook - 1616 North Fort Myer Drive",
                                "emoji": True,
                            },
                            "value": "493",
                        },
                    }
                },
                "doc_id": {
                    "plain_text_input-action": {
                        "type": "plain_text_input",
                        "value": "asd",
                    }
                },
                "scope": {
                    "plain_text_input-action": {
                        "type": "plain_text_input",
                        "value": "asd",
                    }
                },
                "cost": {
                    "number_input-action": {"type": "number_input", "value": "12"}
                },
            }
        },
        "hash": "1711627234.8stnF1cQ",
        "title": {"type": "plain_text", "text": "Document Processing", "emoji": True},
        "clear_on_close": False,
        "notify_on_close": False,
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "previous_view_id": None,
        "root_view_id": "V06RPRV95E1",
        "app_id": "A06KV1TBUEQ",
        "external_id": "",
        "app_installed_team_id": "T0331TJV7",
        "bot_id": "B06KCBZ4CNB",
    },
    "response_urls": [],
    "is_enterprise_install": False,
    "enterprise": None,
}

{'parser': {'Directory': OrderedDict({'1.2': <class 'pluginlib.importer.plugins.directories.Directories'>}), 'DocProcess': OrderedDict({'0.1': <class 'pluginlib.importer.plugins.doc_process.DocProcess'>}), 'FileParser': OrderedDict({'1.0': <class 'pluginlib.importer.plugins.file_parser.FileParser'>}), 'pdf2img': OrderedDict({'1.0': <class 'pluginlib.importer.plugins.pdf2img.Pdf2Img'>}), 'SlackChannelInfo': OrderedDict({'1.2': <class 'pluginlib.importer.plugins.slackchannelinfo.SlackChannelInfo'>}), 'SlackFileInfo': OrderedDict({'1.2': <class 'pluginlib.importer.plugins.slackfileinfo.SlackFileInfo'>}), 'SlackUserInfo': OrderedDict({'1.2': <class 'pluginlib.importer.plugins.slackuserinfo.SlackUserInfo'>}), 'Zipper': OrderedDict({'1.3': <class 'pluginlib.importer.plugins.zipper.Zipper'>})}, 'slackevent': {'MessageEvent': OrderedDict({'1.0': <class 'pluginlib.importer.plugins.message_event.MessageEvent'>})}, 'files': {'FileHandler': OrderedDict({'1.0': <class 'pluginlib.importer.plugins.file_handler.FileHandler'>})}, 'Database': {}, 'eventlogger': {'EventLogger': OrderedDict({'1.0': <class 'pluginlib.importer.plugins.eventlogger.EventLogger'>})}}