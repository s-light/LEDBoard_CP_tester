"""TLC5971 & FancyLED."""

__doc__ = """
animation.py - TLC5971 & FancyLED & 2D Array / Mapping.

it combines the TLC5971 library with FancyLED and 2D Array / Mapping.

Enjoy the colors :-)
"""

import board
import busio
import supervisor

from adafruit_tlc59711.adafruit_tlc59711_multi import TLC59711Multi
import adafruit_fancyled.adafruit_fancyled as fancyled
from pixel_map import PixelMap2D

from mapping import map_range
from mapping import multi_map
from mapping import multi_map_tuple
from mapping import MultiMap

from helper import wait_with_print
from helper import time_measurement_call


##########################################
if __name__ == '__main__':
    print()
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print()

##########################################
print(42 * '*')
print("define pixel array / init TLC5971")

##########################################
# mappings
# LEDBoard_4x4_16bit mapping

LEDBoard_col_count = 4
LEDBoard_row_count = 4
LEDBoard_pixel_count = LEDBoard_row_count * LEDBoard_col_count
LEDBoard_single = [
    [15, 14, 11, 10],
    [13, 12, 9, 8],
    [7, 6, 3, 2],
    [5, 4, 1, 0],
]

LEDBoard_single_90deg = [
    [10, 8, 2, 0],
    [11, 9, 3, 1],
    [14, 12, 6, 4],
    [15, 13, 7, 5],
]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# boad layout
Boards_col_count = 1
Boards_row_count = 1
Boards_positions = [
    [0, 1],
    [2, 3],
]
Boards_pos_type = [
    [1, 0],
    [0, 0],
]

# Boards_col_count = 4
# Boards_row_count = 4
# Boards_positions = [
#     [12, 8, 4, 0],
#     [13, 9, 5, 1],
#     [14, 10, 6, 2],
#     [15, 11, 7, 3],
# ]
# Boards_pos_type = [
#     [0, 1, 1, 0],
#     [0, 1, 1, 0],
#     [0, 1, 1, 0],
#     [0, 1, 1, 0],
# ]

Boards_count = Boards_col_count * Boards_row_count
Matrix_col_count = LEDBoard_col_count * Boards_col_count
Matrix_row_count = LEDBoard_row_count * Boards_row_count
Matrix_pixel_count = Matrix_col_count * Matrix_row_count


def mymap_LEDBoard_4x4_16bit(self, *, col=0, row=0):
    """Map row and col to pixel_index."""
    # get Board position
    board_col = col // LEDBoard_col_count
    board_row = row // LEDBoard_row_count
    board_sub_col = col % LEDBoard_col_count
    board_sub_row = row % LEDBoard_row_count

    board_offset = Boards_positions[board_row][board_col]
    board_type = Boards_pos_type[board_row][board_col]
    if board_type == 0:
        pixel_offset = LEDBoard_single[board_sub_row][board_sub_col]
    elif board_type == 1:
        pixel_offset = LEDBoard_single_90deg[board_sub_row][board_sub_col]
    else:
        print("ERROR: board_type {} not implemented.".format(board_type))

    pixel_index = (board_offset * LEDBoard_pixel_count) + pixel_offset

    return pixel_index


pmap = PixelMap2D(
    row_count=Matrix_row_count,
    col_count=Matrix_col_count,
    map_function=mymap_LEDBoard_4x4_16bit
)

##########################################
# led controller

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
pixels = TLC59711Multi(spi, pixel_count=Matrix_pixel_count)


def pixels_init_BCData():
    """Initialise global brightness control data."""
    BCValues = TLC59711Multi.calculate_BCData(
        Ioclmax=18,
        IoutR=18,
        IoutG=11,
        IoutB=13,
    )
    print("BCValues = {}".format(BCValues))
    pixels.bcr = BCValues[0]
    pixels.bcg = BCValues[1]
    pixels.bcb = BCValues[2]
    pixels.update_BCData()
    pixels.show()


