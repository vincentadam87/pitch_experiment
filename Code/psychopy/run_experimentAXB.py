from psychopy import core, visual, gui, data, event
from psychopy.misc import fromFile, toFile

from scipy.io.wavfile import write
import numpy as np
import pygame
import random
import os, sys
# realpath() with make your script run, even if you symlink it :)
#cmd_subfolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "/scripts")
cmd_subfolder = os.path.realpath('..')+'/scripts'
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import sound_build, exp_param

#------------ load global experiment parameters
Exp = exp_param.exp_param()
iti = Exp.iti

# constants initialization
TOP_POS = [0,+3]
CENTER_POS = [0,0]
BOTTOM_POS = [0,-4]
# function definition

def get_subject_info():
    try:
        expInfo = fromFile('../data/lastParams.pickle') # check existence of previous parameter file
    except:
        expInfo = {'pseudo':'pseudo'}
        expInfo['date']= data.getDateStr() #add current time
    #present a dialog box to get user info
    dlg = gui.DlgFromDict(expInfo, title='Experiment', fixed=['date'])
    if dlg.OK:
        toFile('../data/lastParams.pickle', expInfo)#save params to file for next time
    else:
        core.quit()#cancel -> exit
    return expInfo

def set_msg(txt,type):
    if (type == 'TITLE'):
        m = visual.TextStim(win,text=txt, pos=TOP_POS, bold=True,wrapWidth = 30)
    elif (type == 'MAIN'):
        m = visual.TextStim(win,text=txt, pos=CENTER_POS,wrapWidth = 30)
    elif (type == 'KEY'):
        m = visual.TextStim(win,text=txt, pos=BOTTOM_POS,wrapWidth = 30)
    m.draw()    
    
def playsound(s,vol,it=1):
    scaled = np.int16(s * (2**9-1))#
    write('test.wav', 44100, scaled)
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
    pygame.mixer.music.load("test.wav")
    if not (vol == None):
        pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play(it)

def run_calibration():
    # display instructions
    set_msg('SET SOUND LEVEL','TITLE')
    set_msg('press up and down to increase/decrease sound level and press enter when level is confortable','MAIN')
    set_msg('Press return to continue','KEY')

    win.flip()
    # prepare calibration sound
    s = sound_build.make_lp_noise(100000,3000,Exp.rate)
    vol = 0.5
    playsound(s,vol,200)
    pressEnter = False
    while pressEnter==False:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='up':
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.03)
                print(pygame.mixer.music.get_volume())
            elif thisKey=='down':
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.03)
                print(pygame.mixer.music.get_volume())
            elif thisKey in ['return']:
                pressEnter = True
            elif thisKey in ['q', 'escape']:
                core.quit() #abort experiment
        event.clearEvents() #must clear other (eg mouse) events - they clog the buffer
    vol = pygame.mixer.music.get_volume()
    
    pygame.mixer.music.stop()
    return vol

def display_instructions():
    set_msg('INTRODUCTION','TITLE')
    set_msg('AXB control','MAIN')
    set_msg('Press any key to continue','KEY')
    win.flip()
    core.wait(0.5)
    event.waitKeys()



def get_response():
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='left':
                win.flip()
                thisResp = 0
            elif thisKey=='right':
                win.flip()
                thisResp = 1
            elif thisKey in ['q', 'escape']:
                core.quit() #abort experiment
            else:
                thisResp = 0
                set_msg('Oops','KEY')
        event.clearEvents() #must clear other (eg mouse) events - they clog the buffer
        win.flip()        
    return thisResp


        
def run_main_experiment():
    time_start = core.getTime()
    time_play = time_start
    order = Exp.make_random_stim_order()
    Nonethird = np.floor(len(order)/3)
    Ntwothird = np.floor(2*len(order)/3)

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


    t = 0
    for i in np.arange(0,100):
        t = t+1

        snr_type = random.randint(0,1)
        timbre_type = random.randint(0,1)
        AXB_type =  random.randint(0,1)
        WXZ_type =  random.randint(0,1)

        pair = couples[snr_type]
        A = pair[int(WXZ_type)]
        B = pair[int(not WXZ_type)]
        X = [A,B][AXB_type]

        blank = np.zeros((Exp.rate,1),float)
        seq = np.append(blank,A)
        seq = np.append(seq,blank)
        seq = np.append(seq,X)
        seq = np.append(seq,blank)
        seq = np.append(seq,B)
        seq = np.append(seq,blank)

        snrdb = [0,-6][snr_type]
        s = sb.add_lpnoise_at_snrdb(seq,snrdb,Exp)
        s = sound_build.make_noisy_stim(i,Exp)

        scaled = np.int16(s/np.max(np.abs(s)) * 32767)
        write('test.wav', 44100, scaled)
        core.wait(time_play - core.getTime())        
        set_msg('AAB or ABB?','MAIN')
        win.flip()        
        playsound(s,vol)
        core.wait(0.1) 
        #core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen
        thisResp = get_response()
        iscorrect = (get_response()==AXB_type)

        time_play =  core.getTime() + iti
        dataFile.write('%i,%i,%i,%i,%i,%i\n' %(snr_type,timbre_type,AXB_type,WXZ_type, thisResp,iscorrect))
    dataFile.close()





#------------ initial information input window

expInfo = get_subject_info()
#make a text file to save data

fileName = 'AXB_'+expInfo['pseudo'] + expInfo['date']
dataFile = open('../data/'+fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
dataFile.write('stim index,chosen dir\n')

#create window and stimuli
win = visual.Window([800,600],fullscr=True,allowGUI=True, monitor='testMonitor', units='deg')

#and some handy clocks to keep track of timemake_random_stim_order
globalClock = core.Clock()
trialClock = core.Clock()

######### SOUND CALIBRATION #######################
vol = run_calibration()
######### Task INSTRUCTIONS ##########################
display_instructions() 


run_main_experiment()

################################################

#give some output to user in the command line in the output window
feedback1 = visual.TextStim(win, pos=[0,+3],
    text='thanks')
feedback1.draw()
win.flip() 

event.waitKeys() #wait for participant to respond

win.close()
core.quit()
