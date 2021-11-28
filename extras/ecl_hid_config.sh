#!/bin/bash

# Create the HID devices used for ECL joystick/keyboard output
# (used for ECL shifter and GPIO inputs)

sleep 2

# Create 16 button 16_buttons_rpi_joystick gadget
cd /sys/kernel/config/usb_gadget/
mkdir -p 16_buttons_rpi_joystick
cd 16_buttons_rpi_joystick

# Define USB specification
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Joystick Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
echo 0x00 > bDeviceClass
echo 0x00 > bDeviceSubClass
echo 0x00 > bDeviceProtocol

# Perform localization
mkdir -p strings/0x409

echo "0123456789" > strings/0x409/serialnumber
echo "Raspberry Pi" > strings/0x409/manufacturer
echo "RaspberryPi Joystick" > strings/0x409/product


# Define the functions of the device
mkdir functions/hid.usb0
echo 0 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass
echo 4 > functions/hid.usb0/report_length

# Write report descriptor ( X and Y analog joysticks plus 16 buttons )
echo "05010904A1011581257F0901A10009300931750895028102C0A10005091901291015002501750195108102C0C0" | xxd -r -ps > functions/hid.usb0/report_desc

# Define the functions of the device
mkdir functions/hid.usb1
echo 0 > functions/hid.usb1/protocol
echo 0 > functions/hid.usb1/subclass
echo 8 > functions/hid.usb1/report_length

# Write report descriptor ( Keyboard, 8 byte? )
echo "05010906a101050719e029e71500250175019508810275089501810175019503050819012903910275019505910175089506150026ff00050719002aff008100c0" | xxd -r -ps > functions/hid.usb1/report_desc

# Create configuration file
mkdir -p configs/c.1/strings/0x409

echo 0x80 > configs/c.1/bmAttributes
echo 500 > configs/c.1/MaxPower # 500 mA
echo "RaspberryPi Joystick Configuration" > configs/c.1/strings/0x409/configuration

# Link the configuration file
ln -s functions/hid.usb0 configs/c.1
ln -s functions/hid.usb1 configs/c.1

# Activate device 
ls /sys/class/udc > UDC

sleep 1

# Allow non-root access to device

chmod a+rw /dev/hidg0
chmod a+rw /dev/hidg1

sleep 2

