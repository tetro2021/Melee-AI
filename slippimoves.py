import random
import melee
from melee import enums
import numpy
from numpy.random import choice

def shortHopLaser(ai_state, controller):
    
    if ai_state.action == enums.Action.STANDING:
        controller.release_all()
        controller.press_button(enums.Button.BUTTON_Y)
        return
    if ai_state.action == enums.Action.LANDING:
            #print("Got here")
            controller.release_all()
            if ai_state.action_frame == 4:
                controller.press_button(enums.Button.BUTTON_Y)
                return
    if not ai_state.on_ground:
        controller.press_button(enums.Button.BUTTON_B)
        if ai_state.action_frame == 4:
            controller.release_button(enums.Button.BUTTON_B)
    else:
        controller.release_button(enums.Button.BUTTON_Y)


def SDILeft(ai_state, controller):
    if ai_state.hitstun_frames_left != 0:
        if (controller.current.main_stick != (0,0.5)):
            controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, 0.5)
            #print(controller.current.main_stick)
        else:
            controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5, 0.5)
            #print(controller.current.main_stick)
    else:
        controller.release_all()


def SDIRight(ai_state, controller):
    if ai_state.hitstun_frames_left != 0:
        if (controller.current.main_stick != (1,0.5)):
            controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, 0.5)
            #print(controller.current.main_stick)
        else:
            controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5, 0.5)
            #print(controller.current.main_stick)
    else:
        controller.release_all()


def SDIDownLeft(ai_state, controller):
    # if ai_state.action == enums.Action.THROWN_UP:
    #     #controller.release_all()
    #     if controller.current.main_stick != (0,0):
    #         #print("got here")
    #         controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, 0)
    if ai_state.hitlag:
        if (controller.current.main_stick != (0,0)):
            #controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, 0)
            #print(controller.current.main_stick)
        else:
            #controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5, 0.5)
            #print(controller.current.main_stick)
    else:
        controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5, 0.5)

def SDIDownRight(ai_state, controller):
    # if ai_state.action == enums.Action.THROWN_UP:
    #     #controller.release_all()
    #     if controller.current.main_stick != (0,0):
    #         #print("got here")
    #         controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, 0)
    if ai_state.hitlag:
        if (controller.current.main_stick != (1,0)):
            #controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, 0)
            #print(controller.current.main_stick)
        else:
            #controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5, 0.5)
            #print(controller.current.main_stick)
    else:
        controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5, 0.5)


def faceOpponent(ai_state, controller, player_state):
    if ai_state.on_ground:
        if ai_state.facing and (ai_state.x > player_state.x):
            print("Facing right flip left")
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.4,0.5)
        elif not ai_state.facing and (ai_state.x < player_state.x):
            print("Facing left flip right")
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.6,0.5)
        else:
            controller.release_all()



def simpleFoxAI(ai_state, controller, player_state):
    if ai_state.on_ground:
        if ai_state.facing:
            if ai_state.x > player_state.x:
                #print("Facing right flip left")
                controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.4,0.5)
            else:
                controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5,0.5)
                #SDIDownLeft(ai_state,controller)
                shortHopLaser(ai_state,controller)
        elif not ai_state.facing: 
            if ai_state.x < player_state.x:
                #print("Facing left flip right")
                controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.6,0.5)
            else:
                controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5,0.5)
                #SDIDownRight(ai_state,controller)
                shortHopLaser(ai_state, controller)
    else:
        if ai_state.x < player_state.x:
            SDIDownLeft(ai_state,controller)
        else:
            SDIDownRight(ai_state,controller)
        shortHopLaser(ai_state,controller)



def PoorlyMadeTechplacement(ai_state, controller, stagePositiony):
    if ai_state.on_ground:
            if ai_state.y < stagePositiony:
                stagePositiony = ai_state.y
                print(stagePositiony)
            if ai_state.y < stagePositiony:
                #print("This is stage position: ")
                #print(stagePositiony)
                #print("this is ai_state")
                #print(ai_state.y)
                controller.press_button(enums.Button.BUTTON_L)
            else:
                #print("This is stage position BIGGER: ")
                #print(stagePositiony)
                #print("this is ai_state SMALLER")
                #print(ai_state.y)
                controller.release_button(enums.Button.BUTTON_L)




def SimpleTech(ai_state, controller, numtecs, numsuccess):
    if (ai_state.y < 0 and not ai_state.on_ground and not ai_state.off_stage and not ai_state.hitlag and (ai_state.speed_y_self + ai_state.speed_y_attack) < -0.01):
        controller.release_all()
        #random.seed(466514514)
        x = randomizeProbability(numtecs, numsuccess)
        options[x](controller)
        #print(x)
        ydiff = ai_state.ecb_bottom[1]
        y = ai_state.y
        #print(y -ydiff)
        #print("\n")
        #print(y)
        return True
    else:
        if ai_state.on_ground:
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5,0.5)
            controller.release_all()
            return False
        #controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5,0.5)
        controller.release_button(enums.Button.BUTTON_L)
        return False



