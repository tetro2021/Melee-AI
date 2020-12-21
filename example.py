#!/usr/bin/python3
import argparse
import signal
import sys
import melee
from melee import enums
from slippimoves import *

# This example program demonstrates how to use the Melee API to run a console,
#   setup controllers, and send button presses over to a console
# python example.py --port 1 --opponent 2 --dolphin_executable_path FM-Slippi

def check_port(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 4:
        raise argparse.ArgumentTypeError("%s is an invalid controller port. \
                                         Must be 1, 2, 3, or 4." % value)
    return ivalue

parser = argparse.ArgumentParser(description='Example of libmelee in action')
parser.add_argument('--port', '-p', type=check_port,
                    help='The controller port (1-4) your AI will play on',
                    default=2)
parser.add_argument('--opponent', '-o', type=check_port,
                    help='The controller port (1-4) the opponent will play on',
                    default=1)
parser.add_argument('--debug', '-d', action='store_true',
                    help='Debug mode. Creates a CSV of all game states')
parser.add_argument('--address', '-a', default="127.0.0.1",
                    help='IP address of Slippi/Wii')
parser.add_argument('--dolphin_executable_path', '-e', default=None,
                    help='The directory where dolphin is')
parser.add_argument('--connect_code', '-t', default="",
                    help='Direct connect code to connect to in Slippi Online')
parser.add_argument('--iso', default=None, type=str,
                    help='Path to melee iso.')

args = parser.parse_args()

# This logger object is useful for retroactively debugging issues in your bot
#   You can write things to it each frame, and it will create a CSV file describing the match
log = None
if args.debug:
    log = melee.Logger()

# Create our Console object.
#   This will be one of the primary objects that we will interface with.
#   The Console represents the virtual or hardware system Melee is playing on.
#   Through this object, we can get "GameState" objects per-frame so that your
#       bot can actually "see" what's happening in the game
console = melee.Console(path=args.dolphin_executable_path,
                        slippi_address=args.address,
                        logger=log)

# Create our Controller object
#   The controller is the second primary object your bot will interact with
#   Your controller is your way of sending button presses to the game, whether
#   virtual or physical.
controller = melee.Controller(console=console,
                              port=args.port,
                              type=melee.ControllerType.STANDARD)

controller_opponent = melee.Controller(console=console,
                                       port=args.opponent,
                                       type=melee.ControllerType.GCN_ADAPTER)

# This isn't necessary, but makes it so that Dolphin will get killed when you ^C
def signal_handler(sig, frame):
    console.stop()
    if args.debug:
        log.writelog()
        print("") #because the ^C will be on the terminal
        print("Log file created: " + log.filename)
    print("Shutting down cleanly...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Run the console
console.run(iso_path=args.iso)

# Connect to the console
print("Connecting to console...")
if not console.connect():
    print("ERROR: Failed to connect to the console.")
    sys.exit(-1)
print("Console connected")

# Plug our controller in
#   Due to how named pipes work, this has to come AFTER running dolphin
#   NOTE: If you're loading a movie file, don't connect the controller,
#   dolphin will hang waiting for input and never receive it
print("Connecting controller to console...")
if not controller.connect():
    print("ERROR: Failed to connect the controller.")
    sys.exit(-1)
print("Controller connected")
print("Player Port: " + str(args.opponent))
costume = 0
stagePositiony = 16.1
teching = True
# Main loop
while True:
    # "step" to the next frame
    gamestate = console.step()
    if gamestate is None:
        continue

    # The console object keeps track of how long your bot is taking to process frames
    #   And can warn you if it's taking too long
    if console.processingtime * 1000 > 12:
        print("WARNING: Last frame took " + str(console.processingtime*1000) + "ms to process.")

    # What menu are we in?
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:

        # Slippi Online matches assign you a random port once you're in game that's different
        #   than the one you're physically plugged into. This helper will autodiscover what
        #   port we actually are.
        discovered_port = args.port
        if args.connect_code != "":
            discovered_port = melee.gamestate.port_detector(gamestate, melee.Character.FOX, costume)
        if discovered_port > 0:
            # NOTE: This is where your AI does all of its stuff!
            # This line will get hit once per frame, so here is where you read
            #   in the gamestate and decide what buttons to push on the controller
            # melee.techskill.multishine(ai_state=gamestate.player[discovered_port], controller=controller)

            #Setup for player & AI
            ai_state=gamestate.player[discovered_port]
            player_state = gamestate.player[2]
            

            #Tracker for important variables
            # if stagePositiony != ai_state.y:
            #     #stageChanged = True
            #     print("Stage pos changed" + str(ai_state.y))
            #     stagePosition = ai_state.y
            
            #if not ai_state.on_ground:
                #wasOffGround = True
            # if ai_state.action == enums.Action.THROWN_FORWARD:
            #     if ai_state.action_frame == 1:
            #         print("here")
            #         controller.release_all()
            #     else:
            #         print("Can you tech it?   " + str(canTech))
            #         controller.press_button(enums.Button.BUTTON_L)

            
            #simpleFoxAI(ai_state, controller, player_state)
            
            # if ai_state.action == enums.Action.GRABBED:
            #     print("Got grabbed")

            # if ai_state.action == enums.Action.THROWN_UP:
            #     print("Got grabbed")

            # if ai_state.action == enums.Action.THROWN_BACK:
            #     print("Got grabbed")
            
            teching = SimpleTech(ai_state, controller)
            if not teching:
                simpleFoxAI(ai_state, controller, player_state)
              
                
                






        else:
            # If the discovered port was unsure, reroll our costume for next time
            costume = random.randint(0, 4)
    else:
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            melee.Character.FOX,
                                            melee.Stage.FINAL_DESTINATION,
                                            args.connect_code,
                                            costume=costume,
                                            autostart=True,
                                            swag=False)
    if log:
        log.logframe(gamestate)
        log.writeframe()
