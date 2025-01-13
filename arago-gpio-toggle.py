"""
Dual License: MIT and GPLv3

MIT License:
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:
This software is provided "AS IS", without warranty of any kind.

GPLv3 License:
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.
See <https://www.gnu.org/licenses/> for details.

Author: Fred Fisher
Company: Validus Group Inc.
Website: www.validusgroup.com

====================================================================================
NOTES:
- Tested on Texas Instruments' Yocto Kirkstone Build (Arago Distribution)
- Kernel: Linux beaglebone 6.1.80-ti #1 SMP PREEMPT Fri Mar 22 02:57:54 UTC 2024 armv7l
- Required Packages:
  - Python 3.10 or newer
  - `gpiod` Python library version 1.5.4 (compatible with `libgpiod` 1.6.3)
  - `libgpiod` version 1.6.3
- Ensure `/dev/gpiochip0` is accessible with appropriate permissions.
- Example command to verify GPIO access: `gpiodetect`

This must be installed after board is up.
pip3 install gpiod==1.5.4

====================================================================================
"""

import gpiod
import time

CHIP_PATH = "/dev/gpiochip0"  # Adjust if needed
LINE_OFFSET = 12             # GPIO line offset for P8_12

def main():
    # Open the GPIO chip
    chip = gpiod.chip(CHIP_PATH)  # Use lowercase 'chip'
    print(f"Opened GPIO chip: {CHIP_PATH}")

    # Access the GPIO line
    line = chip.get_line(LINE_OFFSET)
    if not line:
        raise RuntimeError(f"Failed to access line {LINE_OFFSET} on chip {CHIP_PATH}")
    print(f"Accessing GPIO line: {LINE_OFFSET}")

    # Configure line request
    config = gpiod.line_request()
    config.consumer = "gpio_toggle"
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT

    # Request the line with configuration
    line.request(config)
    print(f"GPIO line {LINE_OFFSET} set as output.")

    # Toggle the GPIO line in a loop
    try:
        while True:
            line.set_value(1)  # Set line HIGH
            print("Line HIGH")
            time.sleep(0.5)

            line.set_value(0)  # Set line LOW
            print("Line LOW")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")

    # Release the line
    line.release()

if __name__ == "__main__":
    main()
