"""Called by "python -m". Allows package to be used as a script.

Example usage:
echo "{red}Red{/red}" |python -m colorclass
"""

from __future__ import print_function

import fileinput
import os

from colorclass.color import Color
from colorclass.toggles import (
    disable_all_colors,
    enable_all_colors,
    set_dark_background,
    set_light_background,
)
from colorclass.windows import Windows

TRUTHY = ("true", "1", "yes", "on")


if __name__ == "__main__":
    if os.environ.get("COLOR_ENABLE", "").lower() in TRUTHY:
        enable_all_colors()
    elif os.environ.get("COLOR_DISABLE", "").lower() in TRUTHY:
        disable_all_colors()
    if os.environ.get("COLOR_LIGHT", "").lower() in TRUTHY:
        set_light_background()
    elif os.environ.get("COLOR_DARK", "").lower() in TRUTHY:
        set_dark_background()
    Windows.enable()
    for LINE in fileinput.input():
        print(Color(LINE))
