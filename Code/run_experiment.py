
from psychopy import core, visual, gui, data, event
from psychopy.misc import fromFile, toFile
import time, numpy, random
import exp_param, sound_build
import pygame
from scipy.io.wavfile import write
import numpy as np


try:#try to get a previous parameters file
    expInfo = fromFile('lastParams.pickle')
except:#if not there then use a default set
    expInfo = {'subject':'pseudo'}
expInfo['dateStr']= data.getDateStr() #add the current time
#present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Pitch experiment', fixed=['dateStr'])
if dlg.OK:
    toFile('lastParams.pickle', expInfo)#save params to file for next time
else:
    core.quit()#the user hit cancel so exit

#make a text file to save data
fileName = expInfo['subject'] + expInfo['dateStr']
dataFile = open(fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
dataFile.write('stim index,chosen dir\n')

                          
#create window and stimuli
win = visual.Window([800,600],allowGUI=True, monitor='testMonitor', units='deg')

#and some handy clocks to keep track of time
globalClock = core.Clock()
trialClock = core.Clock()

##################################################
######### SOUND CALIBRATION #######################
Exp = exp_param.exp_param()


message0 = visual.TextStim(win, pos=[0,+3],text='CALIBRATION')
message0.draw()

message1 = visual.TextStim(win, pos=[0,-3],text='press up and down to increase sound level and press enter when level is confortable')
message1.draw()
win.flip()#to show our newly drawn 'stimuli'

pressEnter = False

level = Exp.level

s = sound_build.make_lp_noise(100000,Exp)
scaled = np.int16(s*level)
write('test.wav', 44100, scaled)
pygame.mixer.init()
pygame.mixer.music.load("test.wav")
pygame.mixer.music.play(200)
pygame.mixer.music.set_volume(0.5)

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

#################################################
######### INSTRUCTIONS ##########################

#display instructions and wait
message1 = visual.TextStim(win, pos=[0,+3],text='INSTRUCTIONS')
message2 = visual.TextStim(win, pos=[0,0], 
    text="press up or down to charaterize middle tone relative move")
message1.draw()
message2.draw()

message1 = visual.TextStim(win, pos=[0,3],text='Hit a key when ready.')

win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()


##################################################
######### TRAINING #######################

message3 = visual.TextStim(win, pos=[0,-3],text='We will now begin a short training session')
message3.draw()
win.flip()
core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen

################

for t in range(0,2):
    i = random.randint(1,2)
    s = sound_build.make_training_sound(i,Exp)
    scaled = np.int16(s*level)
    write('test.wav', 44100, scaled)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load("test.wav")
    pygame.mixer.music.play()
    core.wait(1) 

    message3 = visual.TextStim(win, pos=[0,-3],text='Listen now')
    message3.draw()
    win.flip()
    core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen

    targetSide = 0

    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='up':
                if targetSide==-1: thisResp = 1#correct
                else: thisResp = -1             #incorrect
            elif thisKey=='down':
                if targetSide== 1: thisResp = 1#correct
                else: thisResp = -1             #incorrect
            elif thisKey in ['q', 'escape']:
                core.quit() #abort experiment
        event.clearEvents() #must clear other (eg mouse) events - they clog the buffer


event.waitKeys()

################################################


message1 = visual.TextStim(win, pos=[0,+3],text='Hit a key when ready for the real experiment.')
message1.draw()
win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()
##################################################

# Before starting the experiment choose an ordering
order = Exp.make_random_stim_order()

for i in order: 
#set location of stimuli
    targetSide = 1 # is tone up or down 
    message3 = visual.TextStim(win, pos=[0,-3],text='Listen now')
    message3.draw()
    win.flip()
    core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen
                              # eg, to get 30 frames: for f in xrange(30): win.flip()
    #blank screen


#############################################################
    data = np.random.uniform(-1,1,44100) # 44100 random samples between -1 and 1
    s = sound_build.make_noisy_stim(i,Exp)
    scaled = np.int16(s*level)
    write('test.wav', 44100, scaled)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load("test.wav")
    pygame.mixer.music.play()
#############################################################

    win.flip()

    #get response
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='up':
                if targetSide==-1: thisResp = 1#correct
                else: thisResp = -1             #incorrect
            elif thisKey=='down':
                if targetSide== 1: thisResp = 1#correct
                else: thisResp = -1             #incorrect
            elif thisKey in ['q', 'escape']:
                core.quit() #abort experiment
        event.clearEvents() #must clear other (eg mouse) events - they clog the buffer

    #add the data to the staircase so it can calculate the next level
    dataFile.write('%i,%i\n' %(i, targetSide))
    core.wait(1)

#staircase has ended
dataFile.close()

#give some output to user in the command line in the output window
feedback1 = visual.TextStim(win, pos=[0,+3],
    text='thanks')
feedback1.draw()
win.flip() 

event.waitKeys() #wait for participant to respond

win.close()
core.quit()