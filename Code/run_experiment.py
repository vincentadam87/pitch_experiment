
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
TOP_POS = [0,+3]
CENTER_POS = [0,0]
BOTTOM_POS = [0,-3]
# ---------------------
def get_subject_info():
    try:#try to get a previous parameters file
        expInfo = fromFile('lastParams.pickle')
    except:#if not there then use a default set
        expInfo = {'pseudo':'pseudo'}
        expInfo['date']= data.getDateStr() #add the current time
    #present a dialog box to change params
    dlg = gui.DlgFromDict(expInfo, title='Experiment', fixed=['date'])
    if dlg.OK:
        toFile('lastParams.pickle', expInfo)#save params to file for next time
    else:
        core.quit()#the user hit cancel so exit
    return expInfo

def run_calibration():
    # display instructions
    message_cal= visual.TextStim(win,text='SET SOUND LEVEL', pos=TOP_POS, bold=True)
    message_cal_instr = visual.TextStim(win,text='press up and down to increase/decrease sound level and press enter when level is confortable',pos=CENTER_POS,wrapWidth = 30)
    message_cal.draw()
    message_cal_instr.draw()
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
    message_title = visual.TextStim(win,text='INSTRUCTIONS', pos=TOP_POS, bold=True )
    message_instr = visual.TextStim(win, text="press up or down to charaterize the melodic contour of the sound you hear (Up-Down or Down-Up)", pos=CENTER_POS,wrapWidth = 30)
    message_presskey = visual.TextStim(win,text='Hit a key when ready.', pos=BOTTOM_POS)
    message_title.draw()
    message_instr.draw()
    message_presskey.draw()
    win.flip()#to show our newly drawn 'stimuli'
    #pause until there's a keypress
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
                message3 = visual.TextStim(win, pos=[0,-3],text='Oops!')
                message3.draw()
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

        message3 = visual.TextStim(win, pos=[0,-3],text='Up or down?')
        message3.draw()
        win.flip()        
        pygame.mixer.music.play()
        
        #core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen
        
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
        
        
        message3 = visual.TextStim(win, pos=[0,-3],text='Up or down?')
        message3.draw()
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

message_sessions_title = visual.TextStim(win,text='TRAINING SESSIONS', pos=TOP_POS, bold=True)
message_sessions_intro = visual.TextStim(win,text='We will now begin two short training sessions', pos=CENTER_POS)
message_presskey = visual.TextStim(win,text='Hit a key when ready.', pos=BOTTOM_POS)
message_sessions_title.draw()
message_sessions_intro.draw()
message_presskey.draw()
win.flip()
event.waitKeys()
core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen

message_session1 = visual.TextStim(win, pos=[0,3],text='Session 1')
message_presskey = visual.TextStim(win, pos=[0,-3],text='Hit a key when ready.')
message_session1.draw()
message_presskey.draw()
win.flip()
event.waitKeys()
run_training(1,training_duration)
message_session1 = visual.TextStim(win, pos=[0,3],text='Session 1 completed')
message_presskey = visual.TextStim(win, pos=[0,-3],text='Hit a key when ready.')
message_session1.draw()
message_presskey.draw()
win.flip()
event.waitKeys()

message_session2 = visual.TextStim(win, pos=[0,3],text='Session 2')
message_presskey = visual.TextStim(win, pos=[0,-3],text='Hit a key when ready.')
message_session2.draw()
message_presskey.draw()
win.flip()
event.waitKeys()
win.flip()
run_training(2,training_duration)
message_session2= visual.TextStim(win, pos=[0,3],text='Session 2 completed')
message_presskey = visual.TextStim(win, pos=[0,-3],text='Hit a key when ready.')
message_session2.draw()
message_presskey.draw()
win.flip()
event.waitKeys()
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