##########################################
# Declare a 6-element RGB rainbow palette
palette = [
    fancyled.CRGB(1.0, 0.0, 0.0),  # Red
    fancyled.CRGB(0.5, 0.5, 0.0),  # Yellow
    fancyled.CRGB(0.0, 1.0, 0.0),  # Green
    fancyled.CRGB(0.0, 0.5, 0.5),  # Cyan
    fancyled.CRGB(0.0, 0.0, 1.0),  # Blue
    fancyled.CRGB(0.5, 0.0, 0.5),  # Magenta
]


chakra_diagonal = [
    [(0.00, 1.0, 1.0), (0.10, 1.0, 1.0), (0.13, 1.0, 1.0), (0.25, 1.0, 1.0)],
    [(0.10, 1.0, 1.0), (0.13, 1.0, 1.0), (0.25, 1.0, 1.0), (0.40, 1.0, 1.0)],
    [(0.13, 1.0, 1.0), (0.25, 1.0, 1.0), (0.40, 1.0, 1.0), (0.55, 1.0, 1.0)],
    [(0.25, 1.0, 1.0), (0.40, 1.0, 1.0), (0.55, 1.0, 1.0), (0.76, 1.0, 1.0)],
]

paper_colors_day = [
    # frame
    (0,  (0.15, 0.8, 0.2)),
    (3,  (0.15, 0.8, 0.4)),
    # hills
    (4,  (0.25, 1.0, 0.5)),
    (8, (0.25, 1.0, 0.8)),
    # mountains mid
    (9, (0.3, 0.5, 0.7)),
    (11, (0.3, 0.5, 0.5)),
    # river
    (12, (0.5, 1.0, 0.5)),
    (12, (0.5, 1.0, 0.5)),
    # mountains
    (13, (0.3, 1.0, 1.0)),
    (14, (0.3, 1.0, 1.0)),
    # sky
    (15, (0.5, 0.7, 1.0)),
    (16, (0.5, 0.7, 1.0)),
    # stars
    (17, (0.5, 1.0, 0.0)),
    (19, (0.5, 1.0, 0.0)),
    # unused
    (20, (0.0, 0.0, 0.0)),
    (32, (0.0, 0.0, 0.0)),
]

paper_colors_night = [
    # frame
    (0,  (0.15, 0.8, 0.07)),
    (3,  (0.15, 0.8, 0.1)),
    # hills
    (4,  (0.25, 1.0, 0.1)),
    (8, (0.25, 1.0, 0.2)),
    # mountains mid
    (9, (0.15, 0.8, 0.2)),
    (11, (0.15, 0.8, 0.2)),
    # river
    (12, (0.6, 1.0, 0.2)),
    (12, (0.6, 1.0, 0.2)),
    # mountains
    (13, (0.8, 1.0, 0.4)),
    (14, (0.8, 1.0, 0.4)),
    # sky
    (15, (0.7, 1.0, 0.8)),
    (16, (0.7, 1.0, 0.6)),
    # stars
    (17, (0.14, 0.9, 1.0)),
    (19, (0.14, 0.9, 1.0)),
    # unused
    (20, (0.0, 0.0, 0.0)),
    (32, (0.0, 0.0, 0.0)),
]

##########################################

