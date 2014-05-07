from psychopy import core, visual, gui, data, event
from psychopy.misc import fromFile, toFile

from scipy.io.wavfile import write
import numpy as np
import pygame

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
    set_msg('You will perform two small training sessions and the main experiment. The coming instructions apply to the whole experiment','MAIN')
    set_msg('Press any key to continue','KEY')
    win.flip()
    core.wait(0.5)
    event.waitKeys()

    set_msg('INSTRUCTIONS','TITLE')
    set_msg('press up or down to charaterize the melodic contour of the sound you hear : Up-Down or Down-Up (you will hear some examples during training sessions)','MAIN')
    set_msg('Press any key to continue','KEY')
    win.flip()
    core.wait(0.5)
    event.waitKeys()


    set_msg('INSTRUCTIONS','TITLE')
    set_msg('the purpose of the experiment is to probe your subjective perceptual experience. There is no strictly right or wrong response in any trial','MAIN')
    set_msg('Press any key to continue','KEY')
    win.flip()
    core.wait(0.5)
    event.waitKeys()

    set_msg('INSTRUCTIONS','TITLE')
    set_msg('Some trials will be ambiguous. In such trials, try to answer rapidly according to your best judgement','MAIN')
    set_msg('Press any key to continue','KEY')
    win.flip()
    core.wait(0.5)
    event.waitKeys()

    set_msg('INSTRUCTIONS','TITLE')
    set_msg('Your choices have no influence in what stimulus comes next. If you hear the same stimulus consecutively this is just chance in action','MAIN')
    set_msg('Press any key to continue','KEY')
    win.flip()
    core.wait(0.5)
    event.waitKeys()


def get_response():
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='up':
                win.flip()
                thisResp = 1 # UP
            elif thisKey=='down':
                win.flip()
                thisResp = -1# DOWN
            elif thisKey in ['q', 'escape']:
                core.quit() #abort experiment
            else:
                thisResp = 0
                set_msg('Oops','KEY')
        event.clearEvents() #must clear other (eg mouse) events - they clog the buffer
        win.flip()        
    return thisResp

def run_training(session,duration):
    time_start = core.getTime()
    time_play = time_start
    time_stop = time_start + duration
    while (core.getTime()<time_stop):
        
        s = sound_build.make_random_training_sound(session,Exp)     
        core.wait(time_play - core.getTime())
        set_msg('Up or down?','MAIN')
        win.flip()        
        playsound(s,vol)
        get_response()
        print(core.getTime() -time_start)
        time_play =  core.getTime() + iti
        

def run_main_experiment():
    time_start = core.getTime()
    time_play = time_start
    order = Exp.make_random_stim_order()
    Nonethird = np.floor(len(order)/3)
    Ntwothird = np.floor(2*len(order)/3)

    t = 0
    for i in order:
        t = t+1
        print(core.getTime() -time_start)
        if t in [Nonethird,Ntwothird]:
            set_msg('Short Break!','MAIN')
            set_msg('Press return to continue','KEY')
            win.flip()
            event.waitKeys(keyList=['return','space'])
            core.wait(1) 



        s = sound_build.make_noisy_stim(i,Exp)
        scaled = np.int16(s/np.max(np.abs(s)) * 32767)
        write('test.wav', 44100, scaled)
        core.wait(time_play - core.getTime())        
        set_msg('Up or down?','MAIN')
        win.flip()        
        playsound(s,vol)
        core.wait(0.1) 
        #core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen
        thisResp = get_response()
        iscorrect = Exp.isRespCorrect(i,thisResp) # 1=correct, O=incorrect, -1=missed
        time_play =  core.getTime() + iti
        dataFile.write('%i,%i,%i\n' %(i, thisResp,iscorrect))
    dataFile.close()





#------------ initial information input window

expInfo = get_subject_info()
#make a text file to save data

fileName = expInfo['pseudo'] + expInfo['date']
dataFile = open('../data/'+fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
dataFile.write('stim index,chosen dir,correct\n')

#create window and stimuli
#win = visual.Window([800,600],fullscr=True,allowGUI=True, monitor='testMonitor', units='deg')
win = visual.Window([800,600],fullscr=False,allowGUI=True, monitor='testMonitor', units='deg')

#and some handy clocks to keep track of timemake_random_stim_order
globalClock = core.Clock()
trialClock = core.Clock()

######### SOUND CALIBRATION #######################
vol = run_calibration()
######### Task INSTRUCTIONS ##########################
display_instructions() 

######### TRAINING Sessions #######################
training_duration = Exp.Training_duration


set_msg('TRAINING SESSIONS','TITLE')
set_msg('We will now begin two short training sessions','MAIN')
set_msg('Press return to continue','KEY')
win.flip()

event.waitKeys(keyList=['return','space'])


set_msg('SESSION 1','TITLE')
set_msg('Press enter to begin','KEY')
win.flip()
event.waitKeys(keyList=['return'])
run_training(1,training_duration)

set_msg('SESSION 1','TITLE')
set_msg('Session 1 completed','MAIN')
set_msg('Press enter to continue','KEY')
win.flip()
event.waitKeys(keyList=['return'])

set_msg('SESSION 2','TITLE')
set_msg('Press enter to begin','KEY')
win.flip()
event.waitKeys(keyList=['return'])
run_training(2,training_duration)

set_msg('SESSION 2','TITLE')
set_msg('Session 2 completed','MAIN')
set_msg('Press enter to continue','KEY')
win.flip()
event.waitKeys(keyList=['return'])

############## Main experiment ##################
set_msg('MAIN EXPERIMENT','TITLE')
set_msg('You will now start the main experiment. You will hear a greater variety of sounds than in the training sessions','MAIN')
set_msg('Press return to start','KEY')
win.flip()
event.waitKeys(keyList=['return'])
win.flip()

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
