import json
from settings import settings as settings
import csv
from datetime import datetime

def show_port_stats(session, dev_list, field_list):
    # Purpose:  For each device in the dev_list, send REST API call to vManage 
    #           to query interface statistics
    # Input:    session: a session from requests library
    #           dev_list: a list of devices
    #           field_list: a list of fields that you want to show
    # Future:   This function will be made more generic.

    for dev in dev_list:
        devip = dev['devip']
        # Call vManage REST API + device's IP
        response_body = session.get(settings.vmanage_server 
            + '/dataservice/device/interface/stats?deviceId=' 
            + devip, verify=False)
        # If the response is 200 OK, process the data
        if response_body.status_code == 200:
            table_header_raw = json.loads(response_body.text)['header']['columns']
            table_data = json.loads(response_body.text)['data']
            table_header = []
            # Go through the header and choose only the ones in the field list
            for col in table_header_raw:
                if col['property'] in field_list:
                    table_header.append(col['property'])
            print_header(table_header)
            print_data(table_header, table_data)
        else:
            print ("REST CALL ERROR: {}".format(str(response_body.status_code)))

def print_break(table_header):
    # Purpose:  Print line break 
    # Input:    table_header: column header
    print ("+" + "-".rjust(20,"-"), end='')
    for i in range(1, len(table_header)):
        print ("+" + "-".rjust(16, "-"), end='')
    print ('+')

def print_header(table_header):
    # Purpose:  Print a header 
    # Input:    table_header: column header
    print ("|" + str(table_header[0]).ljust(20," "), end='')
    for i in range(1, len(table_header)):
        print ("|" + str(table_header[i]).rjust(16," "), end='')
    print ('|')
    print_break(table_header)


def print_data(table_header, table_data):
    # Purpose:  Print data based on the supplied header
    # Input:    table_header: column header
    #           table_data:   data
    for data in table_data:
        col = []
        for head in table_header:
            if head in data:
                col.append(data[head])
            else:
                col.append("")
        print ("|" + str(col[0]).ljust(20, " "), end='')
        for i in range(1,len(col)):
            print ("|" + str(col[i]).rjust(16, " "), end='')
        print ('|')
    print_break(table_header)

def dump_to_csv(session, dev_list, field_list, filename):
    # Purpose:  Write data to a csv file
    # Input:    session:    a session from requests library
    #           dev_list:   a list of devices
    #           field_list: a list of fields that you want to show
    #           filename:   a csv file
    row_list = []
    current_time = datetime.now(tz=None)
    for dev in dev_list:
        devip = dev['devip']
        # Call vManage REST API + device's IP
        response_body = session.get(settings.vmanage_server 
            + '/dataservice/device/interface/stats?deviceId=' 
            + devip, verify=False)
        # If the response is 200 OK, process the data
        if response_body.status_code == 200:
            table_header_raw = json.loads(response_body.text)['header']['columns']
            table_data = json.loads(response_body.text)['data']
            table_header = []
            # Go through the header and choose only the ones in the field list
            for col in table_header_raw:
                if col['property'] in field_list:
                    table_header.append(col['property'])
            # Add data to row. One row consists of one interface on a device.
            # Then add row to rowlist
            for data in table_data:
                row = []
                row.append(current_time)
                row.append(devip)
                for head in table_header:
                    if head in data:
                        row.append(data[head])
                    else:
                        row.append("")
                row_list.append(row)
        else:
            print ("REST CALL ERROR: {}".format(str(response_body.status_code)))
    # If the row_list is not empty, write to csv file
    if row_list:
        with open(filename, 'a') as fd:
            writer = csv.writer(fd)
            writer.writerows(row_list)

