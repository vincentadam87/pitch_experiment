# Functions to build sounds

import numpy as np
import filtering as filt
import random
from scipy.signal import hilbert, convolve
# -----------------------------------------------------------------
# ------------ Base functions (Experiment independent)
# -----------------------------------------------------------------

# Normalizing sounds (set std to 1)
def normalize(x):
    return np.divide(x,np.std(x))

# shift signal by half period
def half_period_shift(x,f0,rate):
    y = np.zeros(len(x))
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

def ABAB(A,B,f,t):
    rate = 1/(t[1]-t[0])
    y = np.zeros(len(t))
    c1 = dirac_comb(f,t)
    c2 = half_period_shift(dirac_comb(f,t),f,rate)
    y1 = convolve(A,c1)
    y2 = convolve(B,c2)
    y = y1+ y2
    return y[0:len(t)]

def ABABl(f,l,timbre,t,fs):
    Np = int(fs/f/2.*0.8)
    A = np.random.randn(Np)
    B = np.random.randn(Np)
    C = l*A+(1-l)*B
    y = ABAB(A,C,f,t)
    (af,bf) = filt.make_low_pass_butterworth(timbre, 6,fs)
    y = filt.apply_filter(y,af,bf)
    return y[0:len(t)]

#def ABABl(f,l,timbre,t):
#    fsamp = 1/(t[1]-t[0])
#    T_omega = 1/float(f) #  
#    N_omega = fsamp/f
#    t_omega = np.linspace(0, T_omega*f, N_omega)
#    # enveloppe
#    N_env = int(N_omega/4)  # in proportion of period
#    t_env = t_omega[0:N_env-1]
#    T_env = t_env[-1]
#    env = np.ones(len(t_omega))
#    env[0:N_env-1] = 1/2-np.cos(np.pi*t_env/T_env)
#    env[-N_env+1:] = np.cos(np.pi*t_env/T_env)
#    env = (env +1)/2
#    env = env**2
#    # filters
#    (af,bf) = filt.make_low_pass_butterworth(timbre, 6,fsamp)#
#
#    # sounds
#    #A = np.random.normal(size=N_omega)
#    time_env = np.arange(len(env))/fsamp
#    A = hct(f,time_env,[0,20])
#    #B = np.random.normal(size=N_omega)
#    B = np.imag(hilbert(A))
#
#    # Filtering after modulating
#    #env = np.ones(env.shape)
#    A_filt = filt.apply_filter(A*env,af,bf)
#    B_filt = filt.apply_filter(B*env,af,bf)
#    C_filt = A_filt*l + (1-l)*B_filt
#
#    N_rep = int(fsamp*t[-1]/N_omega) +1# repeat for a sec#
#
#    AB = np.tile(np.concatenate((A_filt,C_filt),1), N_rep/2)
#    return AB[0:len(t)]


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

def make_act_target(ratio,f,timbre, exp):
    # loading parameters
    duration_stim = exp.duration_stim
    rate = exp.rate
    # function
    time_stim = make_time(duration_stim,rate)
    #fir,N,nyq_rate = filt.make_low_pass_FIR(f_c,f_w,rate)

    y = act(1,1/float(ratio),f,time_stim)
    if (timbre == exp.DARK):
        f_c = exp.fc_ACT_DARK
        a,b = filt.make_low_pass_butterworth(f_c, 6,rate)  
        z= normalize(filt.apply_filter(y,a,b))
    if (timbre == exp.BROAD):
        z = normalize(y)
    return z


def make_act_control(ratio,f,timbre,exp):
    # loading parameters
    duration_stim = exp.duration_stim
    rate = exp.rate
    # function
    time_stim = make_time(duration_stim,rate)
    #fir,N,nyq_rate = filt.make_low_pass_FIR(f_c,f_w,rate)

    if (timbre == exp.DARK):
        f_c = exp.fc_ACT_DARK
        a,b = filt.make_low_pass_butterworth(f_c, 6,rate)  
        x= filt.apply_filter(act(0,1/float(ratio),f,time_stim),a,b)
        y= filt.apply_filter(act(1,1/float(ratio),f,time_stim),a,b)
        return np.divide(x,np.std(y)) # cross normalization
    if (timbre == exp.BROAD):
        x= act(0,1/float(ratio),f,time_stim)
        y= act(1,1/float(ratio),f,time_stim)
        return np.divide(x,np.std(y)) # cross normalization

