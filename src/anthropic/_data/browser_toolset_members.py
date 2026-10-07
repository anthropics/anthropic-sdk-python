from typing import Dict, Optional
from typing_extensions import Required, TypedDict


class BrowserToolsetMembers(TypedDict, total=False):
    confirm_required: Required[bool]

    confirmation: Required[Optional[str]]

    enabled_by_default: Required[bool]

    result: Required[str]


BROWSER_TOOLSET_MEMBERS: Dict[str, BrowserToolsetMembers] = {
    "navigate": {
        "result": "navigate",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "screenshot": {
        "result": "screenshot",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "zoom": {
        "result": "screenshot",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "left_click": {
        "result": "none",
        "confirmation": "Clicked.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "right_click": {
        "result": "none",
        "confirmation": "Right-clicked.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "middle_click": {
        "result": "none",
        "confirmation": "Middle-clicked.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "double_click": {
        "result": "none",
        "confirmation": "Double-clicked.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "triple_click": {
        "result": "none",
        "confirmation": "Triple-clicked.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "hover": {
        "result": "none",
        "confirmation": "Hovered.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "left_click_drag": {
        "result": "none",
        "confirmation": "Dragged.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "left_mouse_down": {
        "result": "none",
        "confirmation": "Mouse button pressed.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "left_mouse_up": {
        "result": "none",
        "confirmation": "Mouse button released.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "mouse_move": {
        "result": "none",
        "confirmation": "Moved the mouse.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "scroll": {
        "result": "none",
        "confirmation": "Scrolled {scroll_direction}.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "scroll_to": {
        "result": "none",
        "confirmation": "Scrolled to {ref}.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "type": {
        "result": "none",
        "confirmation": "Typed.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "key": {
        "result": "none",
        "confirmation": "Pressed {text}.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "hold_key": {
        "result": "none",
        "confirmation": "Held {text} for {duration}s.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "form_input": {
        "result": "none",
        "confirmation": "Set the value of {ref}.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "read_page": {
        "result": "text",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "find": {
        "result": "text",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "get_page_text": {
        "result": "text",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "wait": {
        "result": "none",
        "confirmation": "Waited {duration}s.",
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "file_upload": {
        "result": "none",
        "confirmation": "Uploaded.",
        "enabled_by_default": False,
        "confirm_required": True,
    },
    "read_console": {
        "result": "text",
        "confirmation": None,
        "enabled_by_default": False,
        "confirm_required": False,
    },
    "read_network": {
        "result": "text",
        "confirmation": None,
        "enabled_by_default": False,
        "confirm_required": False,
    },
    "javascript_exec": {
        "result": "text",
        "confirmation": None,
        "enabled_by_default": False,
        "confirm_required": True,
    },
    "new_tab": {
        "result": "tab",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "list_tabs": {
        "result": "tabs",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "switch_tab": {
        "result": "tab",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
    "close_tab": {
        "result": "none",
        "confirmation": None,
        "enabled_by_default": True,
        "confirm_required": False,
    },
}
