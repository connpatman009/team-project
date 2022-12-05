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

# // --- TRAFFIC LIGHT POLICIES --- //
# EMS POLICY
def ems_policy(intersection_id):
    pass
# NORMAL POLICY
def normal_policy(intersection_id):
    pass

# BASE TRACI CONTROL LOOP
def run():
    step = 0
    print(traci.trafficlight.getIDList())
    print(traci.multientryexit.getIDList())
    hit_1 = False
    hit_2 = False
    hit_3 = False
    hit_4 = False
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # DO TRACI THINGS HERE
        in_det_1 = traci.multientryexit.getLastStepVehicleNumber('det1')
        in_det_2 = traci.multientryexit.getLastStepVehicleNumber('det2')
        in_det_3 = traci.multientryexit.getLastStepVehicleNumber('det3')
        in_det_4 = traci.multientryexit.getLastStepVehicleNumber('det4')
        if in_det_1:
            hit_1 = True
        if in_det_2:
            hit_2 = True
        if in_det_3:
            hit_3 = True
        if in_det_4:
            hit_4 = True
        
        # At this point, hit_X will be true if EMS has hit detector X, so
        if hit_1 and not hit_2:
            # Set intersection 1 to policy
            pass
        elif hit_2 and not hit_3:
            # Return intersection 1 to normal
            # Set intersection 2 to policy
            pass
        elif hit_3 and not hit_4:
            # Return intersection 2 to normal
            # Set intersection 3 to policy
            pass
        elif hit_4:
            # Return intersection 3 to normal
            pass
            


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
