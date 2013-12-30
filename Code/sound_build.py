# Functions to build sounds

import numpy as np
import filtering as filt

# -----------------------------------------------------------------
# ------------ Base functions (Experiment independent)
# -----------------------------------------------------------------

# Normalizing sounds (set std to 1)
def normalize(x):
    return np.divide(x,np.std(x))

# shift signal by half period
def half_period_shift(x,f0,rate):
    y = np.zeros(len(x))
    omega= 1/f0;
    T2 = int(np.floor(rate/f0/2));
    y[0:-T2:] += x[T2::]
    return y

# generate white noise
def white_noise(l):
    return np.random.randn(l) 

def make_lp_noise(n,f_c_noise,rate):
    # load experiment parameters
    a,b = filt.make_low_pass_butterworth(f_c_noise, 6,rate) 
    N = 0 # to cut begining of filter convolution
    wn = np.random.randn(n+N) # generate white noise
    fwn = filt.apply_filter(wn,a,b)
    return normalize(fwn[-n:]) 


def add_to_stim(stim,x,i_start):
    stim[i_start:i_start+len(x):] += x;
    return stim

def make_time(duration,rate):
    return np.linspace(0,duration, num=rate*duration)

def make_time_from_x(x,rate):
    return np.linspace(0,len(x)*rate, num=len(x))


# ------------------- define functions to generate sounds

# Pure tone, amplitude 1
def normedsin(f,t):
    return np.sin(2*np.pi*f*t)


# Dirac comb amplitude 1
def dirac_comb(f,t):
    omega= 1/f;
    rate = 1/(t[1]-t[0])
    T = int(np.floor(rate/f));
    k = int(np.ceil(len(t)/T));
    x=np.zeros(len(t))
    for k in range(0, k):
      x[k*T]=1
    return x


# alternating click train, 
def act(a1,a2,f,t):
    rate = 1/(t[1]-t[0])
    y = np.zeros(len(t))
    y += a1*dirac_comb(f,t)  + a2*half_period_shift(dirac_comb(f,t),f,rate)
    return y
    
# HCT
def hct(f,t,k):
    y = np.zeros(len(t))
    for i in range(k[0], k[1]):
        y = y + normedsin(i*f,t);
    return np.divide(y,len(k))

# -----------------------------------------------------------------
# ------------ Sound generation functions (Experiment dependent)
# -----------------------------------------------------------------


def make_flanker(exp):
    # loading parameters
    f0 = exp.f0
    duration_stim = exp.duration_stim
    rate = exp.rate
    harmonics_flanker = exp.harmonics_flanker
    # function
    time_stim = make_time(duration_stim,rate)
    fi = np.sqrt(2)*f0  # fi is here between f0 and 2f0
    return normalize(hct(fi,time_stim,harmonics_flanker))

def make_act_target(ratio,f,f_c, exp):
    # loading parameters
    duration_stim = exp.duration_stim
    rate = exp.rate
    # function
    time_stim = make_time(duration_stim,rate)
    #fir,N,nyq_rate = filt.make_low_pass_FIR(f_c,f_w,rate)
    a,b = filt.make_low_pass_butterworth(f_c, 6,rate)  
    return normalize(filt.apply_filter(act(1,1/float(ratio),f,time_stim),a,b))

def make_act_control(ratio,f,f_c,exp):
    # loading parameters
    duration_stim = exp.duration_stim
    rate = exp.rate
    # function
    time_stim = make_time(duration_stim,rate)
    #fir,N,nyq_rate = filt.make_low_pass_FIR(f_c,f_w,rate)
    a,b = filt.make_low_pass_butterworth(f_c, 6,rate)   
    x= filt.apply_filter(act(0,1/float(ratio),f,time_stim),a,b)
    y= filt.apply_filter(act(1,1/float(ratio),f,time_stim),a,b)
    return np.divide(x,np.std(y)) # cross normalization

def make_hct_target(f,f_c,exp):
    # loading parameters
    duration_stim = exp.duration_stim
    rate = exp.rate
    # function

    k = np.array([0,int(np.floor(f_c/f))]) # crop harmonics over f_c
    print(k)
    time_stim = make_time(duration_stim,rate)
    return normalize(hct(f,time_stim,k)) # no filtering

    
# stim is as follows : flanker (60ms), blank (100ms), target (60ms), blank (100ms), flanker (60ms)
def make_triplet(flanker,target,exp):
    # loading parameters
    rate = exp.rate
    interval = exp.interval
    # function
    stim = np.zeros(2*len(flanker)+len(target)+2*rate*interval)
    i = 0; stim = add_to_stim(stim,(flanker),i)
    i = i + len(flanker)+rate*interval; stim = add_to_stim(stim,(target),i)
    i = i + len(target)+rate*interval;  stim = add_to_stim(stim,(flanker),i)
    return stim


# calls individual target functions that outputs normalized signals (std = 1)
def make_target(i,exp):
    # loading parameters
    Sound_array = exp.Sound_array
    # function
    stim_op = Sound_array[i]
    print(stim_op)
    stim_type = stim_op[0] # ACT Stimuli
    if (stim_type == 0):
        f = stim_op[1]
        ratio = stim_op[2]
        f_c = stim_op[4]
        target = make_act_target(ratio,f,f_c,exp)
    if (stim_type == 1): # HCT Stimuli
        f = stim_op[1]
        f_c = stim_op[3]
        target = make_hct_target(f,f_c,exp)
    if (stim_type == 2): # ACT Controls
        f = stim_op[1]
        ratio = stim_op[2]
        f_c = stim_op[4]
        target = make_act_control(ratio,f,f_c,exp)
    return target


# noise is added assuming a signal std of 1
def make_noisy_stim(i,exp):
    # loading parameters
    rate = exp.rate
    Sound_array = exp.Sound_array
    f_c_noise = exp.f_c_noise
    # function
    y = make_triplet( make_flanker(exp),make_target(i,exp),exp)
    snrdb = Sound_array[i][2]
    y = y+10**(-snrdb/20)*make_lp_noise(len(y),f_c_noise,rate)
    return y

def make_training_sound(i,exp):
    # loading parameters
    duration_stim = exp.duration_stim
    rate = exp.rate
    f0 = exp.f0
    fi = np.exp((2*np.log(f0)-np.log(2))/2) 

    # function
    time_stim = make_time(duration_stim,rate)
    x1 = normalize(normedsin(fi,time_stim))
    x2 = normalize(normedsin(i*f0,time_stim))
    
    y = make_triplet(x1,x2,exp)
    return y

