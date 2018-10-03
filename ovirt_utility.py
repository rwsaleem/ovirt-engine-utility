import sys
import subprocess
"""
Usage: This script is to take a ovirt-engine backup to remote drive using the ovirt-engine and rsync utility and also if the engine gets crashed 
it will restore the engine from the backup which we have taken on remote drive.
"""
def backup():
    try:
        source = input("Enter the file name where you want to store the engine-backup = ")
        destination = input("Enter the remote IP Address (e.g.root@<drive_ip_addr>:/<folder-name>) where you want to store the backup = ")
        #engine-backup to local system.
        backup = 'sudo engine-backup --mode=backup --file=' + source + ' --log=' + source +  '.log'
        subprocess.run(backup, shell=True)
        print("Backup is completed, now we are proceeding with transeferring the backups to remote hard drive")
        # Local system to network location
        copy = 'rsync -avP ' + source  +' ' + source + '.log ' +  destination
        copy_status = subprocess.run(copy, shell=True)
        # This will delete the backup and log file from the local system if the backup accomplish successfully
        # else it will keep the file.
        if copy_status.returncode == 0:
            subprocess.run('rm -rf ' + source + ' ' + source + '.log ', shell=True) 
            print("Files are successfully removed from folder")
        else:
            print("We haven't removed the file as the transfer not acomplished successfully")
    except OSError as err:
        print(err)
        sys.exit(1)

def restore():
    try: 
        source = input("Enter the remote IP Address (e.g.root@<drive_ip_addr>:/<folder-name>/<file_name>) where you have store the backup = ")
        file_name = source.split("/")[-1]
        # Copy the backup file from the remote location to the local system where ovirt-engine utility is installed.
        # If it is not installed, below script will not work.
        subprocess.run('rsync -avP ' + source + ' /tmp/', shell=True)
        # Restore the backup from local system.
        restore_status = subprocess.run('sudo engine-backup --mode=restore '  +  ' --file=/tmp/' + file_name +  ' --log=' + file_name + '.log', shell=True)
        if restore_status.returncode == 0:
            print("Restore operation performed successfully")
        else:
            print("Oops!, unsccessful") 
        # This will remove the file from local system once the backup is completed or terminated so that 
        # user can re initiate the process.
        subprocess.run('rm -rf ' +  '/tmp/' + file_name, shell=True)
    except OSError as err:
        print(err)
        sys.exit(1)

while True:
    print("Enter the no. of task you want to perform")
    print("1. Engine Backup")
    print("2. Engine Resore")
    task = input()
    if task == "1":
        backup()
        break
    elif task == "2":
        restore()
        break




