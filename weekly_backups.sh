#! /bin/bash -l
#source $HOME/.bash_profile
#source /var/services/homes/wp_backups/wp_backups/venv/bin/activate
#-avzP --delete /media/hdd1/data-1/ /media/hdd2/data-2/ython3 /var/services/homes/wp_backups/wp_backups/weekly_backups.py
DATE=$(date +"%Y-%m-%d")
echo "Backup dir for today: /nas04/backups/${backup_dir}"
BACKUP_DIR=$HOME'/weekly_backups'
SOURCE_DIR=$HOME'/daily_backups/'

function copy_files {
rsync -azq  $1 $2
echo  $1 $2 
SOURCE=$1
#echo $SOURCE
#echo $PWD
#rsync -av $SOURCE $2
#echo "${SOURCE##*/}"
}
ls
for D in $SOURCE_DIR*; do
    if [ -d "${D}" ]; then

	        #copy_files "${D}/" $BACKUP_DIR   # your processing here
			cd "${D}"	
			FOLDERNAME="${PWD##*/}"
			BACKUPFOLDER=$BACKUP_DIR"/"$FOLDERNAME"/"
			#echo $FOLDERNAME
			CURRENT_BACKUP=$D"/"$DATE"/"
			copy_files $CURRENT_BACKUP $BACKUPFOLDER   # your processing here
	fi
done
