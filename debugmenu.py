"""DebugMenu."""

__doc__ = """
debugmenu.py

serial debug menu handling.
"""

import time

import board
import busio
import supervisor


##########################################
if __name__ == '__main__':
    print()
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print()


##########################################

class MyDebugMenu(object):
    """MyDebugMenu."""

    def __init__(self, animation):
        """Init."""
        super(MyDebugMenu, self).__init__()
        self.animation = animation

    def handle_pixel_set(self, input_string):
        """Handle Pixel Set."""
        pixel = 0
        value = 0
        sep = input_string.find(":")
        try:
            pixel = int(input_string[1:sep])
        except ValueError as e:
            print("Exception parsing 'pixel': ", e)
        try:
            value = int(input_string[sep+1:])
        except ValueError as e:
            print("Exception parsing 'value': ", e)
        self.animation.pixels.set_pixel_16bit_value(pixel, value, value, value)
        self.animation.pixels.show()

    def handle_pixel_map_set(self, input_string):
        """Handle Pixel Set."""
        row = 0
        col = 0
        value = 0

        sep_pos = input_string.find(",")
        sep_value = input_string.find(":")
        try:
            col = int(input_string[1:sep_pos])
        except ValueError as e:
            print("Exception parsing 'col': ", e)
        try:
            row = int(input_string[sep_pos+1:sep_value])
        except ValueError as e:
            print("Exception parsing 'row': ", e)
        try:
            value = int(input_string[sep_value+1:])
        except ValueError as e:
            print("Exception parsing 'value': ", e)
        pixel_index = 0
        try:
            pixel_index = pmap.map(col=col, row=row)
        except IndexError as e:
            print("{}; col:'{:>3}' row:'{:>3}'".format(e, col, row))

        print(
            "pixel_index:'{:>3}' col:'{:>3}' row:'{:>3}'"
            "".format(pixel_index, col, row)
        )
        self.animation.pixels.set_pixel_16bit_value(
            pixel_index, value, value, value)
        self.animation.pixels.show()

    def handle_row_set(self, input_string):
        """Handle row set."""
        row_index = 0
        value = 0.0
        brightness = 1.0

        sep_value = input_string.find(":")
        try:
            row_index = int(input_string[1:sep_value])
        except ValueError as e:
            print("Exception parsing 'row': ", e)

        sep_pos = input_string.find(",")
        try:
            if sep_pos is -1:
                value = float(input_string[sep_value+1:])
            else:
                value = float(input_string[sep_value+1:sep_pos])
        except ValueError as e:
            print("Exception parsing 'value': ", e)
        try:
            brightness = float(input_string[sep_pos+1:])
        except ValueError as e:
            print("Exception parsing 'brightness': ", e)
        # sep_pos = input_string.find(",")

        print(
            "row:{:2} "
            "value:{} "
            "brightness:{} "
            "".format(
                row_index,
                value,
                brightness,
            )
        )

        color = fancyled.CHSV(
            h=value,
            s=1.0,
            v=brightness
        )
        self.animation.set_row_color(row_index, color)
        self.animation.pixels.show()

    def handle_brightness(self, input_string):
        """Handle brightness set."""
        value = 0
        try:
            value = float(input_string[1:])
        except ValueError as e:
            print("Exception parsing 'value': ", e)
        self.animation.brightness = value

    def handle_speed(self, input_string):
        """Handle brightness set."""
        value = 0
        try:
            value = float(input_string[1:])
        except ValueError as e:
            print("Exception parsing 'value': ", e)
        self.animation.speed = value

    def print_help(self):
        """Print Help."""
        print(
            "you can set some options:\n"
            "- single pixel by index: 'p18:500'\n"
            "- single pixel by col row: 'm2,5:500'\n"
            "- full row: 'r2:0.1'\n"
            "- toggle animation: 'a'\n"
            "- set brightness: 'b{}'\n"
            "- set speed: 's{}'\n"
            "- update animation: 'u'\n"
            "".format(
                self.animation.brightness,
                self.animation.speed
            )
        )

    def check_input(self):
        """Check Input."""
        input_string = input()
        if "p" in input_string:
            self.handle_pixel_set(input_string)
        if "m" in input_string:
            self.handle_pixel_map_set(input_string)
        if "r" in input_string:
            self.handle_row_set(input_string)
        if "a" in input_string:
            self.animation.animation_run = not self.animation.animation_run
        if "b" in input_string:
            self.handle_brightness(input_string)
        if "s" in input_string:
            self.handle_speed(input_string)
        if "u" in input_string:
            self.animation.update_animation()
        # prepare new input
        # print("enter new values:")
        self.print_help()
        print(">> ", end="")

    def update(self):
        """Loop."""
        if supervisor.runtime.serial_bytes_available:
            self.check_input()


##########################################
# main loop
#
# if __name__ == '__main__':
#     # nothing to do
