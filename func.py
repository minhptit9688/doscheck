import re
import time
import os
import configparser
from itertools import zip_longest

def getHomeDir():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['ENV']['DIR']

def getBannedIPFile():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['ENV']['IP_BAN']

def getFileName():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['ENV']['FILE_NAME']

def getThreshold():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['ENV']['THRESHOLD']

#combine 2 elements in a loop
def IP_Pair(iter):
    a = zip_longest(iter[::2],iter[1::2])
    return a

def getSection(file,begin,end):
    data = []
    with open(file) as f:
        for line in f:
            if line.startswith(begin):
                for line in f:
                    data.append(line)
                    if line.startswith(end):
                        break
    return data

def getIpList():
    data = []
    banned_IP_list = getBannedIPFile()
    dir = getHomeDir()
    file = dir+banned_IP_list
    with open(file) as f:
        for line in f:
            if re.findall(r"\b(\w+[.]\w+[.]\w+[.]\w+)", line):
                data.append(line.split())
    return data

def check_hits_Command():
    dir = getHomeDir()+getFileName()
    now = time.localtime()
    checked = int(time.time()) - 300
    result = time.localtime(checked)

    if now.tm_hour > result.tm_hour:
        cmd = "grep -E '{}/{}/{}:{}:[0-9]' {} | awk '{}' | sort | uniq -c | sort -nr | head -10".format(now.tm_mday,now.tm_mon,now.tm_year,now.tm_hour,dir,'print $1')
        return cmd
    else:
        cmd = "grep -E '{}/{}/{}:{}:[0-9]' {} | awk '{}' | sort | uniq -c | sort -nr | head -10".format(result.tm_mday,result.tm_mon,result.tm_year,result.tm_hour,dir,"print $1")
        return cmd

def checkDuplicatedEntry(ip):
    ip_list = getIpList()
    l = []
    for item in ip_list:
        l.append(item[0])
    if ip in l:
        return True
    else:
        return False

def updateBannedIP(ip,hits,time):
    banned_IP_list = getBannedIPFile()
    dir = getHomeDir()
    file = dir+banned_IP_list

    if checkDuplicatedEntry(ip):
        print("duplicated IP")
    else:
        with open(file,'a') as f:
            f.write('\t{}\t\t{}\t\t\t{}\n'.format(ip,hits,time))
            f.close()

def banIP(ip):
    os.system("csf -d "+ip)

def releaseIP(ip):
#execute release IP from banned list on Linux
    return True
