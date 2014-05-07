from psychopy import core, visual, gui, data, event
from psychopy.misc import fromFile, toFile
import time, numpy, random
import exp_param, sound_build
import pygame
from scipy.io.wavfile import write
import numpy as np

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
        expInfo = fromFile('lastParams.pickle') # check existence of previous parameter file
    except:
        expInfo = {'pseudo':'pseudo'}
        expInfo['date']= data.getDateStr() #add current time
    #present a dialog box to get user info
    dlg = gui.DlgFromDict(expInfo, title='Experiment', fixed=['date'])
    if dlg.OK:
        toFile('lastParams.pickle', expInfo)#save params to file for next time
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
    
def run_calibration():
    # display instructions
    set_msg('SET SOUND LEVEL','TITLE')
    set_msg('press up and down to increase/decrease sound level and press enter when level is confortable','MAIN')
    win.flip()
    # prepare calibration sound
    level = Exp.level
    s = sound_build.make_lp_noise(100000,3000,Exp.rate)
    scaled = np.int16(s*level)
    write('test.wav', 44100, scaled)
    # run calibration
    pygame.mixer.init()
    pygame.mixer.music.load("test.wav")
    pygame.mixer.music.play(200)
    pygame.mixer.music.set_volume(0.5)
    pressEnter = False
    while pressEnter==False:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='up':
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.1)
                print(pygame.mixer.music.get_volume())
            elif thisKey=='down':
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.1)
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
    N_stims = len(Exp.Training_sounds[session-1])
    while (core.getTime()<time_stop):
        
        i = random.randint(1,N_stims)
        s = sound_build.make_random_training_sound(session,Exp)
        scaled = np.int16(s/np.max(np.abs(s)) * 32767)
        write('test.wav', 44100, scaled)       
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.load("test.wav")
        core.wait(time_play - core.getTime())
        set_msg('Up or down?','MAIN')
        win.flip()        
        pygame.mixer.music.play()        
        
        thisResp = get_response()
        time_play =  core.getTime() + iti
        

def run_main_experiment():
    time_start = core.getTime()
    time_play = time_start
    order = Exp.make_random_stim_order()
    for i in order[1:10]:
        s = sound_build.make_noisy_stim(i,Exp)
        scaled = np.int16(s/np.max(np.abs(s)) * 32767)
        write('test.wav', 44100, scaled)
        core.wait(0.2) 
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.load("test.wav")
        core.wait(time_play - core.getTime())
        
        set_msg('Up or down?','MAIN')
        win.flip()        
        pygame.mixer.music.play()
        core.wait(1) 
        #core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen
        thisResp = get_response()
        time_play =  core.getTime() + iti
        dataFile.write('%i,%i\n' %(i, thisResp))
        core.wait(1)
    dataFile.close()





#------------ initial information input window

expInfo = get_subject_info()
#make a text file to save data

fileName = expInfo['pseudo'] + expInfo['date']
dataFile = open(fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
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

######### TRAINING Sessions #######################
training_duration = 5


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

set_msg('SESSION 1','TITLE')
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

message1 = visual.TextStim(win, pos=[0,+3],text='Hit a key when ready for the real experiment.')
message1.draw()
win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()

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