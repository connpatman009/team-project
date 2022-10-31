#! /usr/bin/env python
from fileinput import close
import os

def wsumo(network_name, end_time_in_steps=3600):
    """convert net_edit output file to files we need for sumo"""

    # Ensure args are strings
    network_name = str(network_name)
    network_file_name = "\"" + network_name + ".net.xml\""
    end_time_in_steps = str(end_time_in_steps).strip()

    # Create output_name
    first_output_name = "\"" + network_name + "_trips.trips.xml\""

    # Create rou name
    routes_output = "\"" + network_name + "_routes.rou.xml\""

    # Write command strings
    first_command = "randomtrips.py -n " + network_file_name + " -e \"" + end_time_in_steps + "\" -o " + first_output_name

    second_command = "duarouter -n " + network_file_name + " --route-files " + first_output_name + " -o " + routes_output + " --no-warnings --ignore-errors"

    # Initialize Strings for sumo.cfg file
    first_line = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    open_configuration = "<configuration xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://sumo.dlr.de/xsd/duarouterConfiguration.xsd\">"

    input = "\t<input>\n\t\t<net-file value=" + network_file_name + "/>\n\t\t<route-files value = " + routes_output + "/>\n\t</input>"

    time = "\t<time>\n\t\t<begin value=\"0\"/>\n\t\t<end value=\"" + end_time_in_steps + "\"/>\n\t</time>" 

    close_configuration = "</configuration>"

    sumo_cfg = first_line + "\n\n" + open_configuration + "\n\n" + input + "\n\n" + time + "\n\n" + close_configuration

    return first_command, second_command, sumo_cfg

def runProg():

    cwd = os.getcwd()

    print("\nGot cwd as: " + cwd + "\n")

    input('If directory is wrong, exit now... else press ENTER to continue...\n')

    file_name = input('Input file name...\n')

    file_name = str(file_name)

    # Generate commands and sumo_cfg contents
    FIRST_COMMAND, SECOND_COMMAND, SUMO_CFG = wsumo(file_name, 3500)

    print("1ST COMMAND IS: " + FIRST_COMMAND + "\n")
    print("2ND COMMAND IS: " + SECOND_COMMAND + "\n")

    print("Executing commands...\n")

    os.system(FIRST_COMMAND)
    os.system(SECOND_COMMAND)

    print("EXECUTED COMMANDS TO GENERATE SUMO WORK FILES... WRITING CFG NOW...\n")

    # Create sumo cfg file
    cfg_file = open(cwd + "/" + file_name + "_sim.sumo.cfg", "w")
    cfg_file.write(SUMO_CFG)
    cfg_file.close()

    print("---------WROTE SUMO CFG FILE...---------\n")

    input('press ENTER to exit')

    pass

if __name__ == '__main__':
    runProg()
    pass