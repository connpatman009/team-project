import csv
import os
import sys
import optparse
from random import randint
from sumolib import checkBinary
import traci

# VERIFY THAT SUMO IS INSTALLED AND PATH IS SET UP
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
else:
    sys.exit("ERROR: Please declare SUMO_HOME in your environment variables.")

# GET OPTIONS
def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of SUMO")
    options, args = opt_parser.parse_args()
    return options

# RETURNS TRUE IF THERE IS AN ACTIVE BLUE LIGHT DEVICE IN VEH_ID_LIST
def isEMSPresent(veh_id_list):
    for vehID in veh_id_list:
            if traci.vehicle.getParameterWithKey(vehID, "has.bluelight.device")[1] == 'true':
                return True
    return False

# BASE TRACI CONTROL LOOP
def run():
    step = 0
    print(traci.trafficlight.getIDList())
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # DO TRACI THINGS HERE

        # These det booleans will be true if the detector was just tripped last step
        det1_0 = traci.inductionloop.getTimeSinceDetection('det1_0') == 0
        det1_1 = traci.inductionloop.getTimeSinceDetection('det1_1') == 0
        det2_0 = traci.inductionloop.getTimeSinceDetection('det2_0') == 0
        det2_1 = traci.inductionloop.getTimeSinceDetection('det2_1') == 0
        det3_0 = traci.inductionloop.getTimeSinceDetection('det3_0') == 0
        det3_1 = traci.inductionloop.getTimeSinceDetection('det3_1') == 0
        det4_0 = traci.inductionloop.getTimeSinceDetection('det4_0') == 0
        det4_1 = traci.inductionloop.getTimeSinceDetection('det4_1') == 0

        # If the detector was tripped last step, print its ID
        if det1_0:
            print("det1_0")
        if det1_1:
            print("det1_1")
        if det2_0:
            print("det2_0")
        if det2_1:
            print("det2_1")
        if det3_0:
            print("det3_0")
        if det3_1:
            print("det3_1")
        if det4_0:
            print("det4_0")
        if det4_1:
            print("det4_1")

        step += 1
    traci.close()
    sys.stdout.flush()
    pass

# Main
if __name__ == "__main__":
    options = get_options()
    FILENAME = "simulation_EMS.sumocfg"

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else: sumoBinary = checkBinary('sumo-gui')

    cmd =   [   sumoBinary,
                "-c",
                FILENAME,
                "--tripinfo-output",
                "tripinfo.xml"
            ]

    traci.start(["sumo-gui", "-c", FILENAME])
    run()
