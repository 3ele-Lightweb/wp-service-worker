#custom models
import os
import  odoo_connector as oc
import  wp_connector as wpc
import subprocess
from datetime import date
from pathlib import Path
import pathlib

from pathlib import Path
home = str(Path.home())
import logging

#logging.basicConfig(filename='daily_backups.log',level=logging.INFO)
current_dir = pathlib.Path(__file__).parent
current_file = pathlib.Path(__file__)
today = date.today()
date = today.strftime("%Y-%m-%d")
class WpServiceWorker:
    def __init__(self):
        self.token = os.environ.get('ODOO_TOKEN')
        self.host = "https://www.3ele.de/api"

    def install_plugin(self):
        #init connector
        odoo = oc.odoo_connector(self.token, self.host)
        #set model
        model ="wp_instance.plugins"
        #set mod
        mod = "search"
        #set domain
        domain = '[("name","=","wp-timetorest")]'
        #set fields, we need from the plugin
        fields='["name","download_url","wp_instance"]'
        #call odoo API
        plugin = odoo.get_record(domain=domain,fields=fields,mod=mod,model=model)
        plugin = plugin[0]
        
        #init wp-connector
        wp = wpc.wp_connector()
        for wp_instance_id in plugin['wp_instance']:
            model ="wp_instance.wp_core"
            mod = "search"
            fields='["name","url","wp_path","sql_path","host","user","ssh_port"]'
            domain = '[("id","=","'+str(wp_instance_id)+'")]'
            wp_instance = odoo.get_record(domain=domain,fields=fields,mod=mod,model=model)
            wp_instance = wp_instance[0]
            print (wp_instance)
#           command = 'wp plugin install '+ plugin['download_url']+' path="'+wp_instance['wp_path']+'" --activate '
            hostname = wp_instance['host']
            username = wp_instance['user']
            path = wp_instance['wp_path']
            command = "ssh -t  "+ wp_instance['user']+"@"+ wp_instance['host'] + " \"bash -ic 'wp --info;'\""
           # print (command)
            result = subprocess.check_output(command, shell=True)
            print (result)
        #    wp.execute_wp_cli(hostname, username, command)



if __name__ == "__main__":
    worker = WpServiceWorker()
    worker.install_plugin()
