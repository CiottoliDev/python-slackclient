import json
from abc import ABCMeta
from functools import wraps
from typing import Callable, Iterable

from ...errors import SlackObjectFormationError


class BaseObject:
    def __str__(self):
        return f"<slack.{self.__class__.__name__}>"


class JsonObject(BaseObject, metaclass=ABCMeta):

    def validate_json(self) -> None:
        """
        Raises:
          SlackObjectFormationError if the object was not valid
        """
        for attribute in (func for func in dir(self) if not func.startswith("__")):
            method = getattr(self, attribute)
            if callable(method) and hasattr(method, "validator"):
                method()

    @staticmethod
    def __get_non_null_attributes(dict_: dict) -> dict:
        """
        Construct a dictionary out of non-null keys (from attributes property)
        present on this object
        """
        return {key: value for key, value in dict_.items() if value is not None}

    def to_dict(self, *args) -> dict:
        self.validate_json()
        _json = json.dumps(self, default=lambda o: o.__dict__)
        _dict = json.loads(_json, object_hook=self.__get_non_null_attributes)

        return _dict

    def __repr__(self):
        _json = self.to_dict()
        if _json:
            return f"<slack.{self.__class__.__name__}: {_json}>"
        else:
            return self.__str__()


class JsonValidator:
    def __init__(self, message: str):
        """
        Decorate a method on a class to mark it as a JSON validator. Validation
            functions should return true if valid, false if not.

        Args:
            message: Message to be attached to the thrown SlackObjectFormationError
        """
        self.message = message

    def __call__(self, func: Callable) -> Callable[..., None]:
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            if not func(*args, **kwargs):
                raise SlackObjectFormationError(self.message)

        wrapped_f.validator = True
        return wrapped_f


class EnumValidator(JsonValidator):
    def __init__(self, attribute: str, enum: Iterable[str]):
        super().__init__(
            f"{attribute} attribute must be one of the following values: "
            f"{', '.join(enum)}"
        )

# def extract_json(item_or_items: Union[JsonObject, List[JsonObject], str], *format_args
# ) -> Union[dict, List[dict], str]:
#     """
#     Given a sequence (or single item), attempt to call the to_dict() method on each
#     item and return a plain list. If item is not the expected type, return it
#     unmodified, in case it's already a plain dict or some other user created class.
#
#     Args:
#       item_or_items: item(s) to go through
#       format_args: Any formatting specifiers to pass into the object's to_dict
#             method
#     """
#     try:
#         return [
#             elem.to_dict(*format_args) if isinstance(elem, JsonObject) else elem
#             for elem in item_or_items
#         ]
#     except TypeError:  # not iterable, so try returning it as a single item
#         return (
#             item_or_items.to_dict(*format_args)
#             if isinstance(item_or_items, JsonObject)
#             else item_or_items
#         )
