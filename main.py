# 1 - check log, identify attacker IP, ban, update IP Ban List
# 2 - check IP ban List & time, release IP if longer then 15 days

#!/usr/bin/env python
import func
import subprocess
import time

now = time.time()
cmd = func.check_hits_Command()

#capture ouput from command line & convert to list IP/Hits
#proc = subprocess.check_output(cmd, shell=True)

proc = subprocess.check_output("grep -E '26/Oct/2022:09:[0-9]' /Users/phamtuanminh/Desktop/hoangtv/nginx80.access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -10", shell=True)

output = proc.decode("utf-8")
item = output.split()
list_ip = func.IP_Pair(item)

#check if number of hits > 10000 add to banned list, if duplicate ==> print Duplicated IP
banned_ip = []
for item in list_ip:
    if float(item[0]) > 10000:
        banned_ip.append(item[1])
        func.updateBannedIP(item[1],item[0],now)

print(banned_ip)

