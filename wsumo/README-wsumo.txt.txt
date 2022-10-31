---------- THIS IS THE README FOR WSUMO ----------

WSUMO is a Python program to assist with generating
the necessary work files for SUMO from a network file
generated with netedit (or other programs).

HOW TO SETUP WSUMO:

1. Put the python file (wsumo.py) somewhere on your local machine
2. Add the directory to wsumo.py to your env variables
    - On windows:
        + Search "environment variables" with windows search
        + Open env vars page
        + Select "Environment Variables"
        + Select "Path" and then "Edit" option
        + Click "New" to add a new Path
        + Enter path to directory containing wsumo.py
        + Apply changes and close window
        + wsumo.py should now run in any directory on your pc

HOW TO USE WSUMO:

1. In a terminal, navigate to the directory containing the .net.xml file you want to use
2. Type "wsumo.py" and hit ENTER
3. Follow the instructions in the prompt
    - When it asks for you to "Input file name...", put whatever comes before ".net.xml"
        + E.g. if your file is foobar_network.net.xml, enter "foobar_network"