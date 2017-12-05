#!/bin/python


import ConfigParser
import datetime
import json
import os
from time import sleep
import psutil


def check_settings():
    return os.path.isfile('settings')


def create_settings_file():
    while True:
        log_format = raw_input("Please, select format of output (json|plain): ")
        if log_format == "json" or log_format == "plain":
            break
    while True:
        log_interval = raw_input("Please, select log interval in minutes :")
        if int(log_interval) == 0:
            print "Interval must be greater than 0!"
        elif log_interval.isdigit():
            break
    settings = file('settings', "w")
    settings.writelines("[main]")
    settings.writelines("format = {0}".format(log_format))
    settings.writelines("interval = {0}".format(log_interval))
    settings.close()


def read_settings():
    config = ConfigParser.ConfigParser()
    if check_settings():
        config.read('settings')
        log_format = config.get("main", "format")
        log_interval = config.get("main", "interval")
        return log_format, log_interval
    else:
        print "No settings file. Exiting..."
        exit(0)


def make_human(item):
    return str(int(item) >> 20) + "Mb"


def gen_key_val(dict_item):
    dict_item = list(dict_item)
    return str(dict_item[0])+" - " + str(dict_item[1]) + ";"


def print_out_plain(data_to_out):
    out_string = str(datetime.datetime.now())+":"
    for item in data_to_out.items():
        out_string += gen_key_val(item)
    log = file("out.log", "a")
    log.write(out_string+"\n")
    log.close()


def print_out_json(data_to_out):
    out_json = json.dumps({str(datetime.datetime.now()): [data_to_out]}, sort_keys=False)
    out_file = file("log.json", "a")
    out_file.write(out_json)
    out_file.close()


def write_pid():
    pid = file("/home/student/task3.pid", "w")
    pid.write(str(os.getpid()))
    pid.close()


write_pid()
while True:
    while True:
        if check_settings():
            out_format, out_interval = read_settings()
            break
        else:
            create_file = raw_input("No settings file. Want to create (y|n)? ")
            if create_file == 'y':
                create_settings_file()
            if create_file == 'n':
                exit(0)
    data = {}
    data.update({'CPU': sum(psutil.cpu_percent(1, percpu=True))})
    data.update({'VMEM': make_human(psutil.virtual_memory().used)})
    data.update({'MEM': make_human(psutil.virtual_memory().used + psutil.swap_memory().used)})
    data.update({'IO read': make_human(psutil.disk_io_counters().read_count)})
    data.update({'IO write': make_human(psutil.disk_io_counters().write_count)})
    data.update({'NET sent': make_human(psutil.net_io_counters().bytes_sent)})
    data.update({'NET write': make_human(psutil.net_io_counters().bytes_sent)})
    if out_format == 'plain':
        print_out_plain(data)
    elif out_format == 'json':
        print_out_json(data)
    sleep(int(out_interval) * 60)
