#!python
import ConfigParser
import ast
import os
from datetime import *
from array import *
config_path = "/home/anil/progs/pyprogs/finalcode"
arr = []
TRUE = 1
FALSE = 0
defaultbackup = FALSE

#####################################################
# given a path return the policy number
#####################################################
def getpolicynos(ppath):
        for policy in readparser.sections():
                for data in readparser.options(policy):
                        path = readparser.get(policy,data)
                        if path == ppath:
                                return policy
########################################################

#########################################################################
# Finding the next_run to backup and return policy
##########################################################################
def findschedule():
        for policy in readparser.sections():
                for data in readparser.options(policy):
                        if data == 'next_run':
                                val = readparser.get(policy,data)
                                nxtrun = datetime.strptime(val, "%Y%m%d%H%M")
                                if datetime.now() > nxtrun :
                                        return TRUE
##########################################################################

#########################################################################
# Add hours to the date and return the nxt date 
########################################################################
def addhours(date, hours):
        add_hrs = '"+' + str(hours) + ' hour"'
        cmd = '/bin/date  -d ' + str(add_hrs) + ' +"%Y%m%d%H%m"'
        return os.popen(cmd).read()

#########################################################################

##########################################################################
# Given a i/p as policy which will be started for backup
#########################################################################
def runbackup(files):
        for policy in readparser.sections():
                for data in readparser.options(policy):
                        val = readparser.get(policy,data)
                        if data == 'src':
                                src = val
                        if data == 'dest':
                                dst = val
                        if data == 'schedule':
                                sched = val
                        if data == 'start_run':
                                start_run = val
                        if data == 'prev_run':
                                prev_run = datetime.strptime(val, "%Y%m%d%H%M")
                        if data == 'next_run':
                                nxt_run = val
                                next_run = datetime.strptime(val, "%Y%m%d%H%M")
                                nxtrun_update = addhours(next_run, sched)
                                print next_run
#find . -newermt '2013-07-05 16:00' -exec tar -cvf /bkp/backup.tar {} \;
#find . -type f -newermt '2013-07-05 16:00' -exec tar -rvf /bkp/backup.tar {} \; 
        #       dest = dst + '/' + policy + '/' + str(nxt_run) + '_backup.tar'
                dest = dst + '/' + policy
                if not os.path.exists(dest):
                        os.makedirs(dest)
                dest = dest + '/' + str(nxt_run) + '_backup.tar'
                if defaultbackup == TRUE:
                        cmd = 'tar -cvf ' + dest  + ' -T '+ config_path + '/defaultlist.txt'

                else:
                        prev_run = "'" + str(prev_run) + "'"
                        cmd = 'find ' + src + ' -newermt ' + prev_run + ' -exec tar -cvf ' + dest + ' {} \;'


                print cmd
                os.system(cmd)
                cmd = 'gzip  ' + dest
                print cmd
                os.system(cmd)
                writeconfig = ConfigParser.RawConfigParser()
                writeconfig.add_section(policy)
                writeconfig.set(policy,'SRC',src )
                writeconfig.set(policy, 'DEST' ,dst )
                writeconfig.set(policy, 'SCHEDULE', sched)
                writeconfig.set(policy, 'START_RUN',start_run)
                writeconfig.set(policy, 'PREV_RUN',nxt_run)
                writeconfig.set(policy, 'NEXT_RUN',nxtrun_update)
                with open(files , 'w') as configfile:
                        writeconfig.write(configfile)
                return

##############################################################################

##############################################################################
# The main function find all the schedule and start the backup to run
##############################################################################

os.chdir(config_path)
for files in os.listdir("."):
    if files.endswith(".conf"):
        readparser = ConfigParser.RawConfigParser()
        readparser.read([files])
        if (findschedule() == TRUE):
                if files == "default.conf":
                        defaultbackup = TRUE
                runbackup(files)
##############################################################################
                                         
