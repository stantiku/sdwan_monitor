import requests
import json
import urllib3
from settings import settings as settings
from sdwan_operations import monitor as sdwanmn
import time
import sys, getopt

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main(argv):
    # To run the program use the syntax:
    # python __main__.py -d <devfile> -f <fieldfile> -c <optional csvfile>
    devfile = ''
    fieldfile = ''
    csvfile = ''
    try:
        opts, args = getopt.getopt(argv,"hd:f:c:",["devfile=", "fieldfile=", "csvfile"])
    except getopt.GetoptError:
        print ('python __main__.py -d <devfile> -f <fieldfile> -c <optional csvfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python __main__.py -d <devfile> -f <fieldfile> -c <optional csvfile>')
            sys.exit(1)
        elif opt in ("-d", "--devfile"):
            devfile = arg
        elif opt in ("-f", "--fieldfile"):
            fieldfile = arg
        elif opt in ("-c", "--csvfile"):
            csvfile = arg

    # Read the device list from the supplied file (for example, dev_list.json)
    try:
        with open(devfile) as f:
            dev_list = json.load(f)
    except FileNotFoundError:
        print ('python __main__.py -d <devfile> -f <fieldfile> -c <optional csvfile>')
        sys.exit(2)
    
    # Read the field list from the supplied file (for example, field_list.json)
    try:
        with open(fieldfile) as f:
            field_list = json.load(f)
    except FileNotFoundError:
        print ('python __main__.py -d <devfile> -f <fieldfile> -c <optional csvfile>')
        sys.exit(2)
    while (True):
        # Create a session and pass it as a parameter for show_port_stats
        session = requests.Session()
        session.auth = (settings.vmanage_username, settings.vmanage_password)
        sdwanmn.show_port_stats(session, dev_list, field_list)
        # Comment below to stop exporting data to csv
        if csvfile != "":
            sdwanmn.dump_to_csv(session,dev_list,field_list,csvfile)
        time.sleep(60)


if __name__ == "__main__":
    main(sys.argv[1:])
