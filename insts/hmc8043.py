import time

def setup(inst, default_voltage = 5.0, default_current_limit = 0.5, debug=False):
	print(inst.query("*IDN?").strip())
	inst.query_delay = 0.1

	volt_string = "VOLT " + str(default_voltage)
	curr_string = "CURR " + str(default_current_limit)

	command_sequence = [
		"OUTP:MAST OFF",
		"INST OUT1",
		"OUTP:CHAN OFF",
		"INST OUT2",
		"OUTP:CHAN OFF",
		"INST OUT3",
		"OUTP:CHAN ON",
		volt_string,
		curr_string,
	]

	try: 
		for cmd in command_sequence:
			if (send_command(inst, cmd) == False):
				print(f"'{cmd}' failed.")
				exit()
	except Exception as e:
		print(str(e))
		print("Failed to setup hmc8043")
		exit()

def get_meas(inst):
	current = inst.query(":MEAS:CURR:DC?").strip()
	voltage = inst.query(":MEAS:VOLT:DC?").strip()
	power   = inst.query(":MEAS:POW?").strip()

	measurements = {
		"current" : current,
		"voltage" : voltage,
		"power"   : power,
	}
	return measurements	


def set_output_parameters(inst,volt_setting=5.55, curr_setting=0.005):
	# not really used in balde-efficincy
	hmc_voltage_cmd = f"VOLT {volt_setting}"
	hmc_current_cmd = f"CURR {curr_setting}"
	send_command(inst, "OUTP:MAST OFF")
	send_command(inst,"INST OUT1")
	send_command(inst,hmc_voltage_cmd)
	send_command(inst,hmc_current_cmd)
	send_command(inst,"INST OUT2")
	send_command(inst,hmc_voltage_cmd)
	send_command(inst,hmc_current_cmd)
	send_command(inst, "OUTP:MAST ON")


def main():
	print("I don't do anything")	

def send_command(inst, cmd, scpi_delay=0.10, debug=False):
	if (debug): print(cmd)
	inst.write(cmd)
	time.sleep(scpi_delay)
	if (debug): 
		error_str = str(inst.query("SYST:ERR?").strip())
		print(error_str)
	time.sleep(scpi_delay)
	#if (debug): print("---")
	return True

if __name__ == '__main__':
	main()