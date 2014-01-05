# Class to store all experiment parameters

import numpy as np
import random 
class exp_param:

	# Target/flanker sound parameters
	rate = 44100 #44.1 khz, the sampling rate
	f0 =250 # lowest fundamental in octave pair
	fi = f0*np.sqrt(2) # half way between f0 and 2*f0
	duration_stim =0.06 # total duration of stimulus in sec
	RATIO = [1,1.69,2.25,2.89,4] # ratio of alternating click-trains
	harmonics_flanker = [3,20] # harmonics chosen to best match timbre of target alternating click trains
	fc_ACT_DARK = 3000 # for butterworth filter
	fc_HCT_DARK = 3500 # for hard cut of harmonics higher in HCT
	fc_HCT_BROAD = 20000 # for hard cut of harmonics higher in HCT

	# Stimulus structure
	interval = 0.1 # blank interval length between flankers and target
	se_blank_duration = 0.01 # extra milliseconds at sound onset and offset
	duration_tot = 3*duration_stim + 2*interval + 2*se_blank_duration #0.38  
	f_c_noise = 1000 # cut-off frequency for noise
	level = 1000

	# Experiment structure
	N_stim = 23 # total number of stim
	N_rep = 10 # number of repetition per stim (Hehrmann 30)
	iti = 1 # time between response and begining of next trial
	Training_duration = 60 #120 # 300 =5 minutes

	# Constants
	ACT = 0
	HCT = 1
	CONTROL = 2
	BROAD = 1
	DARK = 0
	CORRECT_UP = 1
	CORRECT_DOWN = 0
	
	time_stim = np.arange(0,np.floor(duration_tot*rate))/rate
	time_target = np.arange(0,np.floor(duration_stim*rate))/rate

	Sound_array = np.array([
	    # ACT Stimuli
	    [ACT, 0,f0, RATIO[0], DARK], #0
	    [ACT, 0,f0, RATIO[0], BROAD], #1 
	    [ACT, -6,f0, RATIO[0], BROAD], #2
	    [ACT, 0,f0, RATIO[1], DARK], #3
	    [ACT, 0,f0, RATIO[1], BROAD], #4
	    [ACT, -6,f0, RATIO[1], BROAD], #5
	    [ACT, 0,f0, RATIO[2], DARK], #6
	    [ACT, 0,f0, RATIO[2], BROAD], #7
	    [ACT, -6,f0, RATIO[2], BROAD], #8
	    [ACT, 0,f0, RATIO[3], DARK], #9
	    [ACT, 0,f0, RATIO[3], BROAD], #10
	    [ACT, -6,f0, RATIO[3], BROAD], #11
	    [ACT, 0,f0, RATIO[4]   , DARK], #12
	    [ACT, 0,f0, RATIO[4]   , BROAD], #13
	    [ACT, -6,f0, RATIO[4]   , BROAD], #14
	    # HCT Stimuli
	    [HCT, 0,f0, DARK, CORRECT_DOWN], #15  % second is freq ratio (1 = f0, 0.5 = f0/2)
	    [HCT, 0,f0, BROAD,CORRECT_DOWN], #16
	    [HCT, 0,f0*2, DARK,CORRECT_UP], #17
	    [HCT, 0,f0*2, BROAD,CORRECT_UP], #18
	    # ACT Control
	    [CONTROL, 0,f0, RATIO[4] , DARK,CORRECT_DOWN], #19
	    [CONTROL, 0,f0, RATIO[4] , BROAD,CORRECT_DOWN], #20 
	    [CONTROL, -6,2*f0, RATIO[4] , DARK,CORRECT_UP], #21
	    [CONTROL, -6,2*f0, RATIO[4] , BROAD,CORRECT_UP], #22
	    # Additional training
	    [ACT, 0,f0, 9    , BROAD], #23
   	    [ACT, 0,f0, 9   , DARK]]) #24

	CorrectResp = np.array([[15,16,19,20],[17,18,21,22]]) # down / up
	Calibration_sounds = [0,1,23,24]
	Training_sounds = np.array([[0,1,23,24],[0,1,6,7,12,13]])

	def __init__(self):
		pass

	def make_random_stim_order(self):
		# 23 stim, repeated 30 times each = 690 trials
		#The numpy equivalent of repmat(a, m, n) is tile(a, (m, n)).
		order1 =np.tile(np.arange(0,exp_param.N_stim),(exp_param.N_rep,1))
		order2 = np.concatenate(order1,axis=0)
		random.shuffle(order2)
		return order2

	def isRespCorrect(self,i,thisResp):
		if thisResp in [1,-1]: # key pressed is up or down

			if i in exp_param.CorrectResp[0]: # correct response is down
				if (thisResp == -1):
					return 1 
				else:
					return 0
			elif i in exp_param.CorrectResp[1]: # correct response is up
				if (thisResp == 1):
					return 1
				else:
					return 0
			else:	# there was no correct or wrong response
				return -1
		else:
			return -1 # key miss

	def isACT(self,i):
		return (exp_param.Sound_array[i][0] == exp_param.ACT)
	def isHCT(self,i):
		return (exp_param.Sound_array[i][0] == exp_param.ACT)
	def isCONTROL(self,i):
		return (exp_param.Sound_array[i][0] == exp_param.ACT)

