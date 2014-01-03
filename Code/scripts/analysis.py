# script to analyse and plot output of psychophysical experiment

# Desired output
# 1 -- Assess pitch perception
# 	For non ambiguous HCT target stimuli plot accuracy (error  = octave error)
# 2 -- Assess timbral effect for ambiguous pitch
# 	For ambiguous ACT target stimuli plot psychometric curves
# 3 -- Controls: Assess pitch perception for Control stimuli
#   For control stimuli plot accuracy (octave error)

import csv

# --- Load data file

def read_data(filename):
	with open(filename+'.csv', 'r') as f:
		reader = csv.reader(f)
		reader.next()
		for row in reader:
			print row

# --- Read data

# build array from data#
#data =np.recfromcsv(filename+'.csv', delimiter=',', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')

# 1 : Pitch perception (stimuli HCT : 15,16,17,18)




# 2 : Resolving ambiguity
# 3 : Controls

