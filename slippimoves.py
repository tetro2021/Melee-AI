import melee
from melee import enums

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
            controller.release_all()
    else:
        controller.release_all()


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
    if ai_state.action == enums.Action.THROWN_UP:
        #controller.release_all()
        if controller.current.main_stick != (0,0):
            #print("got here")
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, 0)
    elif ai_state.hitstun_frames_left != 0:
        if (controller.current.main_stick != (0,0)):
            controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, 0)
            #print(controller.current.main_stick)
        else:
            controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5, 0.5)
            #print(controller.current.main_stick)
    else:
        controller.release_all()

def SDIDownRight(ai_state, controller):
    if ai_state.action == enums.Action.THROWN_UP:
        #controller.release_all()
        if controller.current.main_stick != (0,0):
            #print("got here")
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, 0)
    elif ai_state.hitstun_frames_left != 0:
        if (controller.current.main_stick != (1,0)):
            controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, 0)
            #print(controller.current.main_stick)
        else:
            controller.release_all()
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.5, 0.5)
            #print(controller.current.main_stick)
    else:
        controller.release_all()


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
                if ai_state.facing and (ai_state.x > player_state.x):
                    #print("Facing right flip left")
                    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.4,0.5)
                elif not ai_state.facing and (ai_state.x < player_state.x):
                    #print("Facing left flip right")
                    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0.6,0.5)
                else:
                    if ai_state.x < player_state.x:
                        SDIDownLeft(ai_state,controller)
                    else:
                        SDIDownRight(ai_state,controller)
                    shortHopLaser(ai_state,controller)
    else:
        if ai_state.action == enums.Action.TUMBLING:
            controller.press_shoulder(enums.Button.BUTTON_L, )
            print("Got here")
            return
        if ai_state.x < player_state.x:
            SDIDownLeft(ai_state,controller)
        else:
            SDIDownRight(ai_state,controller)
        shortHopLaser(ai_state,controller)


    #else:
        #controller.release_all()




# def ComboDILeft(ai_state, controller):
#     if ai_state.action == enums.Action.THROWN_UP:
#         #controller.release_all()
#         if controller.current.main_stick != (0,0.5):
#             #print("got here")
#             controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, 0.5)
#     elif ai_state.hitlag:
#         #controller.release_all()
#         if controller.current.main_stick != (0,0.5):
#             #print("got here")
#             controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, 0.5)
#             #return
#     else:
#         controller.release_all()