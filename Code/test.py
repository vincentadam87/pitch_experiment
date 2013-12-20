import exp_param
import filtering
import sound_build
from pylab import *
import matplotlib.pyplot as pp

Exp = exp_param.exp_param()



o = Exp.make_random_stim_order()

#for i in range(9,13):
#	y =  sound_build.make_target(i,Exp)
#	figure(i)
#	pp.plot(y)
#show()