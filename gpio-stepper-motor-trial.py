"""
/*
MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

GPLv3 License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

# Notes on the Purpose of This Demo Code
# Author: Fred Fisher, Validus Group Inc. (www.validusgroup.com)
# Copyright 2025


# This is purely demo code to demonstrate why a "bit bang" approach (e.g.,
# toggling all lines at once without accounting for timing variations)
# can lead to unexpected behavior in motor control systems. The internals
# of the kernel and the scheduling of GPIO tasks can significantly affect
# the precision and consistency of output pulses.

# Compatibility Notes:
# - libgpiod version used: 1.6.3
# - gpiod (Python library) version: 1.5.4
# - Python 3.10.15
# - BeagleBone Black industrial
# - Arago OS, Linux beaglebone 6.1.80-ti #1 SMP PREEMPT Fri Mar 22 02:57:54 UTC 2024


# Observation Tips:
# - Watch the motor and watch the pulse signal response on a scope to see 
#   how pulse width and timing variations impact the motor's behavior.
# - Adjust the frequency variable and observe how the motor speed and
#   consistency change with different pulse settings.

# Disclaimer:
# This demo code is provided as-is for educational purposes. Validus Group
# Inc. and Fred Fisher assume no liability for misuse or unintended outcomes.
# Please ensure proper safety measures are in place when using this code
# in a hardware environment.
"""


import gpiod
import time

CHIP_PATH_OUTPUT = "/dev/gpiochip0"  # Chip for P8_12 (Pulse)
CHIP_PATH_DIRECTION = "/dev/gpiochip1"  # Chip for P8_10 (Direction)
CHIP_PATH_ENABLE = "/dev/gpiochip1"  # Chip for P8_8 (Enable)
LINE_OFFSET_OUTPUT = 12                # GPIO line offset for P8_12 (Pulse)
LINE_OFFSET_DIRECTION = 4              # GPIO line offset for P8_10 (Direction)
LINE_OFFSET_ENABLE = 3                 # GPIO line offset for P8_8 (Enable)

# Motor parameters
pulses_per_rotation = 400  # Pulses per rotation
frequency = 100        # Frequency in Hz (pulses per second)
period = 1.0 / frequency   # Period in seconds
half_period = period / 2   # Half-period for 50% duty cycle


def main():
    # Open the GPIO chips
    chip_output = gpiod.chip(CHIP_PATH_OUTPUT)  # For P8_12
    chip_direction = gpiod.chip(CHIP_PATH_DIRECTION)  # For P8_10
    chip_enable = gpiod.chip(CHIP_PATH_ENABLE)  # For P8_8
    print(f"Opened GPIO chips: {CHIP_PATH_OUTPUT}, {CHIP_PATH_DIRECTION}, and {CHIP_PATH_ENABLE}")

    # Access the GPIO lines
    output_line = chip_output.get_line(LINE_OFFSET_OUTPUT)
    direction_line = chip_direction.get_line(LINE_OFFSET_DIRECTION)
    enable_line = chip_enable.get_line(LINE_OFFSET_ENABLE)

    # Check lines
    if not output_line:
        raise RuntimeError(f"Failed to access line {LINE_OFFSET_OUTPUT} on chip {CHIP_PATH_OUTPUT}")
    if not direction_line:
        raise RuntimeError(f"Failed to access line {LINE_OFFSET_DIRECTION} on chip {CHIP_PATH_DIRECTION}")
    if not enable_line:
        raise RuntimeError(f"Failed to access line {LINE_OFFSET_ENABLE} on chip {CHIP_PATH_ENABLE}")

    print(f"Accessed GPIO lines: {LINE_OFFSET_OUTPUT}, {LINE_OFFSET_DIRECTION}, {LINE_OFFSET_ENABLE}")

    # Configure line requests
    config = gpiod.line_request()
    config.consumer = "motor_control"
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT

    output_line.request(config)
    direction_line.request(config)
    enable_line.request(config)

    try:
        while True:
            # Enable the motor (inverted logic: LOW = Enabled)
            enable_line.set_value(0)
            print("Motor Enabled (Enable Line = 0)")

            # Rotate forward
            direction_line.set_value(0)  # Set direction to forward
            print("Direction: Forward")
            for _ in range(pulses_per_rotation):
                output_line.set_value(1)  # Pulse HIGH
                time.sleep(half_period)
                output_line.set_value(0)  # Pulse LOW
                time.sleep(half_period)

            # Small delay between direction changes
            time.sleep(0.5)

            # Rotate backward
            direction_line.set_value(1)  # Set direction to backward
            print("Direction: Backward")
            for _ in range(pulses_per_rotation):
                output_line.set_value(1)  # Pulse HIGH
                time.sleep(half_period)
                output_line.set_value(0)  # Pulse LOW
                time.sleep(half_period)

            # Small delay before next loop
            time.sleep(0.5)

            # Disable the motor (inverted logic: HIGH = Disabled)
            enable_line.set_value(1)
            print("Motor Disabled (Enable Line = 1)")
            time.sleep(1)  # Pause before next rotation cycle

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Ensure all lines are set to safe states before exiting
        print("Disabling motor and setting pins to LOW before exit.")
        output_line.set_value(0)
        direction_line.set_value(0)
        enable_line.set_value(1)  # Ensure motor is disabled (Enable Line = 1)
        output_line.release()
        direction_line.release()
        enable_line.release()
        print("GPIO lines released and motor stopped.")

if __name__ == "__main__":
    main()
