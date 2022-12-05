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

# Returns whether or not an EMS vehicle is present in the simulation
def isEMSPresent(veh_id_list):
    for vehID in veh_id_list:
            if traci.vehicle.getParameterWithKey(vehID, "has.bluelight.device")[1] == 'true':
                return True
    return False

# // --- TRAFFIC LIGHT POLICIES --- //
# EMS POLICY
def ems_policy(type, intersection_id):

    # Green Corridor (Turn EMS lanes for intersection green)
    if type == 'gc':
        traci.trafficlight.setRedYellowGreenState(intersection_id, 'GGGGrrrrGGGGrrrr')
        return
    # Red Freeze (Turn all lights for intersection red)
    elif type == 'rf':
        traci.trafficlight.setRedYellowGreenState(intersection_id, 'rrrrrrrrrrrrrrrr')
        return
    # Normal policy (No traffic light manipulation)
    elif type == 'na':
        # DO NOTHING HERE
        pass
    else:
        raise Exception("You did not enter a valid EMS-policy type. Please re-run with one of the following options:\n\n<gc (green corridor) | rf (red freeze) | na (normal lights)>")
    
# Define traffic light phases
intersection_J3_phases = []
intersection_J3_phases.append(traci.trafficlight.Phase(42, "GGGgrrrrGGGgrrrr", 0, 0))
intersection_J3_phases.append(traci.trafficlight.Phase(3, "yyyyrrrryyyyrrrr", 0, 0))
intersection_J3_phases.append(traci.trafficlight.Phase(42, "rrrrGGGgrrrrGGGg", 0, 0))
intersection_J3_phases.append(traci.trafficlight.Phase(3, "rrrryyyyrrrryyyy", 0, 0))

intersection_J4_phases = []
intersection_J4_phases.append(traci.trafficlight.Phase(36, "GGGgrrrrGGGgrrrr", 0, 0))
intersection_J4_phases.append(traci.trafficlight.Phase(6, "yyyGrrrryyyGrrrr", 0, 0))
intersection_J4_phases.append(traci.trafficlight.Phase(3, "rrryrrrrrrryrrrr", 0, 0))
intersection_J4_phases.append(traci.trafficlight.Phase(36, "rrrrGGGgrrrrGGGg", 0, 0))
intersection_J4_phases.append(traci.trafficlight.Phase(6, "rrrryyyGrrrryyyG", 0, 0))
intersection_J4_phases.append(traci.trafficlight.Phase(3, "rrrrrrryrrrrrrry", 0, 0))

intersection_J5_phases = []
intersection_J5_phases.append(traci.trafficlight.Phase(42, "rrrrGGGgrrrrGGGg", 0, 0))
intersection_J5_phases.append(traci.trafficlight.Phase(3, "rrrryyyyrrrryyyy", 0, 0))
intersection_J5_phases.append(traci.trafficlight.Phase(42, "GGGgrrrrGGGgrrrr", 0, 0))
intersection_J5_phases.append(traci.trafficlight.Phase(3, "yyyyrrrryyyyrrrr", 0, 0))

int_to_phases_map = {   'J3' : intersection_J3_phases,
                        'J4' : intersection_J4_phases,
                        'J5' : intersection_J5_phases   }

# NORMAL POLICY
def return_to_normal(intersection_id):
    logic = traci.trafficlight.Logic("custom", 0, 0, int_to_phases_map[intersection_id])
    traci.trafficlight.setCompleteRedYellowGreenDefinition(intersection_id, logic)
    traci.trafficlight.setPhase(intersection_id, 0)

# BASE TRACI CONTROL LOOP
def run(sumo_gui, FILENAME, policy_type):
    traci.start([sumo_gui, "-c", FILENAME])
    step = 0
    intersection_ids = traci.trafficlight.getIDList()
    hit_1 = False
    hit_2 = False
    hit_3 = False
    hit_4 = False

    already_hit = False

    count_EMS_time_steps = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if(isEMSPresent(traci.vehicle.getIDList())):
            count_EMS_time_steps += 1
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
            # Set intersection 1 to ems policy
            ems_policy(policy_type, intersection_ids[0])
            pass
        elif hit_2 and not hit_3:
            # Return intersection 1 to normal
            # Set intersection 2 to ems policy
            return_to_normal(intersection_ids[0])
            ems_policy(policy_type, intersection_ids[1])
            pass
        elif hit_3 and not hit_4:
            # Return intersection 2 to normal
            # Set intersection 3 to ems policy
            return_to_normal(intersection_ids[1])
            ems_policy(policy_type, intersection_ids[2])
            pass
        elif hit_4 and not already_hit:
            # Return intersection 3 to normal
            return_to_normal(intersection_ids[2])
            already_hit = True
            pass
        step += 1
    traci.close()
    sys.stdout.flush()
    return count_EMS_time_steps, step

def run_all_policies_experiment(sumo_gui, FILENAME):
    print('Running GREEN CORRIDOR policy...')
    gc_ems_steps, gc_total_steps = run(sumo_gui, FILENAME, 'gc')
    print('Running RED FREEZE policy...')
    rf_ems_steps, rf_total_steps = run(sumo_gui, FILENAME, 'rf')
    print('Running NORMAL policy (no traffic light manipulation)...')
    na_ems_steps, na_total_steps = run(sumo_gui, FILENAME, 'na')

    print('\n\n---------------- RESULTS ----------------\n')
    print('GREEN CORRIDOR:\nEMS travel time = {} steps\nCongestion clearing time = {} steps\n'.format(gc_ems_steps, gc_total_steps))
    print('RED FREEZE:\nEMS travel time = {} steps\nCongestion clearing time = {} steps\n'.format(rf_ems_steps, rf_total_steps))
    print('CONTROL (no traffic light manipulation):\nEMS travel time = {} steps\nCongestion clearing time = {} steps\n'.format(na_ems_steps, na_total_steps))
    print('-----------------------------------------\n')
# Main
if __name__ == "__main__":

    options = get_options()
    FILENAME = "simulation.sumocfg"

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

    user_input = input("\nRun auto-experiment? [Y/N]\n\n")
        
    if user_input.lower() == 'y':
        sumo_gui = 'sumo'
        run_all_policies_experiment(sumo_gui, FILENAME)
        pass
    else:
        sumo_gui = input("\nRun sumo-gui? [Y/N]\n\n")
        if sumo_gui.lower() == 'y':
            sumo_gui = 'sumo-gui'
        else:
            sumo_gui = 'sumo'
            policty_type = input("\nPlease type your preffered policy: <gc (green corridor) | rf (red freeze) | na (normal lights)>\n\n")
            EMSTravelTime, TotalCongestionClearingTime = run(sumo_gui, FILENAME, policty_type)
            print('\nEMS travel time = {} steps\nCongestion clearing time = {} steps\n'.format(EMSTravelTime, TotalCongestionClearingTime))
