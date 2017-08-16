#!/usr/bin/env python
"""RCC router copy config"""
import os
import hashlib
from datetime import datetime
from telnetlib import Telnet
from device_settings import cisco, huawei, juniper
# remove after tests
#from CONFIGCISCO import TEXT

class Device:
    """It is work like an Expect scripts:
     - connect to a network device over telnet
     - get configuration ("show run", "display cur" etc)
     - compare (md5hash) a config with an old one
     - save a new config."""

    def __init__(self, location, ip, login, password, group, enpassword=None):
        self.ip = ip.encode()
        self.login = login.encode()
        self.password = password.encode()
        self.group = group
        self.location = location
        if enpassword:
            self.enpassword = enpassword.encode()
        else:
            pass


    def get_config(self):
        """Connect to network device with incoming parameters
        (from router_db.txt)."""
        try:
            tn = Telnet(self.ip, 23, 5)
            # output_conf = '0'
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
                output_conf = tn.read_all()

            elif self.group == 'huawei':
                # tn.set_debuglevel(1)
                tn.read_until(huawei['read_login'])
                tn.write(self.login + b'\n')
                tn.read_until(huawei['read_pass'])
                tn.write(self.password + b'\n')
                tn.read_until((self.location + '>').encode())
                tn.write(huawei['nobreaks'])
                tn.read_until((self.location + '>').encode())
                tn.write(huawei['show_conf'])
                output_conf = tn.read_until((self.location + '>').encode())
                tn.write(huawei['quit'])

            elif self.group == 'juniper':
                # tn.set_debuglevel(1)
                tn.read_until(juniper['read_login'])
                tn.write(self.login + b'\n')
                tn.read_until(juniper['read_pass'])
                tn.write(self.password + b'\n')
                tn.read_until(juniper['waitfor'])
                tn.write(juniper['show_conf'])
                # tn.read_until(juniper['waitfor'])
                tn.write(juniper['quit'])
                output_conf = tn.read_until(juniper['waitfor'])

            return output_conf
            
        except IOError as detail:
            curr_time = datetime.now().strftime('%b %Y %X %d')
            errdevice = self.group.encode() + b' ' + self.ip
            errdevice = errdevice.decode('utf-8')
            result = 'Warning! {0}! {1}. Check error.txt!'\
                        .format(detail, errdevice)
            with open('error.txt', 'a') as file:
                file.write(curr_time + ' ' + errdevice + '\n')
            print(result)
           
    def backup(self):
        """Save config, if new"""
        ip = self.ip.decode('utf-8')
        backupdir = 'C:\\Users\\admin\\PycharmProjects\\github\\rcc\\configs\\'
        configname = self.location + '_' + ip + '.txt'
        try:
            new_config = self.get_config()
            if new_config:
                if os.path.exists(backupdir):
                    pass
                else:
                    os.makedirs(backupdir)
                    print('Backup directory not found, creating...')
                # if file exist, get md5_hash of live and current config
                if os.path.exists(backupdir + configname):
                    with open(backupdir + configname, 'rb') as b:
                        file_content = (b.read()).decode()
                        result = self.compare(new_config, file_content)
                        if result is False:
                            with open(backupdir + configname, 'w') as f:
                                f.write(new_config.decode())
                                print(self.location, ip, 'has updates! saved.')
                                Git().add(configname)  # git add .
                        else:
                            print(self.location, ip, 'not changed')
                # if file not exist, write data in new file
                else: 
                    with open(backupdir + configname, 'w') as file:
                        file.write(new_config.decode())
                        print(self.location, ip, 'has updates! saved.')
                        Git().add(configname)
            else:
                pass
        except IOError as detail:
            print(detail)

    def compare(self, result, file_content):
        """Compare active config (type bytes)
        with old config, stored on hdd.
        replace'\r' (that appear in Windows)."""

        result_str = result.decode()
        new_config = (result_str.replace('\r', '')).encode()
        old_config = (file_content.replace('\r', '')).encode()
        nc = hashlib.md5(new_config)
        oc = hashlib.md5(old_config)
        print(nc.hexdigest(), oc.hexdigest())

        return nc.hexdigest() == oc.hexdigest()


class Git:
    """ Version control for configuration files by Git
    git add ., git commit -m "date+location+ip", git push to local
    Kallithea server (https://kallithea-scm.org/)."""
    
    def add(self, filename):
        # git add -a filename -m " "
        print(filename, 'commited.')

    def push(self):
        pass

    def sent_email(self):
        print('ok')
