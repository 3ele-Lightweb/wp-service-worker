#! /bin/bash -l
source $HOME/.bash_profile
source /var/services/homes/wp_backups/wp-service-worker/venv/bin/activate
python3 /var/services/homes/wp_backups/wp-service-worker/wp-service-worker.py
