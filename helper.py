"""Helper."""

__doc__ = """
helper.py

helper functions.
"""

import time


def wait_with_print(duration=1):
    """Wait with print."""
    step_duration = 0.5
    waiting_duration = 0
    while waiting_duration < duration:
        # print(". ", end='', flush=True)
        print(".", end='')
        time.sleep(step_duration)
        waiting_duration += step_duration
    print("")


def time_measurement_call(message, test_function, loop_count=1000):
    """Measure timing."""
    duration = 0
    start_time = time.monotonic()
    for _index in range(loop_count):
        start_time = time.monotonic()
        test_function()
        end_time = time.monotonic()
        duration += end_time - start_time
    print(
        "{call_duration:>8.2f}ms\t{message}"
        "".format(
            call_duration=(duration / loop_count) * 1000,
            message=message,
        )
    )
