#!/usr/bin/python
##--------------------
##--- Author: Pradeep Singh
##--- Blog: https://iotbytes.wordpress.com/
##--- Date: 1st Dec 2017
##--- Version: 1.0
##--- Python Ver: 2.7
##--- Description: This python code will reset a USB port connected to Raspberry Pi
##--------------------


import os
import sys
import fcntl


#=================================================================
# Reset Modem
#=================================================================
def reset_USB_Device( usb_bus, usb_dev ):

	# Same as _IO('U', 20) constant in the linux kernel.
	CONST_USB_DEV_FS_RESET_CODE = ord('U') << (4*2) | 20

	usb_dev_path = '/dev/bus/usb/%s/%s' % (usb_bus, usb_dev)

	try:
		if usb_dev_path != "":
			print "Trying to reset USB Device: " + usb_dev_path
			device_file = os.open(usb_dev_path, os.O_WRONLY)
			fcntl.ioctl(device_file, CONST_USB_DEV_FS_RESET_CODE, 0)
			print "USB Device reset successful."
		else:
			print "Device not found."
	except:
		print "Failed to reset the USB Device."
	finally:
		try:
			os.close(device_file)
		except:
			pass

#=================================================================

if __name__ == '__main__':

	reset_USB_Device( sys.argv[1], sys.argv[2] )
