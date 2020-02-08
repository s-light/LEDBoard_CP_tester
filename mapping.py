"""Mapping."""

__doc__ = """
mapping.py - Mapping.

some mapping helpers.
"""


"""
The MIT License (MIT)

Copyright (c) 2020 Stefan Krüger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def map_range(x, in_min, in_max, out_min, out_max):
    """Map Value from one range to another."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_range_int(x, in_min, in_max, out_min, out_max):
    """Map Value from one range to another."""
    return int(
        (x - in_min) * (out_max - out_min)
        //
        (in_max - in_min) + out_min
    )


##########################################

def multi_map(val, array_in, array_out):
    """Map value."""
    result = None

    if (val <= array_in[0]):
        return array_out[0]
    if (val >= array_in[-1]):
        return array_out[-1]

    # search right interval
    # array_in[0] allready tested
    pos = 1
    while (val > array_in[pos]):
        pos += 1

    # this will handle all exact "points" in array_in
    if (val == array_in[pos]):
        return array_out[pos]

    # interpolate in the right segment for the rest
    result = map_range(
        val,
        array_in[pos-1], array_in[pos],
        array_out[pos-1], array_out[pos]
    )
    return result


def multi_map_tuple(val, array):
    """Map value."""
    result = None

    if (val <= array[0][0]):
        result = array[0][1]
    if (val >= array[-1][0]):
        result = array[-1][1]

    # search right interval
    # array[0][0] allready tested
    pos = 1
    while (val > array[pos][0]):
        pos += 1

    # this will handle all exact "points"
    if (val == array[pos][0]):
        result = array[pos][0]

    # interpolate in the right segment for the rest

    out_low = array[pos-1][1]
    out_hig = array[pos][1]
    # print("out_low", out_low)
    try:
        temp = []
        for tuple_index in range(len(out_low)):
            # print("out_low[tuple_index]", out_low[tuple_index])
            temp.append(map_range(
                val,
                array[pos-1][0], array[pos][0],
                out_low[tuple_index], out_hig[tuple_index]
            ))
        result = tuple(temp)
        # print("temp", temp)
        # print("result", result)
    except TypeError as e:
        print("TypeError: ", e)
        result = map_range(
            val,
            array[pos-1][0], array[pos][0],
            out_low, out_hig
        )
    # print("result", result)
    return result


class MultiMap(object):
    """MultiMap."""

    def __init__(self, array_in, array_out):
        """Init."""
        super(MultiMap, self).__init__()
        self.array_in = array_in
        self.array_out = array_out

    def mapit(self, val):
        """Map value."""
        result = None

        if (val <= self.array_in[0]):
            return self.array_out[0]
        if (val >= self.array_in[N-1]):
            return self.array_out[N-1]

        # search right interval
        # self.array_in[0] allready tested
        pos = 1
        while (val > self.array_in[pos]):
            pos += 1

        # this will handle all exact "points" in array_in
        if (val == self.array_in[pos]):
            return self.array_out[pos]

        # interpolate in the right segment for the rest
        result = map_range(
            val,
            self.array_in[pos-1], self.array_in[pos],
            self.array_out[pos-1], self.array_out[pos]
        )
        return result

##########################################
