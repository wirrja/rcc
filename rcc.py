#!/usr/bin/env python
'''RCC router copy config'''
import os
from datetime import datetime
from telnetlib import Telnet
from device_settings import cisco, huawei, juniper

# remove after tests
# from CONFIGCISCO import TEXT

class Device:
    '''It is work like an Expect scripts:
     - connect to a network device over telnet
     - get configuration ("show run", "display cur" etc)
     - compare (md5hash) a config with an old one
     - save a new config.'''

    def __init__(self, location, ip, login, password, group, enpassword=None):
        self.ip = ip.encode('ascii')
        self.login = login.encode('ascii')
        self.password = password.encode('ascii')
        self.group = group.encode('ascii')
        self.location = location
        if enpassword:
            self.enpassword = enpassword.encode('ascii')
        else:
            pass


    def get_config(self):

        try:
            tn = Telnet(self.ip, 23, 1)

            if self.group == 'cisco':
                # tn.set_debuglevel(1)
                tn.read_until(cisco['read_login'])
                tn.write(self.login + b'\n')
                tn.read_until(cisco['read_pass'])
                tn.write(self.password + b'\n')
                tn.read_until(cisco['waitfor'])
                tn.write(cisco['root_cli'])
                tn.read_until(cisco['read_pass'])
                tn.write(self.enpassword + b'\n')
                tn.read_until(b'#')
                tn.write(cisco['nobreaks'])
                tn.write(cisco['show_conf'])
                tn.write(cisco['quit'])
                output_conf = tn.read_all().decode('ascii')

            elif self.group == 'huawei':
                # tn.set_debuglevel(1)
                tn.read_until(huawei['read_login'])
                tn.write(self.login + b'\n')
                tn.read_until(huawei['read_pass'])
                tn.write(self.password + b'\n')
                tn.read_until(huawei['waitfor'])
                tn.write(huawei['nobreaks'])
                tn.read_until(huawei['waitfor'])
                tn.write(huawei['show_conf'])
                output_conf = tn.read_until(huawei['waitfor']).decode('ascii')
                tn.write(huawei['quit'])

            elif self.group == 'juniper':
                # tn.set_debuglevel(1)
                tn.read_until(juniper['read_login'])
                tn.write(self.login + b'\n')
                tn.read_until(juniper['read_pass'])
                tn.write(self.password + b'\n')
                tn.read_until(juniper['waitfor'])
                tn.write(juniper['show_conf'])
                tn.read_until(juniper['waitfor'])
                output_conf = tn.read_until(juniper['waitfor']).decode('ascii')
                tn.write(juniper['quit'])

            return output_conf

        except IOError as detail:
            curr_time = datetime.now().strftime('%b %Y %X %d')
            errdevice = self.group + b' ' + self.ip
            errdevice = errdevice.decode('utf-8')
            result = 'Warning! {0}! {1}. Check error.txt!'\
                        .format(detail, errdevice)
            with open('error.txt', 'a') as file:
                file.write(curr_time + ' '+ errdevice + '\n')
            print(result)

            return None


    def backup(self):
        curr_date = datetime.now().strftime('%d_%m_%y')
        backupdir = './configs/'
        configname = self.location + '_' + curr_date + '.txt'
        try:
            result = self.get_config()
            if result:
                if os.path.exists(backupdir):
                    pass
                else:
                    os.makedirs(backupdir)
                    print('Backup directory not found, creating...')
                try:
                    with open(backupdir + configname, 'w') as file:
                        file.write(result)
                        print(self.location, 'was saved!')
                except IOError as detail:
                    print(detail)
            else:
                pass
        except IOError as detail:
            print(detail)


class Git:
    ''' Version control for configuration files by Git
    git add ., git commit -m "date+location+ip", git push to local
    Kallithea server (https://kallithea-scm.org/).'''

    def add(self):
        pass

    def commit(self):
        pass

    def push(self):
        pass

    def sent_email(self):
        pass
