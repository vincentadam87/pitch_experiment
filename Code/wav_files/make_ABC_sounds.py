import scipy
from scipy.io import wavfile
import numpy as np
import struct, sys 

import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_subfolder = os.path.realpath("../scripts")
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import filtering as filt
from scipy.signal import freqz
from matplotlib import pyplot as plt
import exp_param
import sound_build as sb
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

Exp = exp_param.exp_param()
rate = Exp.rate
a = 1000 # amplitude of sounds to play (scaling sounds of rms 1)

# plotting and playing stimuli

R_inf = 10000
A_broad = sb.make_act_target(Exp.RATIO[4],Exp.f0,Exp.BROAD,Exp)
A_dark = sb.make_act_target(Exp.RATIO[4],Exp.f0,Exp.DARK,Exp)
B_broad = sb.make_act_target(R_inf,Exp.f0,Exp.BROAD,Exp)  
B_dark = sb.make_act_target(R_inf,Exp.f0,Exp.DARK,Exp)  

couples = [ [A_broad,B_broad],[A_dark,B_dark]]


# generate individual sounds
i_pair = 0
for pair in couples:
    i_pair +=1
    i_y = 0
    for y in pair:
    	i_y += 1
    	scaled = np.int16(y * (2**9-1))
    	filename = 'pair_'+str(i_pair)+'_elt_'+str(i_y)+'.wav'
    	write(filename, 44100, scaled)

i_pair = 0
for pair in couples:
	i_pair +=1
	blank = np.zeros((Exp.rate,1),float)
	blank = np.zeros((0,1),float)

	seq = np.append(pair[0],blank)
	seq = np.append(seq,pair[1])
	seq = np.append(seq,blank)
	seq = np.append(seq,pair[0])
	seq = np.append(blank,seq)
	seq = np.append(seq,blank)

	seqAAA = np.append(pair[0],blank)
	seqAAA = np.append(seqAAA,pair[0])
	seqAAA = np.append(seqAAA,blank)
	seqAAA = np.append(seqAAA,pair[0])
	seqAAA = np.append(blank,seqAAA)
	seqAAA = np.append(seqAAA,blank)

	seqBBB = np.append(pair[1],blank)
	seqBBB = np.append(seqBBB,pair[1])
	seqBBB = np.append(seqBBB,blank)
	seqBBB = np.append(seqBBB,pair[1])
	seqBBB = np.append(blank,seqBBB)
	seqBBB = np.append(seqBBB,blank)


	for snrdb in [0,-6]:
		print(snrdb)
		#seq = sb.add_lpnoise_at_snrdb(seq,snrdb,Exp)
		scaled = np.int16(seq * (2**9-1))
		plt.plot(np.arange(0,len(seq)),seq)
		plt.show()
		filename = 'XXX_pair_'+str(i_pair)+'_snrdb_'+str(snrdb)+'.wav'
		write(filename, 44100, scaled)

		scaled = np.int16(seqAAA * (2**9-1))
		plt.plot(np.arange(0,len(seqAAA)),seqAAA)
		plt.show()
	
		filename = 'AAA_pair_'+str(i_pair)+'_snrdb_'+str(snrdb)+'.wav'
		write(filename, 44100, scaled)

		scaled = np.int16(seqBBB* (2**9-1))
		filename = 'BBB_pair_'+str(i_pair)+'_snrdb_'+str(snrdb)+'.wav'
		write(filename, 44100, scaled)