class MyAnimation(object):
    """MyAnimation."""

    def __init__(self):
        """Init."""
        super(MyAnimation, self).__init__()
        self.pixels = pixels
        self.pmap = pmap

        self.offset = 0
        self.speed = 0.0001
        self.animation_run = True
        # self.animation_run = False
        # self.brightness = 0.001
        self.brightness = 0.02
        self.paper_colors_current = paper_colors_day

    ##########################################
    # animation patterns & test

    @staticmethod
    def test_set_corners_to_colors():
        """Test Function: Set all 4 corners to different collors."""
        print(42 * '*')
        print("set corners to colors")
        pixels[pmap.map(
            col=0,
            row=0
        )] = (0.2, 0.05, 0.0)
        pixels[pmap.map(
            col=0,
            row=Matrix_row_count-1
        )] = (0.1, 0.0, 0.2)
        pixels[pmap.map(
            col=Matrix_col_count-1,
            row=0
        )] = (0.1, 0.2, 0.0)
        pixels[pmap.map(
            col=Matrix_col_count-1,
            row=Matrix_row_count-1
        )] = (0.0, 0.1, 0.2)
        # print("{:>3}:{:>3} = {:>3}".format(0, 0, pmap.map(0, 0)))
        # print("{:>3}:{:>3} = {:>3}".format(0, 7, pmap.map(0, 7)))
        # print("{:>3}:{:>3} = {:>3}".format(15, 0, pmap.map(15, 0)))
        # print("{:>3}:{:>3} = {:>3}".format(15, 7, pmap.map(15, 7)))
        # pixels[pmap.map(0, 0)] = (0.1, 0.01, 0.0)
        # pixels[pmap.map(0, 7)] = (0.01, 0.0, 0.1)
        # pixels[pmap.map(15, 0)] = (0.01, 0.01, 0.0)
        # pixels[pmap.map(15, 7)] = (0.0, 0.01, 0.1)
        pixels.show()

    def set_chakra_colors(self):
        """Set chakra colors"""
        print(42 * '*')
        print("set chakra colors")
        for x in range(Matrix_col_count):
            for y in range(Matrix_row_count):
                pixel_index = 0
                try:
                    pixel_index = pmap.map(col=x, row=y)
                except IndexError as e:
                    print("{}; col:{col} row:{row}".format(e, col=x, row=y))
                # color = chakra_diagonal[x][y]
                color = fancyled.CHSV(*chakra_diagonal[x][y])
                color_r, color_g, color_b = fancyled.gamma_adjust(
                    color,
                    brightness=self.brightness
                )
                pixels.set_pixel_float_value(
                    pixel_index,
                    color_r, color_g, color_b
                )

        pixels.show()
        pixels.show()

    @staticmethod
    def test_set_2d_colors():
        """Test Function: Set all LEDs to 2D color-range."""
        print("set color range")
        for x in range(Matrix_col_count):
            # xN = x / Matrix_col_count
            xN = map_range_int(x, 0, Matrix_col_count, 1, 500)
            for y in range(Matrix_row_count):
                # yN = y / Matrix_row_count
                yN = map_range_int(y, 0, Matrix_row_count, 1, 500)
                # print(
                #     "x: {:>2} xN: {:>2} "
                #     "y: {:>2} yN: {:>2} "
                #     "pixel_index: {:>2}".format(
                #         x, xN,
                #         y, yN,
                #         get_pixel_index_from_row_col(x, y)
                #     )
                # )
                pixel_index = 0
                try:
                    pixel_index = pmap.map(col=x, row=y)
                except IndexError as e:
                    print("{}; col:{col} row:{row}".format(e, col=x, row=y))
                pixels[pixel_index] = (xN, yN, 0)

        pixels.show()

    def test_loop_2d_colors(self):
        """Test Function: Set all LEDs to 2D color-range."""
        # Positional offset for blue part
        offsetN = map_range_int(self.offset, 0.0, 1.0, 1, 1000)
        for x in range(Matrix_col_count):
            xN = map_range_int(x, 0, Matrix_col_count, 1, 2000)
            for y in range(Matrix_row_count):
                yN = map_range_int(y, 0, Matrix_row_count, 1, 2000)
                pixels[pmap.map(col=x, row=y)] = (xN, yN, offsetN)
        pixels.show()
        self.offset += 0.001  # Bigger number = faster spin
        if self.offset > 1.0:
            self.offset = 0

    def test_minimal_update(self):
        """Minimal Full Loop with HSV."""
        for row_index in range(Matrix_row_count):
            color = fancyled.CHSV(
                0.5,
                # v=0.05
            )
            color_r, color_g, color_b = fancyled.gamma_adjust(
                color,
                brightness=self.brightness
            )
            for col_index in range(Matrix_col_count):
                pixels.set_pixel_float_value(
                    pmap.map_raw[row_index][col_index],
                    color_r, color_g, color_b
                )
        pixels.show()

    def rainbow_update(self):
        """Rainbow."""
        for row_index in range(Matrix_row_count):
            # Load each pixel's color from the palette using an offset
            # color = fancyled.palette_lookup(
            #     palette,
            #     self.offset + row_index / Matrix_row_count
            #
            # )

            # results in 84,47ms
            # but has not as nice colors...
            # color_r, color_g, color_b = fancyled.CRGB(fancyled.CHSV(
            #     self.offset +
            #     # (row_index / Matrix_row_count),
            #     map_range(
            #         row_index,
            #         0, Matrix_row_count,
            #         0, 1.0
            #     ),
            #     v=0.1
            # ))

            # results in 99.41ms
            color = fancyled.CHSV(
                self.offset +
                # (row_index / Matrix_row_count),
                map_range(
                    row_index,
                    0, Matrix_row_count*2,
                    0, 1.0
                ),
                # v=0.05
            )
            color_r, color_g, color_b = fancyled.gamma_adjust(
                color,
                brightness=self.brightness
            )

            for col_index in range(Matrix_col_count):
                # pixels[pmap.map(col=col_index, row=row_index)] = color
                pixels.set_pixel_float_value(
                    # pmap.map(col=col_index, row=row_index),
                    pmap.map_raw[row_index][col_index],
                    color_r, color_g, color_b
                )
                # pixels.set_pixel_float_value(
                #     pmap.map_raw[row_index][col_index],
                #     0.1,
                #     0.5,
                #     0.5,
                # )
        pixels.show()

    def rainbow_update_offset(self):
        """Rainbow offset."""
        self.offset += self.speed  # Bigger number = faster spin
        if self.offset >= 10:
            self.offset -= 10

    def test_paper1_update(self):
        """Test."""
        my_row_count = Matrix_row_count * 2
        my_col_count = int(Matrix_col_count / 2)
        for row_index in range(my_row_count):
            color_raw = multi_map_tuple(row_index, self.paper_colors_current)
            # print("color_raw", color_raw)
            color = fancyled.CHSV(
                h=color_raw[0],
                s=color_raw[1],
                v=color_raw[2],
            )
            # print("color", color)
            # results in 99.41ms
            # color = fancyled.CHSV(
            #     self.offset +
            #     # (row_index / my_row_count),
            #     map_range(
            #         row_index,
            #         0, my_row_count,
            #         0, 1.0
            #     ),
            #     # v=0.05
            # )
            color_r, color_g, color_b = fancyled.gamma_adjust(
                color,
                brightness=self.brightness
            )

            # row_i = row_index
            row_i = int(row_index / 2)
            for col_index in range(my_col_count):
                # print(
                #     "row:{:2}, "
                #     "col:{:2}, "
                #     "".format(row_index, col_index),
                #     end=""
                # )
                col_i = col_index
                if row_index % 2:
                    col_i = my_col_count + col_index
                # print(
                #     "-> "
                #     "row:{:2}, "
                #     "col:{:2}, "
                #     "".format(row_i, col_i)
                # )
                pixels.set_pixel_float_value(
                    pmap.map_raw[row_i][col_i],
                    color_r, color_g, color_b
                )
        pixels.show()

    def test_paper1_update_offset(self):
        """Paper1 offset."""
        max_offset = Matrix_row_count * 2
        self.offset += self.speed  # Bigger number = faster spin
        if self.offset >= max_offset:
            self.offset -= max_offset
            print("offset reset")

    def paper_colors_toggle(self):
        """Toggle Paper colors."""
        if self.paper_colors_current is paper_colors_day:
            print("switched to night")
            self.paper_colors_current = paper_colors_night
        else:
            print("switched to day")
            self.paper_colors_current = paper_colors_day

    ##########################################
    # mapping helper

    def set_pixel_color(self, row_index, col_index, color):
        """Set pixel color."""
        color_r, color_g, color_b = fancyled.gamma_adjust(
            color,
            brightness=self.brightness
        )

        my_col_count = int(Matrix_col_count / 2)
        row = int(row_index / 2)
        col = col_index
        if row_index % 2:
            col = my_col_count + col
        try:
            # pixel_index = pmap.map(col=col, row=row)
            pixel_index = pmap.map_raw[row][col]
        except IndexError as e:
            print(
                "{}; "
                "row:'{:>3}' "
                "col:'{:>3}' "
                "".format(e, col, row)
            )
        # try:
        #     pixel_index = self.animation.pmap.map(col=col, row=row)
        # except IndexError as e:
        #     print("{}; col:'{:>3}' row:'{:>3}'".format(e, col, row))
        pixels.set_pixel_float_value(
            pixel_index,
            color_r, color_g, color_b
        )
        return pixel_index

    def set_row_color(self, row_index, color):
        """Set row color."""
        color_r, color_g, color_b = fancyled.gamma_adjust(
            color,
            brightness=self.brightness
        )

        # set all columns to same value
        my_col_count = int(Matrix_col_count / 2)
        row = int(row_index / 4)
        for col_index in range(my_col_count):
            col = col_index
            if row_index % 2:
                col = my_col_count + col
            try:
                # pixel_index = pmap.map(col=col, row=row)
                pixel_index = pmap.map_raw[row][col]
            except IndexError as e:
                print(
                    "{}; "
                    "row:'{:>3}' "
                    "col:'{:>3}' "
                    "".format(e, col, row)
                )
            pixels.set_pixel_float_value(
                pixel_index,
                color_r, color_g, color_b
            )

    ##########################################
    # main animation handling

    def update_animation(self):
        """Update animation."""
        # self.test_loop_2d_colors()
        self.rainbow_update()
        self.rainbow_update_offset()
        # self.test_paper1_update()
        # self.test_paper1_update_offset()

    def update(self):
        """Update."""
        if self.animation_run:
            self.update_animation()

    ##########################################
    # time tests

    def time_meassurements(self):
        """Test Main."""

    def time_measurement_rainbow(self):
        """Measure timing."""
        print("*** time measurement - rainbow:")
        loop_count = 20

        def _test():
            self.rainbow_update()
            self.rainbow_update_offset()
        time_measurement_call(
            "'self.rainbow_update()'",
            _test,
            loop_count
        )

    def time_measurement_test1(self):
        """Measure timing."""
        print("*** time measurement - test1:")
        loop_count = 20

        def _test():
            self.test_paper1_update()
            self.test_paper1_update_offset()
        time_measurement_call(
            "'self.test_paper1_update()'",
            _test,
            loop_count
        )

    def time_measurement_minimal(self):
        """Measure timing."""
        print("*** time measurement - minimal full loop with HSV:")
        loop_count = 20

        def _test():
            self.test_minimal_update()
        time_measurement_call(
            "'self.test_minimal_update()'",
            _test,
            loop_count
        )

    def run_test(self):
        """Test Main."""
        # pmap.print_mapping()

        self.pixels.set_pixel_all_16bit_value(1, 1, 1)
        # self.pixels.set_pixel_all_16bit_value(100, 100, 100)
        # self.pixels.show()
        # wait_with_print(1)
        pixels_init_BCData()
        self.pixels.show()
        # wait_with_print(1)

        # self.test_set_corners_to_colors()
        # wait_with_print(1)
        # self.test_set_2d_colors()
        # wait_with_print(1)

        self.time_measurement_minimal()

        self.time_measurement_rainbow()
        self.time_measurement_test1()
        wait_with_print(1)


##########################################
# main loop

if __name__ == '__main__':
    my_animation = MyAnimation()
    my_animation.run_test()
    print(42 * '*')
    print("loop")
    while True:
        my_animation.update()
