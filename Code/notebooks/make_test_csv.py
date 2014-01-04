from psychopy import core, visual, gui, data, event
from psychopy.misc import fromFile, toFile
import time, random
from scipy.io.wavfile import write
import numpy as np
import pygame

import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_subfolder = os.path.realpath("../scripts")
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import exp_param as exp_param

Exp = exp_param.exp_param()
fileName = 'test'
dataFile = open('../notebooks/'+fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
dataFile.write('stim index,chosen dir, correct\n')

N = 10000

x = np.zeros((N,3),int)
for r in np.arange(0,N-1):
	i = random.randint(0,23)
	key = random.randint(-1,1)
	correct = Exp.isRespCorrect(i,key)
	dataFile.write('%i,%i,%i\n' %(i, key,correct))
core.wait(1)
dataFile.close()