def make_hct_target(f,timbre,exp):
    # loading parameters
    duration_stim = exp.duration_stim
    rate = exp.rate
    # function

    if (timbre == exp.DARK):
        f_c = exp.fc_HCT_DARK
    if (timbre == exp.BROAD):
        f_c = exp.fc_HCT_BROAD

    k = np.array([0,int(np.floor(f_c/f))]) # crop harmonics over f_c
    print(k)
    time_stim = make_time(duration_stim,rate)
    return normalize(hct(f,time_stim,k)) # no filtering

def make_ABABl_target(f,lmbda,timbre,exp):
    # loading parameters
    duration_stim = exp.duration_stim
    rate = exp.rate
    # function

    if (timbre == exp.DARK):
        f_c = exp.fc_HCT_DARK
    if (timbre == exp.BROAD):
        f_c = exp.fc_HCT_BROAD

    time_stim = make_time(duration_stim,rate)
    return normalize(ABABl(f,lmbda,f_c,time_stim,rate))     

    
# stim is as follows : flanker (60ms), blank (100ms), target (60ms), blank (100ms), flanker (60ms)
def make_triplet(flanker,target,exp):
    # loading parameters
    rate = exp.rate
    interval = exp.interval
    se_blank_duration = exp.se_blank_duration
    # function
    stim = np.zeros(2*len(flanker)+len(target)+2*rate*interval + 2*rate*se_blank_duration)
    i = 0+rate*se_blank_duration; stim = add_to_stim(stim,(flanker),i)
    i = i + len(flanker)+rate*interval; stim = add_to_stim(stim,(target),i)
    i = i + len(target)+rate*interval;  stim = add_to_stim(stim,(flanker),i)
    return stim


# calls individual target functions that outputs normalized signals (std = 1)
def make_target(i,exp):
    # loading parameters
    Sound_array = exp.Sound_array
    # function
    stim_op = Sound_array[i]
    stim_type = stim_op[0] # ACT Stimuli
    if (stim_type == 0):
        f = stim_op[2]
        ratio = stim_op[3]
        timbre = stim_op[4]
        target = make_act_target(ratio,f,timbre,exp)
        name = "ACT target [-,snrdb,-,ratio,timbre]"
    if (stim_type == 1): # HCT Stimuli
        f = stim_op[2]
        timbre = stim_op[3]
        target = make_hct_target(f,timbre,exp)
        name = "HCT target [-,snrdb,f0,timbre]"
    if (stim_type == 2): # ACT Controls
        f = stim_op[2]
        ratio = stim_op[3]
        timbre = stim_op[4]
        target = make_act_control(ratio,f,timbre,exp)
        name = "ACT control [-,snrdb,-,ratio (one CT only),timbre]"
    if (stim_type == 3): # ABAB
        f = stim_op[2]
        lmbda = stim_op[3]
        timbre = stim_op[4]
        target = make_ABABl_target(f,lmbda,timbre,exp)
        name = "ABAB [-,snrdb,-,lmbda ,timbre]"
    print(name)
    print(stim_op)
    return target




# noise is added assuming a signal std of 1
def make_noisy_stim(i,exp):
    # loading parameters
    rate = exp.rate
    Sound_array = exp.Sound_array
    f_c_noise = exp.f_c_noise
    # function
    y = make_triplet( make_flanker(exp),make_target(i,exp),exp)
    
    snrdb = Sound_array[i][1]
    print(snrdb)
    y = y+10**(-snrdb/20)*make_lp_noise(len(y),f_c_noise,rate)
    return y

def add_lpnoise_at_snrdb(x,snrdb,exp):
    # loading parameters
    rate = exp.rate
    f_c_noise = exp.f_c_noise
    y = x+10**(-snrdb/20)*make_lp_noise(len(x),f_c_noise,rate)
    return y

def make_random_training_sound(session,exp):
    print exp.Training_sounds
    indices = exp.Training_sounds[session-1]
    N_indices = len(indices)
    i = random.randint(1,N_indices)
    return make_noisy_stim(indices[i-1],exp)
    

# ---------- Addition for ABX task

