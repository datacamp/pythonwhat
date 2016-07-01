from pythonbackend.Exercise import Exercise
from pythonbackend import utils

def get_sct_payload(output):
	output = [out for out in output if out['type'] == 'sct']
	if (len(output) > 0):
		return(output[0]['payload'])
	else:
		return(None)

def run(data):
    exercise = Exercise(data)
    exercise.runInit()
    output = exercise.runSubmit(data)
    return(get_sct_payload(output))
