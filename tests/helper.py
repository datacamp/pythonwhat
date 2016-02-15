def get_sct_payload(output):
	output = [out for out in output if out['type'] == 'sct']
	if (len(output) > 0):
		return(output[0]['payload'])
	else:
		return(None)