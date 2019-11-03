import unittest

from slack.errors import SlackObjectFormationError
from slack.web.classes.blocks import (
    ActionsBlock,
    ContextBlock,
    DividerBlock,
    ImageBlock,
    SectionBlock,
)
from slack.web.classes.elements import ButtonElement, ImageElement, LinkButtonElement
from slack.web.classes.objects import PlainTextObject, MarkdownTextObject
from . import STRING_3001_CHARS


class DividerBlockTests(unittest.TestCase):
    def test_json(self):
        self.assertDictEqual(DividerBlock().to_dict(), {"type": "divider"})


class SectionBlockTests(unittest.TestCase):

    def test_json_simple(self):
        section = SectionBlock(text=MarkdownTextObject(text="some text"), block_id="a_block").to_dict()
        json = {
            "text": {"text": "some text", "type": "mrkdwn", "verbatim": False},
            "block_id": "a_block",
            "type": "section",
        }
        self.assertDictEqual(section, json)

    def test_json_with_fields(self):
        self.assertDictEqual(
            SectionBlock(
                text=MarkdownTextObject(text="some text"),
                fields=[MarkdownTextObject(text=f"field{i}") for i in range(5)]
            ).to_dict(),
            {
                "text": {"text": "some text", "type": "mrkdwn", "verbatim": False},
                "fields": [
                    {"text": "field0", "type": "mrkdwn", "verbatim": False},
                    {"text": "field1", "type": "mrkdwn", "verbatim": False},
                    {"text": "field2", "type": "mrkdwn", "verbatim": False},
                    {"text": "field3", "type": "mrkdwn", "verbatim": False},
                    {"text": "field4", "type": "mrkdwn", "verbatim": False},
                ],
                "type": "section",
            },
        )

    def test_json_with_accessory(self):
        button = LinkButtonElement(text=PlainTextObject(text="Click me!"), url="http://google.com")
        section = SectionBlock(text=MarkdownTextObject(text="some text"), accessory=button).to_dict()
        coded = {
            "text": {"text": "some text", "type": "mrkdwn", "verbatim": False},
            "accessory": button.to_dict(),
            "type": "section",
        }
        self.assertDictEqual(section, coded)

    def test_text_or_fields_populated(self):
        with self.assertRaises(SlackObjectFormationError):
            SectionBlock().to_dict()

    def test_fields_length(self):
        with self.assertRaises(SlackObjectFormationError):
            SectionBlock(fields=[MarkdownTextObject(text=f"field{i}") for i in range(11)]).to_dict()


class ImageBlockTests(unittest.TestCase):
    def test_json(self):
        self.assertDictEqual(
            ImageBlock(
                image_url="http://google.com", alt_text="not really an image"
            ).to_dict(),
            {
                "image_url": "http://google.com",
                "alt_text": "not really an image",
                "type": "image",
            },
        )

    def test_image_url_length(self):
        with self.assertRaises(SlackObjectFormationError):
            ImageBlock(image_url=STRING_3001_CHARS, alt_text="text").to_dict()

    def test_alt_text_length(self):
        with self.assertRaises(SlackObjectFormationError):
            ImageBlock(
                image_url="http://google.com", alt_text=STRING_3001_CHARS
            ).to_dict()

    def test_title_length(self):
        with self.assertRaises(SlackObjectFormationError):
            ImageBlock(
                image_url="http://google.com", alt_text="text", title=STRING_3001_CHARS
            ).to_dict()


class ActionsBlockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.elements = [
            ButtonElement(text=PlainTextObject(text="Click me"), action_id="reg_button", value="1"),
            LinkButtonElement(text=PlainTextObject(text="URL Button"), url="http://google.com"),
        ]

    def test_json(self):
        block = ActionsBlock(elements=self.elements).to_dict()
        hard = {"type": "actions", "elements": [e.to_dict() for e in self.elements]}
        self.assertDictEqual(block, hard)

    def test_elements_length(self):
        with self.assertRaises(SlackObjectFormationError):
            ActionsBlock(elements=self.elements * 3).to_dict()


class ContextBlockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.elements = [
            ImageElement(image_url="http://google.com", alt_text="google"),
            PlainTextObject(text="Just text"),
        ]

    def test_basic_json(self):
        d = ContextBlock(elements=self.elements).to_dict()
        e = {
            "elements": [
                {
                    "type": "image",
                    "image_url": "http://google.com",
                    "alt_text": "google",
                },
                {"type": "plain_text", "emoji": True, "text": "Just text"},
            ],
            "type": "context",
        }

        self.assertDictEqual(d, e)

    def test_elements_length(self):
        with self.assertRaises(SlackObjectFormationError):
            ContextBlock(elements=self.elements * 6).to_dict()
