py_bkp_rest
===========

Backup and Restore engine in python

The Backup and Restore has 3 parts to note

1. Config files:- Create one backup directory, where you will have all backup policy each policy contains following fields
[schedule1]             
src = /home/anil/src
dest = /home/anil/dst
schedule = 10
start_run = 201307280900
prev_run = 201311221711
next_run = 201311241711

The 1st field is the name of the schedule in []
src is the source directory to be backed up
dest is the destination directory where the backup file will be put under "dest/<schedule1>/<date>.tar.gz" format
schedule tells after how many hours this backup to run.
start_run is YYYYMMDDHHmm when this policy was created
prev_run is YYYYMMDDHHmm is when this policy was ran last time
next_run is YYYYMMDDHHmm is when thie policy will be run next.

After every run the script makes prev_run = next_run and next_run = next_run + schedule(hours)

Just create a file with .conf extension with the above field and you are good to go

2. Backup engine:- Its a python script which reads through the .conf and runs the backup to destination creating a .gz

3. Restore engine :- This restores the backed up data, its args are
             -i = <src folder, where .gz is >
             -o = <o/p folder where restore needs to run
             -s = <start date YYYYMMDDhhmm> of the of the backed up data
             -e = <end data YYYYMMDDhhmm> is the end date of the the backed up data which you want to restore.

