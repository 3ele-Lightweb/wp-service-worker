 #-*- coding: utf-8 -*-
#custom models
import os
import  odoo_connector as oc
import  wp_connector as wpc
import cli as cli
import subprocess
from datetime import date
from pathlib import Path
import pathlib
import sys
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
        self.token="599049b6052d49cab0a7ca2692a1aa45"
        self.host = "https://www.3ele.de/api"

    

    def update_plugin(self, name, target):
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
            #          print (wp_instance)
            command = 'wp plugin install '+ plugin['download_url']+' --activate'
            hostname = wp_instance['host']
            username = wp_instance['user']
            path = wp_instance['wp_path']

          #  command = 'wp --info'  
          #  complete_command = "ssh -t "+ hostname+"@"+ username + " \"bash -ic ' "+command+ "'\""
            print (command)
            wp.execute_wp_cli(hostname, username, path, command)
            #print (wp.read_stdout_csv(output))


if __name__ == "__main__": 
    service = WpServiceWorker()
    cli = cli.wp__worker_cli()
    wp = wpc.wp_connector()
    print (cli.command)
    print (cli.instances)
    for wp_instance in cli.instances:
        hostname = wp_instance['host']
        username = wp_instance['user']
        path = wp_instance['wp_path']
        wp.execute_wp_cli(hostname, username, path,cli.command)

   # odoo = oc.odoo_connector(service.token, service.host)
   # wp_instance = odoo.get_id_from_name(name=cli.target, model=cli.model)
   # print (wp_instance)
