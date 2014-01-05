from psychopy import core, visual, gui, data, event
from psychopy.misc import fromFile, toFile
import time, random
from scipy.io.wavfile import write
import numpy as np
import pygame
from matplotlib import pyplot as plt
import os, sys, inspect
import time
# realpath() with make your script run, even if you symlink it :)
#cmd_subfolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "/scripts")
cmd_subfolder = os.path.realpath('..')+'/scripts'
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)
import sound_build, exp_param

#------------ load global experiment parameters
Exp = exp_param.exp_param()


for i in np.arange(0,np.shape(Exp.Sound_array)[0]):
	s = sound_build.make_noisy_stim(i,Exp)
	level = Exp.level
	#scaled = np.int16(s/np.max(np.abs(s)) * (2**12-1))# 32767)
	scaled = np.int16(s * (2**9-1))# 32767)
	write('test.wav', 44100, scaled)
	pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
	pygame.mixer.music.load("test.wav")
	pygame.mixer.music.play()
	time.sleep(Exp.duration_tot+0.5)
	#plt.plot(Exp.time_stim,s)
	#plt.show()

