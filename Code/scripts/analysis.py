# script to analyse and plot output of psychophysical experiment
# Desired output
# 1 -- Assess pitch perception
# 	For non ambiguous HCT target stimuli plot accuracy (error  = octave error)
# 2 -- Assess timbral effect for ambiguous pitch
# 	For ambiguous ACT target stimuli plot psychometric curves
# 3 -- Controls: Assess pitch perception for Control stimuli
#   For control stimuli plot accuracy (octave error)

import numpy as np
import os, sys 
# realpath() with make your script run, even if you symlink it :)
cmd_subfolder = os.path.realpath("../scripts")
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
cmd_subfolder1 = os.path.realpath("../data")
if cmd_subfolder1 not in sys.path:
    sys.path.insert(0, cmd_subfolder1)

from matplotlib import pyplot as plt
import exp_param as exp_param
import csv


def perform_analysis(filename):
	#path = '../data/'
	#filename = 'gui_short2014_Jan_03_1512'
	#filename = 'remi_short2014_Jan_03_1512'
	#filename = 'VINCENT5JAN'
	#with open(path+filename+'.csv', 'r') as f:
	with open(filename, 'r') as f:
	    reader = csv.reader(f)
	    reader.next()
	    x = list(reader)
	    y = [[int(string) for string in inner] for inner in x]
	  
	INDEX_hct = [15,16,17,18]
	CORRECT_hct = [0,0,1,1]
	counts_hct = np.zeros((len(INDEX_hct),3),float) # correct, incorrect, missed
	INDEX_control = [19,20,21,22]
	CORRECT_control = [0,0,1,1]
	counts_control = np.zeros((len(INDEX_control),3),float) # correct, incorrect, missed

	# Extract counts for HCT
	i_index = -1
	for index in INDEX_hct:
	    i_index += 1
	    for row in y:
	        if (row[0] == index):
	            if (row[2] == 1): #correct
	                counts_hct[i_index,0] += 1 
	            elif (row[2] == 0): #incorrect
	                counts_hct[i_index,1] += 1 
	            elif (row[2] == -1):#missed
	                counts_hct[i_index,2] += 1
	                
	# Compute Accuracy for HCT
	accuracy_hct = np.zeros((4),float)
	i_index = -1
	for row in counts_hct:
	    i_index += 1
	    a = row[1]/(row[0]+row[1])
	    x = CORRECT_hct[i_index]
	    accuracy_hct[i_index] = a**x*(1-a)**(1-x)

	# Extract counts for CONTROLS (counts of correct answers)
	i_index = -1
	for index in INDEX_control:
	    i_index += 1
	    for row in y:
	        if (row[0] == index):
	            if (row[2] == 1): #correct
	                counts_control[i_index,0] += 1 
	            elif (row[2] == 0): #incorrect
	                counts_control[i_index,1] += 1 
	            elif (row[2] == -1):#missed
	                counts_control[i_index,2] += 1
	                
	# Compute Accuracy for HCT
	accuracy_control = np.zeros((4),float)
	i_index = -1
	for row in counts_control:
	    i_index += 1
	    a = row[1]/(row[0]+row[1])
	    x = CORRECT_hct[i_index]
	    accuracy_control[i_index] = a**x*(1-a)**(1-x)

	# Make psychometric curve for mains
	Exp = exp_param.exp_param()


	INDEX_ambi = Exp.Ambi_exp_sounds  # [0...14] for ACT

	N_ambi = len(INDEX_ambi)
	counts_ambi = np.zeros((N_ambi,3),float) # 3 timbre/snr,  5 ratios, 3 possible responses


	# Extract counts for mains
	i_index = -1
	for index in INDEX_ambi:
	    i_index += 1
	    for row in y:
	        if (row[0] == index):
	            if (row[1] == 1): #pressed up
	                counts_ambi[i_index,0] += 1 
	            elif (row[1] == -1): #pressed down
	                counts_ambi[i_index,1] += 1 
	            else:# pressed other key (miss)#psy_curve = np.zeros((3,5)) # cond * ratio

	                counts_ambi[i_index,2] += 1

	# Compute Accuracy for main
	accuracy_ambi = np.zeros((len(INDEX_ambi)),float)
	i_index = -1
	for row in counts_ambi:
	    i_index += 1
	    accuracy_ambi[i_index] = row[0]/(row[0]+row[1])

	# Merge accuracies to build psychometric curves
	# indices of sounds of increasing ratio for the 3 conditions
	ind_by_cond = [np.arange(0,N_ambi,3),
	               np.arange(1,N_ambi,3),
	               np.arange(2,N_ambi,3)]


	psy_curve = [[accuracy_ambi[index] for index in row] for row in ind_by_cond]
	psy_curve_std = [[accuracy_ambi[index]*(1-accuracy_ambi[index]) for index in row] for row in ind_by_cond]

	# compute std
	std_control = ((1-accuracy_control)*accuracy_control)
	std_hct = ((1- accuracy_hct)*accuracy_hct)
	std_ambi= ((1- accuracy_ambi)*accuracy_ambi)


	#########################################

	N = 2
	ind = np.arange(N)  # the x locations for the groups
	width = 0.35       # the width of the bars

	hctf250m = accuracy_hct[[0,2]]
	hctf250std = std_hct[[0,2]]

	hctf500m = accuracy_hct[[1,3]]
	hctf500std = std_hct[[1,3]]

	controlf250m = accuracy_control[[0,2]]
	controlf250std = std_control[[0,2]]

	controlf500m = accuracy_control[[1,3]]
	controlf500std = std_control[[1,3]]

	print(counts_ambi)
	print(counts_hct)
	print(counts_control)

	print(accuracy_ambi)
	print(accuracy_hct)
	print(accuracy_control)

	print(hctf250m)
	print(hctf500m)
	print(controlf250m)
	print(controlf500m)



	RATIO = Exp.RATIO


	def press(event):
	    print('press', event.key)
	    sys.stdout.flush()
	    if event.key=='enter':
			sys.exit()
	#########################################

	
	fig1, ax1 = plt.subplots()
	rects1 = ax1.bar(ind, hctf500m, width, color='r', yerr=hctf500std)
	rects2 = ax1.bar(ind+width, hctf250m, width, color='y', yerr=hctf250std)
	ax1.set_ylabel('fraction high') 
	ax1.set_xticks(ind+width)
	ax1.set_xticklabels( ('500 Hz', '250 Hz') )
	ax1.legend( (rects1[0], rects2[0]), ('Broad', 'Dark') )
	ax1.set_title('HCT')
	plt.ylim(0,1)

	#########################################

	fig2, ax2 = plt.subplots()
	rects1 = ax2.bar(ind, controlf500m, width, color='r', yerr=controlf500std    #accuracy_control[i_index] = row[0]/(row[0]+row[1])
	)
	rects2 = ax2.bar(ind+width, controlf250m, width, color='y', yerr=controlf250std)
	ax2.set_ylabel('fraction high')
	ax2.set_xticks(ind+width)
	ax2.set_xticklabels( ('500 Hz', '250 Hz') )
	ax2.legend( (rects1[0], rects2[0]), ('Broad', 'Dark') )
	ax2.set_title('Controls')
	plt.ylim(0,1)

	#########################################

	fig3, ax3 = plt.subplots()
	for i in np.arange(0,np.shape(psy_curve)[0]):
	    ax3.errorbar(RATIO, psy_curve[i], yerr=psy_curve_std[i] , linestyle="dashed", marker="o")
	
	ax3.legend(['0db dark','0db', '-6dB'])
	ax3.set_xlabel('ratio')
	ax3.set_ylabel('fraction high')
	ax3.grid(True)
	ax3.set_title('Timbral effects, main')

	plt.ioff()
	plt.ylim(0,1)

	fig1.show()
	fig1.canvas.mpl_connect('key_press_event', press)
	fig2.show()
	fig2.canvas.mpl_connect('key_press_event', press)
	fig3.show()
	fig3.canvas.mpl_connect('key_press_event', press)

	plt.show()

#########################################

if __name__ == '__main__':
    map(perform_analysis, sys.argv[1:])
