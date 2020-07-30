#custom models
import os
import  odoo_connector as oc
import  wp_connector as wpc

from datetime import date
from pathlib import Path
import pathlib

from pathlib import Path
home = str(Path.home())
import logging

logging.basicConfig(filename='daily_backups.log',level=logging.INFO)
current_dir = pathlib.Path(__file__).parent
current_file = pathlib.Path(__file__)
today = date.today()
date = today.strftime("%Y-%m-%d")
def download_files():
    token = os.environ.get('ODOO_TOKEN')
    url ="https://www.3ele.de/api/wp_instance.wp_core/search"
    odoo = oc.odoo_connector()
    wp = wpc.wp_connector()
    wp_instances = odoo.get_odoo_wp_instance(url, token)
    for wp_instance in wp_instances:
            
            backup_path = str(home)+"/daily_backups/"+wp_instance['name']+"/"+str(date)
            Path(backup_path).mkdir(parents=True, exist_ok=True)
            Path(backup_path+'/sql/').mkdir(parents=True, exist_ok=True)
            try:
                command ='ssh '+ wp_instance['user']  +'@'+ wp_instance['host'] +' www/wp-cli/wp-cli.phar db export --path='+wp_instance['wp_path']+' '+ wp_instance['sql_path']+'/export-'+str(date)+'.sql'
                os.system(command)
                command ='rsync -az -az --stats '+ wp_instance['user']  +'@'+ wp_instance['host'] +':' + wp_instance['sql_path']+'/export-'+str(date)+'.sql '+backup_path+'/sql/export-'+str(date)+'.sql'
                os.system(command)           
                command ='rsync -az --stats  '+ wp_instance['user']  +'@'+ wp_instance['host'] + ':'+wp_instance['wp_path']+ ' '+backup_path
                os.system(command)
                logging.info('daily backup ' + str(wp_instance['name']) + ' on ' +  str(date) + ' success')
                
            except:
                logging.info('daily backup ' + str(wp_instance['name']) + ' on ' + str(date) + 'failed')
                pass
                

if __name__ == "__main__":
    
    download_files()
