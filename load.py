import pyvisa  # for scpi
import time    # for sleep
import signal  # for ctrl-c
import sys     # call to ping
import os      # for exit signal

from insts import instruments  # globals for VISA resource strings
from insts import mp710259

rm = pyvisa.ResourceManager('@py')
#print(rm.list_resources())
#exit()

def main():
	print("[Opening] mp710259 Load")
	mp710259_load = rm.open_resource(instruments.load_id)
	mp710259.setup(mp710259_load, True)
	cmd_delay = 0.1

	mp710259.send_command(mp710259_load, ":INP ON")
	set_points = ["0.111A", "0.222A", "0.333A"]
	for point in set_points:
		mp710259.send_command(mp710259_load, f":CURR {point}")
		measures = mp710259.get_meas(mp710259_load)
		print(f"At {point}: {measures['current']}, {measures['voltage']}, {measures['power']}")
		time.sleep(5)
	mp710259.send_command(mp710259_load, ":INP OFF")


	# measures = mp710259.get_meas(mp710259_load)
	# print(f"Current: {measures['current']}")
	# print(f"Voltage: {measures['voltage']}")
	# print(f"Power  : {measures['power']}")

if __name__ == '__main__':
	main()
	rm.close()

