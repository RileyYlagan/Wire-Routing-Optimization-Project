#!/usr/bin/python

import sys, getopt
from modules import discretization as dz
from modules import algorithm as alg
import numpy as np
import pyvista as pv
from stl import mesh, main
import time
import random
import csv
import logging
import os

def main(argv):
    # set up logging to file - see previous section for more details


    startTime = time.time()
    meshInput = ''
    wireInput = ''
    outputName = ''
    scaleFactor = 2 # Default 2
    try:
        opts, args = getopt.getopt(argv,"hi:o:m:w:s:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('main.py -m <meshInput> -w <wireInput> -o <outputName>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -m <meshInput> -s <scaleFactor> -w <wireInput> -o <outputName>')
            sys.exit()
        elif opt in ("-m"):
            meshInput = arg
        elif opt in ("-w"):
            wireInput = arg
        elif opt in ("-s"):
            scaleFactor = float(arg)
        elif opt in ("-o", "--ofile"):
            outputName = arg
    os.mkdir("output/"+outputName)
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename="output/"+outputName+"/"+outputName+"_log.log",
                    filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)

    # Now, we can log to the root logger, or any other logger. First the root...

    full_mesh_input = 'input/'+ meshInput
    full_wire_input = 'input/'+ wireInput
    file = open(full_wire_input)
    csvreader = csv.reader(file)
    header = next(csvreader)
    #print(header)
    wire_dict = {}
    rows = []
    for row in csvreader:
        wire_dict[row[0]] = {"start":list(eval(row[1])),"goal": list(eval(row[2])),"max_curvature": eval(row[3]), "separations": dict(eval(row[4]))}
    file.close()
    
    node_dict = dz.main(full_mesh_input,scaleFactor)
    alg.main(wire_dict,node_dict,outputName)



    executionTime = (time.time() - startTime)
    logging.info('Total Execution time in seconds: ' + str(executionTime))

if __name__ == "__main__":
    main(sys.argv[1:])