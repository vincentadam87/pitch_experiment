# Class to store all experiment parameters

import numpy as np
import random 
class exp_param:

	# Global parameters
	rate = 44100 #44.1 khz, the sampling rate
	f0 =250 
	fi = f0*np.sqrt(2)
	# Experiment structure
	N_stim = 23 # total number of stim
	N_rep = 1 # number of repetition per stim
	# Stimulus parameters
	interval = 0.1
	se_blank_duration = 0.01

	# task parameters
	iti = 1
	
	duration_stim =0.06 # total duration of stimulus in sec
	duration_tot = 3*duration_stim + 2*interval + 2*se_blank_duration #0.38  
	
	### ACT & HCT
	BROAD = 1
	DARK = 0
	fc_ACT_DARK = 3000 #
	fc_HCT_DARK = 3500 #
	fc_HCT_BROAD = 20000 #
	### Flanker
	harmonics_flanker = [3,20] # harmonics chosen to best match timbre of target alternating click trains
	# noise characteristics
	f_c_noise = 1000

	level = 1000
	
	time_stim = np.arange(0,np.floor(duration_tot*rate))/rate
	time_target = np.arange(0,np.floor(duration_stim*rate))/rate

	Sound_array = np.array([
	    # ACT Stimuli
	    [0, 0,f0, 1, DARK], #0
	    [0, 0,f0, 1, BROAD], #1 
	    [0, -6,f0, 1, BROAD], #2
	    [0, 0,f0, 1.69, DARK], #3
	    [0, 0,f0, 1.69, BROAD], #4
	    [0, -6,f0, 1.69, BROAD], #5
	    [0, 0,f0, 2.25, DARK], #6
	    [0, 0,f0, 2.25, BROAD], #7
	    [0, -6,f0, 2.25, BROAD], #8
	    [0, 0,f0, 2.89, DARK], #9
	    [0, 0,f0, 2.89, BROAD], #10
	    [0, -6,f0, 2.89, BROAD], #11
	    [0, 0,f0, 4.0   , DARK], #12
	    [0, 0,f0, 4.0   , BROAD], #13
	    [0, -6,f0, 4.0   , BROAD], #14
	    # HCT Stimuli
	    [1, 0,f0, DARK ], #15  % second is freq ratio (1 = f0, 0.5 = f0/2)
	    [1, 0,f0, BROAD], #16
	    [1, 0,f0*2, DARK], #17
	    [1, 0,f0*2, BROAD], #18
	    # ACT Control
	    [2, 0,f0, 4.0, DARK], #19
	    [2, 0,f0, 4.0, BROAD], #20 
	    [2, -6,2*f0, 4.0, DARK], #21
	    [2, -6,2*f0, 4.0, DARK], #22
	    # Additional training
	    [0, 0,f0, 9   , BROAD], #23
   	    [0, 0,f0, 9   , DARK]]) #24

	Calibration_sounds = [0,1,23,24]
	Training_sounds = np.array([[0,1,23,24],[0,1,6,7,12,13]])

	Training_duration = 300 # 5 minutes

	def __init__(self):

		pass

	def make_random_stim_order(self):
		# 23 stim, repeated 30 times each = 690 trials
		#The numpy equivalent of repmat(a, m, n) is tile(a, (m, n)).
		order1 =np.tile(np.arange(0,exp_param.N_stim),(exp_param.N_rep,1))
		order2 = np.concatenate(order1,axis=0)
		random.shuffle(order2)
		return order2


