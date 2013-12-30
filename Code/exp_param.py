# Class to store all experiment parameters

import numpy as np
import random 
class exp_param:

	# Global parameters
	rate = 44100 #44.1 khz, the sampling rate
	f0 =250 
	# Experiment structure
	N_stim = 23 # total number of stim
	N_rep = 1 # number of repetition per stim
	# Stimulus parameters
	interval = 0.1
	se_blank_duration = 0.02

	duration_stim =0.06 # total duration of stimulus in sec
	duration_tot = 3*duration_stim + 2*interval + 2*se_blank_duration #0.38  
	
	### ACT & HCT
	BROAD = 20000 # cutoff frequency
	DARK = 3500 #
	### Flanker
	harmonics_flanker = [3,20] # harmonics chosen to best match timbre of target alternating click trains
	# noise characteristics
	f_c_noise = 1000

	level = 1000
	
	time_stim = np.arange(0,np.floor(duration_tot*rate))/rate
	time_target = np.arange(0,np.floor(duration_stim*rate))/rate

	Sound_array = np.array([
	    # ACT Stimuli
	    [0,f0, 1, 0, DARK], #1
	    [0,f0, 1, 0, BROAD], #2 
	    [0,f0, 1, -6, BROAD], #3
	    [0,f0, 1.69, 0, DARK], #4
	    [0,f0, 1.69, 0, BROAD], #5
	    [0,f0, 1.69, -6, BROAD], #6
	    [0,f0, 2.25, 0, DARK], #7
	    [0,f0, 2.25, 0, BROAD], #8
	    [0,f0, 2.25, -6, BROAD], #9
	    [0,f0, 2.89, 0, DARK], #10
	    [0,f0, 2.89, 0, BROAD], #11
	    [0,f0, 2.89, -6, BROAD], #12
	    [0,f0, 4.0   , 0, DARK], #13
	    [0,f0, 4.0   , 0, BROAD], #14
	    [0,f0, 4.0   , -6, BROAD], #15
	    # HCT Stimuli
	    [1,f0, 0, DARK ], #16  % second is freq ratio (1 = f0, 0.5 = f0/2)
	    [1,f0, 0, BROAD], #17
	    [1,f0*2, 0, DARK], #18
	    [1,f0*2, 0, BROAD], #19
	    # ACT Control
	    [2,f0, 4.0, 0, DARK], #20
	    [2,f0, 4.0, 0, BROAD], #21 
	    [2,2*f0, 4.0, -6, DARK], #22
	    [2,2*f0, 4.0, -6, DARK]]) #23
		

	def __init__(self):
		pass

	def make_random_stim_order(self):
		# 23 stim, repeated 30 times each = 690 trials
		#The numpy equivalent of repmat(a, m, n) is tile(a, (m, n)).
		order1 =np.tile(np.arange(0,exp_param.N_stim),(exp_param.N_rep,1))
		order2 = np.concatenate(order1,axis=0)
		random.shuffle(order2)
		return order2


