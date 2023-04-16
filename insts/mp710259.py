import time
# def connect_visa_mp710259(default_delay=0.1, baud=''):
# 	#
# 	# I don't really use this function anymore
# 	#
# 	# connect as serial or usb?
# 	if (baud == ''):
# 		load = rm.open_resource(instruments_development.load_id)
# 		load.query_delay = default_delay
# 	else:
# 		print("Serial not tested")
# 		load = rm.open_resource(instruments_development.load_id)
# 		load.baud_rate = baud
# 		load.query_delay = default_delay
# 		load.read_termination = '\n'
# 		load.write_termination = '\r\n'

# 	print(load.query('*IDN?'))
# 	return load

def main():
	print("I dont do anything")

def setup(inst, debug=False):
	print(inst.query("*IDN?").strip())
	cmd_delay = 0.1
	command_sequence = [
		":INPut OFF",
		":FUNC CC",
		":CURR 0.111A",
	]

	try: 
		for cmd in command_sequence:
			if (send_command(inst, cmd) == False):
				print(f"'{cmd}' failed.")
				exit()
	except Exception as e:
		print(str(e))
		print("Failed to setup Load")
		exit()

	#send_command(inst, ":INPut OFF")
	#send_command(inst, ":FUNC CC")

	if (debug): print(inst.query(":MEAS:VOLT?").strip())

def wait(inst, timeout=30):
	print("mp710259 OPC not implemented!")

	return False
	# start = time.time()
	# while True:
	# 	# is Operation Complete stuck?
	# 	try:
	# 		if (inst.query("*OPC?").strip() == "1"):
	# 			return True
	# 	except:
	# 		print("!",end='')

	# 	# if we stay stuck for 30 seconds, bail
	# 	if ((time.time() - start) > timeout):
	# 		print("MP730028 OPC Failed")
	# 		return False
	# 	#print(".")
	# 	time.sleep(0.1)
	# return True

def get_meas(inst):
	current = inst.query(":MEAS:CURR?").strip().replace('A','')
	voltage = inst.query(":MEAS:VOLT?").strip().replace('V','')
	power   = inst.query(":MEAS:POW?").strip().replace('W','')

	measurements = {
		"current" : current,
		"voltage" : voltage,
		"power"   : power,
	}
	return measurements

def send_command(inst, cmd, scpi_delay=0.10, debug=False):
	if (debug): print(cmd)
	inst.write(cmd)
	time.sleep(scpi_delay)
	if (debug): 
		#error_str = str(inst.query("SYST:ERR?").strip())
		#print(error_str)
		print("mp710259 doesnot support SYST:ERR")
	time.sleep(scpi_delay)
	#if (debug): print("---")
	return True

if __name__ == '__main__':
	main()
