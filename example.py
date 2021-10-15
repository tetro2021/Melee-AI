#!/usr/bin/python3
import argparse
import signal
import sys
import melee
import socket
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
    print("Number of techs: ")
    print(numtecs)
    print("number of Success: ")
    print(numsuccess)
    print("number of failures: ")
    print( (numtecs[0] - numsuccess[0]),  " ", (numtecs[1] - numsuccess[1]), " ", (numtecs[2] - numsuccess[2]))
    print("Final Tech Calculation:")
    finalTech = SuccessOverTotalCalc(numtecs,numsuccess)
    #This varible is created for saving to file for access on separate attemps
    #It could be possible on a server to keep record of percantage successs of different players
    print(finalTech)
    print("Chance of moving left: ", finalTech[0], "of moving right: ", finalTech[1], "Chance of a normal tech", finalTech[2])
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

# Added info to pass back to php
numtecs = [0.0,0.0,0.0] #Left, Right, Normal respectively
numsuccess = [0.0,0.0,0.0]
inTech = False
teching = True
shouldSpotdoge = 3
currentPercent = -1
rec = RecordStates(numtecs, numsuccess, inTech, teching, shouldSpotdoge, currentPercent)

# Socket to PHP file

# s = socket.socket()
# host = "127.0.0.1"
# port = 12345
# s.bind((host, port))

# s.listen(5)


# Main loop
while True:

    # Connect to PHP file
    # c, addr = s.accept()
    # data = c.recv(1024)
    # if data:
    #     c.close
    #     sys.exit()

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
            rec.recordTechShine(ai_state,controller,player_state)
            
              
                
                






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
