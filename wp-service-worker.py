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
import json
#logging.basicConfig(filename='daily_backups.log',level=logging.INFO)
current_dir = pathlib.Path(__file__).parent
current_file = pathlib.Path(__file__)
today = date.today()
date = today.strftime("%Y-%m-%d")

class WpServiceWorker:
    def __init__(self):
        self.token = os.environ.get('ODOO_TOKEN')
        self.host = "https://www.3ele.de/api"
    def backup_all(self):
       #init connector
        odoo = oc.odoo_connector(self.token, self.host)
        #set model
        model ="wp_instance.wp_core"
        #set mod
        mod = "search"
        #set domain
        #set fields, we need from the plugin
        fields='["id","name"]'
        wp_instances = odoo.search_record(fields=fields,mod=mod,model=model)
        
        for wp_instance in wp_instances:
                id = wp_instance['id']
                
       
                
   
                model = 'wp_instance.wp_core'
                mod = 'backup_data'  
                name='daily backup'
                body = ''
                try:
                    backup_data = odoo.call_record_method(id=str(wp_instance['id']), mod=mod,  model=model)
                    backup_data = backup_data['success']
                    backup_data = json.loads(backup_data.replace("'",'"'))[0]             
                    backup_path = str(home)+"/daily_backups/"+wp_instance['name']+"/"+str(date)
                    Path(backup_path).mkdir(parents=True, exist_ok=True)
                    Path(backup_path+'/sql/').mkdir(parents=True, exist_ok=True)
                    #export sql File
                    command ='ssh '+ backup_data['user']  +'@'+ backup_data['wp_host'] +' '+ backup_data['wp_cli_path'] +' db export --path='+backup_data['wp_path']+' '+ backup_data['sql_path']+'/export-'+str(date)+'.sql'
                    try:  
                        os.system(command)
                        logging_message = name+' export_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' success'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>"
                    except:
                        logging_message = name+' export_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' failed'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>" 
                        pass
                    #download sql File
                    command ='rsync -az -q -b '+ backup_data['user']  +'@'+ backup_data['wp_host'] +':' + backup_data['sql_path']+'/export-'+str(date)+'.sql '+backup_path+'/sql/export-'+str(date)+'.sql'
                    try: 
                        os.system(command) 
                        logging_message = name+' download_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' success'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>"          
                    except:
                        logging_message = name+' backup_download_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' failed'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>" 
          
                        pass
                    
                    
                    command ='rsync -az --stats  '+ backup_data['user']  +'@'+ backup_data['wp_host'] + ':'+backup_data['wp_path']+ ' '+backup_path
                    try: 
                        os.system(command)
                        logging_message = name+' download_wp' + str(wp_instance['name']) + ' on ' + str(date) + ' success'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>"            
                    except:
                        logging_message = name+' download_wp' + str(wp_instance['name']) + ' on ' + str(date) + ' failed'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>"    
                        pass
                
                    
                except:
                    logging_message = name+' complete' + str(wp_instance['name']) + ' on ' + str(date) + ' failed'
                    logging.info(logging_message)
                    body += '<p>'+ logging_message + "<\p>" 

                odoo.create_notification(model=model,id=id,name=name, subject=mod, body=body)

    def update_plugin(self, name):
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
 #   cli = cli.wp__worker_cli()

    service.backup_all()
  #  print (cli.model)
  #  odoo = oc.odoo_connector(service.token, service.host)
  #  wp_instance = odoo.get_id_from_name(name="timetorest", model="wp_instance.plugins")
  #  print (wp_instance)

