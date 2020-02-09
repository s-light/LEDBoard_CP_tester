"""DebugMenu."""

__doc__ = """
debugmenu.py

serial debug menu handling.
"""

import time

import board
import busio
import supervisor

import adafruit_fancyled.adafruit_fancyled as fancyled


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

    ##########################################
    # parser helper

    def parse_value(self, input_string, parse_function, default_value=0):
        """Parse input for two values."""
        result = default_value
        try:
            result = parse_function(input_string)
        except ValueError as e:
            print(
                "Exception parsing '{}': "
                "".format(input_string),
                e
            )
        return result

    def parse_values(self, input_string, parse_function):
        """Parse input for two values."""
        # print("parse_values: '{}'".format(input_string))
        result = []
        start_pos = 0
        seperator_pos = 0
        flag_search = True
        while flag_search:
            seperator_pos = input_string.find(",", seperator_pos+1)
            if seperator_pos == -1:
                string_part = input_string[start_pos:]
            else:
                string_part = input_string[start_pos:seperator_pos]
            result.append(self.parse_value(string_part, parse_function))
            start_pos = seperator_pos + 1
            if seperator_pos == -1:
                flag_search = False
        return tuple(result)

    def parse_color(self, input_string):
        """Parse color."""
        color = fancyled.CHSV(h=0.5, s=1.0, v=1.0)
        values = self.parse_values(input_string, float)
        print("values", values)
        if len(values) is 1:
            # white
            color = fancyled.CHSV(
                h=0.5,
                s=0.0,
                v=values[0]
            )
        elif len(values) is 2:
            # full saturated color
            color = fancyled.CHSV(
                h=values[0],
                s=1.0,
                v=values[1]
            )
        elif len(values) is 3:
            # full color
            color = fancyled.CHSV(
                h=values[0],
                s=values[1],
                v=values[2]
            )

        return color

    ##########################################
    # parser

    def handle_pixel_set(self, input_string):
        """Handle Pixel Set."""
        pixel_index = 0
        value = 0
        sep = input_string.find(":")
        pixel_index = self.parse_value(input_string[1:sep], int)
        value = self.parse_value(input_string[sep+1:], int)
        # try:
        #     pixel_index = int(input_string[1:sep])
        # except ValueError as e:
        #     print("Exception parsing 'pixel_index': ", e)
        # try:
        #     value = int(input_string[sep+1:])
        # except ValueError as e:
        #     print("Exception parsing 'value': ", e)

        print(
            "pixel_index:{:2} "
            "value:{:2} "
            "".format(
                pixel_index,
                value,
            )
        )
        self.animation.pixels.set_pixel_16bit_value(
            pixel_index, value, value, value)
        self.animation.pixels.show()

    def handle_pixel_map_set(self, input_string):
        """Handle Pixel Set."""
        col = 0
        row = 0

        sep_value = input_string.find(":")
        values = self.parse_values(input_string[1:sep_value], int)
        print("values", values)
        try:
            col, row = values
        except ValueError as e:
            print("Exception parsing 'col & row': ", e)

        color = self.parse_color(input_string[sep_value+1:])

        print(
            "col:{:2} "
            "row:{:2} "
            "color:{} "
            "".format(
                col_index,
                row_index,
                color,
            )
        )
        self.animation.set_pixel_color(col, row, color)
        self.animation.pixels.show()

    def handle_test(self, input_string):
        """Handle test."""
        print("test...")
        values = self.parse_values(input_string[1:], int)
        print("values", values)

    def handle_row_set(self, input_string):
        """Handle row set."""
        row_index = 0

        sep_value = input_string.find(":")
        value = self.parse_value(input_string[1:sep_value], int)
        color = self.parse_color(input_string[sep_value+1:])

        print(
            "row:{:2} "
            "color:{} "
            "".format(
                row_index,
                color,
            )
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
            ("*"*42) + "\n"
            "you can set some options:\n"
            "  color:\n"
            "    HSV '0.2,0.5,1.0'\n"
            "    H V '0.2,1.0'\n"
            "      V '1.0'\n"
            "- test: 't12,12'\n"
            "- single pixel by index: 'p14:65000'\n"
            "- single pixel by col row: 'm2,5:color'\n"
            "- full row: 'r2:color'\n"
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
        if "t" in input_string:
            self.handle_test(input_string)
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