def TechLeft(controller):
    controller.press_button(enums.Button.BUTTON_L)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0,0.5)
def TechRight(controller):
    controller.press_button(enums.Button.BUTTON_L)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 1,0.5)
def TechNormal(controller):
    controller.press_button(enums.Button.BUTTON_L)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5,0.5)
def TechDont(controller):
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5,0.5)

options = {0 : TechLeft,
           1 : TechRight,
           2 : TechNormal,
}



def randomizeProbability(numtecs, numsuccess):
    lefProb = 0.3
    rightProb = 0.3
    normProb = 0.4
    if numsuccess[0] != 0:
        leftProb = numtecs[0]/numsuccess[0]
        #print("Left Prob is: " + str(leftProb))
    if numsuccess[1] != 0:
        rightProb = numtecs[1]/numsuccess[1]
    if numsuccess[2] != 0:
        normProb = numtecs[2]/numsuccess[2]
    sum = lefProb + rightProb + normProb
    probarray = [lefProb/sum, rightProb/sum, normProb/sum]
    print(probarray)
    return choice(3,p=probarray)
    

class RecordStates:
    def __init__ (recorder, numtecs, numsuccess, inTech, teching, shouldSpotdoge, currentPercent):
        recorder.numtecs = numtecs
        recorder.numsuccess = numsuccess
        recorder.inTech = inTech
        recorder.teching = teching
        recorder.shouldSpotdoge = shouldSpotdoge
        recorder.currentPercent = currentPercent

    def recordTech(recorder, ai_state, controller, player_state):
        if recorder.shouldSpotdoge == 0:
            if ai_state.action != enums.Action.SPOTDODGE:
                if recorder.currentPercent == ai_state.percent:
                    controller.press_button(enums.Button.BUTTON_L)
                    controller.tilt_analog(enums.Button.BUTTON_C, 0.5,0)
                else:
                    recorder.shouldSpotdoge = 3
                    print("\nFAILURE TECHLEFT!!!!\n\n")
            elif ai_state.action_frame > 2:
                recorder.shouldSpotdoge = 3
                print("Sucsess")
                recorder.numsuccess[0] += 1
        elif recorder.shouldSpotdoge == 1:
            if ai_state.action != enums.Action.SPOTDODGE:
                if recorder.currentPercent == ai_state.percent:
                    controller.press_button(enums.Button.BUTTON_L)
                    controller.tilt_analog(enums.Button.BUTTON_C, 0.5,0)
                else:
                    recorder.shouldSpotdoge = 3
                    print("\nFAILURE TECHRIGHT!!!!\n\n")
            elif ai_state.action_frame > 2:
                recorder.shouldSpotdoge = 3
                print("Sucsess")
                recorder.numsuccess[1] += 1
        elif recorder.shouldSpotdoge == 2:
            if ai_state.action != enums.Action.SPOTDODGE:
                if recorder.currentPercent == ai_state.percent:
                    controller.press_button(enums.Button.BUTTON_L)
                    controller.tilt_analog(enums.Button.BUTTON_C, 0.5,0)
                else:
                    recorder.shouldSpotdoge = 3
                    print("\nFAILURE TECHNORMAL!!!!\n\n")
            elif ai_state.action_frame > 2:
                recorder.shouldSpotdoge = 3
                print("Sucsess")
                recorder.numsuccess[2] += 1
        else:
            recorder.teching = SimpleTech(ai_state, controller, recorder.numtecs, recorder.numsuccess)
            if not recorder.teching:
                simpleFoxAI(ai_state, controller, player_state)





        if(ai_state.action == enums.Action.NEUTRAL_TECH):
            if ai_state.action_frame == 1:
                recorder.currentPercent = ai_state.percent
                recorder.numtecs[2] +=1
                recorder.shouldSpotdoge = 2
                print("Neutral Tech\n")
                print(recorder.numtecs)
        if(ai_state.action == enums.Action.FORWARD_TECH):
            if ai_state.facing:
                if ai_state.action_frame == 1:
                    recorder.currentPercent = ai_state.percent
                    recorder.numtecs[1] +=1
                    recorder.shouldSpotdoge = 1
                    print("TechRight")
            else:
                if ai_state.action_frame == 1:
                    recorder.currentPercent = ai_state.percent
                    recorder.numtecs[0] +=1
                    recorder.shouldSpotdoge = 0
                    print("TechLeft")
        if(ai_state.action == enums.Action.BACKWARD_TECH):
            if ai_state.facing:
                if ai_state.action_frame == 1:
                    recorder.currentPercent = ai_state.percent
                    recorder.numtecs[0] +=1
                    recorder.shouldSpotdoge = 0
                    print("TechLeft")
            else:
                if ai_state.action_frame == 1:
                    recorder.currentPercent = ai_state.percent
                    recorder.numtecs[1] +=1
                    recorder.shouldSpotdoge = 1
                    print("TechRight")

        
        