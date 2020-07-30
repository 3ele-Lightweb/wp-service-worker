#custom models
import os,shutil
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
def archiv_files():
    token = os.environ.get('ODOO_TOKEN')
    url = os.environ.get('ODOO_API_URL')
    url ="https://www.3ele.de/api/wp_instance.wp_core/search"
    odoo = oc.odoo_connector()
    wp = wpc.wp_connector()
    wp_instances = odoo.get_odoo_wp_instance(url, token)
    for wp_instance in wp_instances:
            #print (wp_instance)
            backup_path = str(home)+"/archive/"
            target_path = str(home)+"/daily_backups/"+wp_instance['name']+"/"+str(date)
            Path(backup_path).mkdir(parents=True, exist_ok=True)
            
            try:
                command ='zip -ur '+ backup_path + wp_instance['name'] + '.zip ' + target_path
                os.system(command)
                logging.info('weekly backup ' + str(wp_instance['name']) + ' on ' +  str(date) + ' success')
                
            except:
                logging.info('weekly backup ' + str(wp_instance['name']) + ' on ' + str(date) + 'failed')
                pass
                

if __name__ == "__main__":
    
    archiv_files()
