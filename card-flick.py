import signal
import flicklib
import time
import uinput

device = uinput.Device([uinput.KEY_RIGHT, uinput.KEY_LEFT])

@flicklib.flick()
def flick(start, finish):
	if finish == "north":
		pass

	elif finish == "east":
		device.emit_click(uinput.KEY_RIGHT)

	elif finish == "south":
		pass

	elif finish == "west":
		device.emit_click(uinput.KEY_LEFT)

	else:
		pass

while True:
	time.sleep(0.1)