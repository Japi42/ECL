
# Supported Hardware

ECL currently controls two classes of devices:  LED Devices and Displays.  LED Devices are devices that turn LEDs on and off.  Currently the only supported hardware is the Ultimarc PacDrive.  Displays are miniture screens controled via SPI or I2C.  Currently Displays can be controlled via Adafruit Blinka-compatiable devices (like their FT232H board), or via Luma (tested on a raspberry pi zero).  

## PacDrive Support:

The PacDrive in ECL supports control of 16 LEDs per board, with multiple boards supported (but they must have been ordered with unique IDs).  

Control of the PacDrive is via umtool on Linux.  I use a staticly linked version of this tool for ease of deployment.  This tool can be retrieved from github and compiled using the instructions below:

Compile umtool:

apt-get install autotools-dev autoconf automake libudev-dev libjson-c-dev libusb-1.0-0-dev libtool

git clone https://github.com/katie-snow/Ultimarc-linux.git

./autogen.sh
./configure
edit src/umtool/Makefile to static link umtool:

LINK = $(LIBTOOL) $(AM_V_lt) --tag=CC $(AM_LIBTOOLFLAGS) \
        $(LIBTOOLFLAGS) --mode=link $(CCLD) $(AM_CFLAGS) $(CFLAGS) \
        $(AM_LDFLAGS) -static $(LDFLAGS) -o $@

Install udev rule:
sudo cp 21-ultimarc.rules /etc/udev/rules.d/

Install umtool:

sudo cp src/umtool/umtool /usr/local/bin


