import unittest

from slack.web.classes.elements import UserMultiSelectElement
from slack.web.classes.modals import ModalBuilder
from slack.web.classes.objects import PlainTextObject


class TestModals(unittest.TestCase):
    def test_json_form(self):
        modal = ModalBuilder() \
            .title("Test Check title") \
            .submit("Go") \
            .section(text=PlainTextObject(text="Hi, is a test text block in a section")) \
            .divider() \
            .input(label=PlainTextObject(text="Label"),
                   element=UserMultiSelectElement(placeholder=PlainTextObject(text="Select users"),
                                                  action_id="users")) \
            .to_dict()
        coded = {
            "type": "modal",
            "clear_on_close": False,
            "notify_on_close": False,
            "title": {
                "type": "plain_text",
                "text": "Test Check title",
                "emoji": True
            },
            "submit": {
                "text": "Go",
                "type": "plain_text",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Hi, is a test text block in a section",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "optional": False,
                    "element": {
                        "type": "multi_users_select",
                        "action_id": "users",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select users",
                            "emoji": True
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Label",
                        "emoji": True
                    }
                }
            ]
        }
        self.assertDictEqual(modal, coded)
