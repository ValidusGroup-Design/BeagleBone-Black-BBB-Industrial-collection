GPIO Toggle Script for BeagleBone Black (BBB)
Overview

This repository provides a Python script for toggling a GPIO pin on a BeagleBone Black (BBB) or similar platforms running Texas Instruments' Yocto Kirkstone Build (Arago Distribution). The script leverages the libgpiod library for direct GPIO access using the GPIO character device interface.

The implementation is designed to work with libgpiod 1.6.3 and Python gpiod bindings version 1.5.4, ensuring compatibility with Yocto-based embedded systems.
Features

    Dual Licensing: Distributed under both MIT and GPLv3 licenses, offering flexibility for both open-source and proprietary use.
    Compatibility:
        Tested on Linux beaglebone 6.1.80-ti running the Arago build of Yocto Kirkstone.
        Supports GPIO access via /dev/gpiochip*.
    GPIO Line Control:
        Configures a specific GPIO line as an output.
        Continuously toggles the GPIO state (HIGH/LOW) at a specified interval.
    Ease of Use:
        Includes detailed notes on required dependencies and setup.
        Example usage and debugging commands provided.

System Requirements

    Hardware: BeagleBone Black or compatible device with GPIO character device support.
    Operating System: Yocto-based Linux distribution (tested on Arago Kirkstone).
    Kernel: Linux 6.1.80-ti or newer with GPIO character device enabled.
    Dependencies:
        Python: Version 3.10 or newer.
        libgpiod: Version 1.6.3.
        Python gpiod bindings: Version 1.5.4 (compatible with libgpiod 1.x.x).

Setup Instructions

    Verify Installed Packages:

        Ensure libgpiod is installed:

gpiodetect
pkg-config --modversion libgpiod

Expected output for libgpiod version: 1.6.3.

Verify Python bindings:

pip3 show gpiod

If necessary, install the compatible version:

    pip3 install gpiod==1.5.4

Clone the Repository:

git clone https://github.com/<your-username>/gpio-toggle-bbb.git
cd gpio-toggle-bbb

Run the Script:

    sudo python3 gpio_toggle.py

Example Output

The script toggles a GPIO pin at 500ms intervals, printing its state:

Opened GPIO chip: /dev/gpiochip0
Accessing GPIO line: 12
GPIO line 12 set as output.
Line HIGH
Line LOW
...

Debugging Tools

    Check Available GPIO Chips:

gpiodetect

List GPIO Lines on a Chip:

gpioinfo /dev/gpiochip0

Monitor Kernel Logs for GPIO Issues:

    dmesg | grep gpio

Contribution

Contributions are welcome! Feel free to fork this repository and submit pull requests. Please ensure compatibility with the listed system requirements and dependencies.
License

This project is dual-licensed under the MIT License and GPLv3 License. You may choose either license for your use case. See the LICENSE file for details.
