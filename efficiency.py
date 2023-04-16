import pyvisa  # for scpi
import time    # for sleep
import signal  # for ctrl-c
import sys     # call to ping
import os      # for exit signal

import numpy as np

from insts import instruments  # globals for VISA resource strings
from insts import mp710259
from insts import hmc8043

input_voltage = 4.1
input_current = 1.25

def connect_load():
	global mp710259_load
	try:
		print("[Opening] mp710259 Load")
		mp710259_load = rm.open_resource(instruments.load_id)
		mp710259.setup(mp710259_load, True)
	except Exception as e:
		print(str(e))
		print("Can't open the load")
		rm.close()
		exit()

def print_range(range, unit):
	for point in range:
		print(f",{float(point):.4}{unit}", end="")
	print("")


def connect_ps():
	global hmc8043_ps
	try:
		print("[Opening] hmc8043 bench supply")
		hmc8043_ps = rm.open_resource(instruments.ps_id)
		hmc8043.setup(hmc8043_ps, input_voltage, input_current, True)
	except Exception as e:
		print(str(e))
		print("Can't open the load")
		rm.close()
		exit()	

def main():
	connect_load()
	connect_ps()

	voltages = np.arange(6,13,2).tolist()
	#voltages = [12]
	#voltages = [6.0, 8, 10]
	set_points = np.linspace(0.1, 1, 20)
	#set_points = np.logspace(0, 1, endpoint=True) / 10
	#set_points = ["0.9", "1.0"]

	point_wait = 0.1
	volt_wait = 0.25

	# print out currents for reference
	#print("Set points", end="")
	print_range(set_points, "A")

	# print voltage header
	print("Curr", end="")
	print_range(voltages,"V")

	#exit()
	
	mp710259.send_command(mp710259_load, ":INP ON")
	hmc8043.send_command(hmc8043_ps, "OUTP:MAST ON")
	#print(f"Input Voltage: {input_voltage}V @ max {input_current}A")
	for point in set_points:
		clean_point = f"{point:.4}"
		mp710259.send_command(mp710259_load, f":CURR {clean_point}A")
		#print (f"Set point: {clean_point}", end="", flush=True)
		print(f"{clean_point}", end="", flush=True)
		time.sleep(point_wait)
		
		for volt in voltages:
			hmc8043.send_command(hmc8043_ps, f"VOLT {volt}")
			time.sleep(volt_wait)
			in_measures = hmc8043.get_meas(hmc8043_ps)
			out_measures = mp710259.get_meas(mp710259_load)
			if ((float(out_measures['power']) == 0) or (float(in_measures['power'])) == 0):
				print("N/A?", end="", flush=True)
				#print("...\nPower is 0, aborting.")
				#return
			else:
				eff = (float(out_measures['power']) / float(in_measures['power'])) * 100
				print(f",{eff:.2f}", end="", flush=True)

		print("")
		#print(f"In: {in_measures['current']}, {in_measures['voltage']}, {in_measures['power']}")
		#print(f"Out: {out_measures['current']}, {out_measures['voltage']}, {out_measures['power']}")

	hmc8043.send_command(hmc8043_ps, "OUTP:MAST OFF")
	time.sleep(1)
	print("Shorting output ...")
	mp710259.send_command(mp710259_load, ":FUNC SHOR")
	time.sleep(5)
	print("Disabling Output")
	mp710259.send_command(mp710259_load, ":FUNC CC")
	mp710259.send_command(mp710259_load, ":INP OFF")
	print("Setting back to 100mA")
	mp710259.send_command(mp710259_load, ":CURR 0.1A")

if __name__ == '__main__':
	global rm
	print("Efficiency")
	rm = pyvisa.ResourceManager('@py')
	main()
	rm.close()

