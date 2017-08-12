#!/usr/bin/env python
'''Startup script'''
import os
import re
from rcc import Device


DB_FILE = 'router_db.txt'


def parse():
    '''Parse router_db.txt, file containing information from
    Zabbix(www.zabbix.com) database'''
    if os.path.exists(DB_FILE) is True:
        print('Database file found, start backup\n')
        input_vars = []
        with open(DB_FILE, 'r') as file:
            for string in file:
                stripped = string.rstrip()
                r = re.split('[_ ]', stripped)
                input_vars.append(r)
    else:
        print('Warning: file %s not found!' % DB_FILE)

    for li in input_vars:
        k = re.split('[-]', li[2])
        if len(li) < 6:
            li.append(None)
        yield li[0], li[1], li[3], li[4], k[1], li[5]

def main():
    '''Main function, starting all processes'''
    for location, ip, login, password, group, enpassword in parse():
        Device(location=location, ip=ip, login=login, password=password, group=group,\
               enpassword=enpassword).backup()



if __name__ == '__main__':
    main()
