
import sys
import subprocess

"""
Usage: This script is to take a ovirt-engine backup to remote drive using the ovirt-engine and rsync utility and also if the engine gets crashed 
it will restore the engine from the backup which we have taken on remote drive.
"""




def backup():
    try:
        source = input("Enter the file name where you want to sore the engine-backup = ")
        destination = input("Enter the remote IP Address (e.g.root@<drive_ip_addr>:/<folder-name>) where you want to store the backup = ")

        #engine-backup to computer

        backup = 'sudo engine-backup --mode=backup --file=' + source + ' --log=' + source +  '.log'
        subprocess.run(backup, shell=True)
        print("Backup is completed, now we are proceeding with transeferring the backups to remote hard drive")

        # computer to network drive

        copy = 'rsync -avP ' + source  +' ' + source + '.log ' +  destination

        copy_status = subprocess.run(copy, shell=True)

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
        subprocess.run('rsync -avP ' + source + ' /tmp/', shell=True)
        restore_status = subprocess.run('sudo engine-backup --mode=restore '  +  ' --file=/tmp/' + file_name +  ' --log=' + file_name + '.log', shell=True)
        if restore_status.returncode == 0:
            print("Restore operation performed successfully")
        else:
            print("Oops!, unsccessful") 
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




