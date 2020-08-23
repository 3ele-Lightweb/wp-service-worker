 #-*- coding: utf-8 -*-
#custom models
import os
import  odoo_connector as oc
import  wp_connector as wpc
import cli as cli
import subprocess
from datetime import datetime
from pathlib import Path
import pathlib
import sys
from pathlib import Path
home = str(Path.home())
import logging
import json
current_dir = pathlib.Path(__file__).parent
current_file = pathlib.Path(__file__)
today = datetime.now()
date = today.strftime("%Y-%m-%d-%H-%M")
import fire

def is_int(val):
    #if val.isdigit():
    if type(val) == int:
        return True
    else:
        return False

class WpServiceWorker:
    def __init__(self):
        self.token = os.environ.get('ODOO_TOKEN')
        self.host = "https://www.3ele.de/api"

    def show(self):
        print (self.wp_instances) 

 
    def import_wp_instance_plugins(self):
        #init connector
        odoo = oc.odoo_connector(self.token, self.host)
        #set model
        model ="wp_instance.wp_core"
        #set mod
        mod = "search"
        #set domain
        #domain = '[("name","=","wp-timetorest")]'
        #set fields, we need from the plugin
        fields='["name","id","plugins", "themes", "hoster"]'
        #call odoo API
        wp_instances = odoo.search_record(fields=fields,mod=mod,model=model)
        
        #init wp-connector
        wp = wpc.wp_connector()
        for wp_instance in wp_instances:
            model = 'wp_instance.wp_core'
            mod = 'backup_data'  
            host = odoo.call_record_method(id=str(wp_instance['id']), mod=mod,  model=model)

            if (host):
        
                r_plugins = wp.import_plugins(host)
                plugin_ids = []
                for r_plugin in r_plugins:
  
                    model ="wp_instance.plugins"

                    #plugin_records = odoo.get_id_from_name(r_plugin['name'], model)
                    plugin_records =odoo.search_record(model,'search', fields='["id","name"]', 
                    domain='[("wp_instance","=","'+str(wp_instance["id"])+'"),("name","=","'+r_plugin['name']+'")]')
                    if(plugin_records):
                        for plugin_record in plugin_records:
                      
                            plugin_ids.append(plugin_record['id'])
                            odoo.update_record('wp_instance.plugins', plugin_record['id'], r_plugin)
                    else: 
                        plugin_records = odoo.search_record(model,'search', fields='["id","name"]',domain='[("name","=","'+str(r_plugin["name"])+'")]') 
                        if(plugin_records):                          
                            plugin_ids.append(plugin_records[0]['id'])
                            r_plugin['wp_instance'] = 4,[wp_instance['id']]            
                            print (odoo.update_record(model,plugin_records[0]['id'],r_plugin))
                        else:
                            r_plugin['wp_instance'] = [4,wp_instance['id']]
                            
                            plugin_id = odoo.create_record(model,r_plugin)
   
                            plugin_ids.append(plugin_id['id'])
                      
 
                
                wp_instance['plugins'] = [(6,0,plugin_ids)]
                print (wp_instance)
                print (odoo.update_record('wp_instance.wp_core', wp_instance['id'], wp_instance))

             #   wp.import_themes(host)

    def import_wp_instance_themes(self):
        #init connector
        odoo = oc.odoo_connector(self.token, self.host)
        #set model
        model ="wp_instance.wp_core"
        #set mod
        mod = "search"
        #set domain
        #domain = '[("name","=","wp-timetorest")]'
        #set fields, we need from the theme
        fields='["name","id","themes", "themes", "hoster"]'
        #call odoo API
        wp_instances = odoo.search_record(fields=fields,mod=mod,model=model)
        
        #init wp-connector
        wp = wpc.wp_connector()
        for wp_instance in wp_instances:
            model = 'wp_instance.wp_core'
            mod = 'backup_data'  
            host = odoo.call_record_method(id=str(wp_instance['id']), mod=mod,  model=model)

            if (host):
        
                r_themes = wp.import_themes(host)
                theme_ids = []
                for r_theme in r_themes:
  
                    model ="wp_instance.themes"

                    #theme_records = odoo.get_id_from_name(r_theme['name'], model)
                    theme_records =odoo.search_record(model,'search', fields='["id","name"]', 
                    domain='[("wp_instance","=","'+str(wp_instance["id"])+'"),("name","=","'+r_theme['name']+'")]')
                    if(theme_records):
                        for theme_record in theme_records:
                      
                            theme_ids.append(theme_record['id'])
                            odoo.update_record('wp_instance.themes', theme_record['id'], r_theme)
                    else: 
                        theme_records = odoo.search_record(model,'search', fields='["id","name"]',domain='[("name","=","'+str(r_theme["name"])+'")]') 
                        if(theme_records):                          
                            theme_ids.append(theme_records[0]['id'])
                            r_theme['wp_instance'] = 4,[wp_instance['id']]            
                            print (odoo.update_record(model,theme_records[0]['id'],r_theme))
                        else:
                            r_theme['wp_instance'] = [4,wp_instance['id']]
                            
                            theme_id = odoo.create_record(model,r_theme)
   
                            theme_ids.append(theme_id['id'])
                      
 
                
                wp_instance['themes'] = [(6,0,theme_ids)]
                print (wp_instance)
                print (odoo.update_record('wp_instance.wp_core', wp_instance['id'], wp_instance))

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

class plugin(WpServiceWorker):
    def __init__(self, target):
        super().__init__()

        if (is_int(target)):
            self.odoo = oc.odoo_connector(self.token, self.host)
            #set model
            model ="wp_instance.plugins"
            #set mod
            mod = "search"    
            #set domain
            #set fields, we need from the wp_instance
            fields='["id","name"]'
  
            records = self.odoo.get_record(model,target, fields)
            
            self.wp_instances = records 
        
        else:
            self.wp_instances = []

class theme(WpServiceWorker):
        def __init__(self, target):
            super().__init__()

            if (is_int(target)):
                self.odoo = oc.odoo_connector(self.token, self.host)
                #set model
                model ="wp_instance.themes"
                #set mod
                mod = "search"    
                #set domain
                #set fields, we need from the wp_instance
                fields='["id","name"]'
    
                records = self.odoo.get_record(model,target, fields)
                
                self.wp_instances = records 
            
            else:
                self.wp_instances = []

            

class core(WpServiceWorker):
    def __init__(self, target):
        super().__init__()
        self.odoo = oc.odoo_connector(self.token, self.host)
            #set model
        model ="wp_instance.wp_core"
        #set mod
        mod = "search"    
        #set domain
        #set fields, we need from the wp_instance
        fields='["id","name"]'
        
        if (is_int(target)):

            records = self.odoo.get_record(model,target)
            
            self.wp_instances = records 
        
        elif(target == 'all'):
            self.wp_instances =self.odoo.search_record(model,mod, fields='["id","name","url","wp_path","sql_path","host","user","ssh_port"]', domain='[]')
            
            
            

      
    def backup(self):
        for wp_instance in self.wp_instances:
                print (wp_instance['name'])
                id = wp_instance['id']
                model = 'wp_instance.wp_core'
                mod = 'backup_data'  
                name='daily backup'
                body = ''
                try:
                    #call methode from odoo wp_hosts modul to get sort data
                    backup_data = self.odoo.call_record_method(id=str(wp_instance['id']), mod=mod,  model=model)
                    backup_data = backup_data['success']
                    backup_data = json.loads(backup_data.replace("'",'"'))[0]
                    folder_name = wp_instance['name'].replace(" ", "")             
                    backup_path = str(home)+"/daily_backups/"+folder_name+"/"+str(date)
                    Path(backup_path).mkdir(parents=True, exist_ok=True)
                    Path(backup_path+'/sql/').mkdir(parents=True, exist_ok=True)
                    #export sql File
                    command ='ssh '+ backup_data['user']  +'@'+ backup_data['wp_host'] +' '+ backup_data['wp_cli_path'] +' db export --path='+backup_data['wp_path']+' '+ backup_data['sql_path']+'/export-'+str(date)+'.sql'
                    try: 
                        
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT) 
                        print (type(output))
                        print (output)
                        logging_message = name+' export_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' success'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>"+'<p>'+ output.decode("utf-8")  + "<\p>"
                        
                    except Exception as e:
                        logging_message = name+' export_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' failed'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + str(e)+"<\p>" 
                        print (str(e))
                        pass
                    #download sql File
                    command ='rsync -az -q -b '+ backup_data['user']  +'@'+ backup_data['wp_host'] +':' + backup_data['sql_path']+'/export-'+str(date)+'.sql '+backup_path+'/sql/export-'+str(date)+'.sql'
                    try: 
                        output = subprocess.check_output(command, shell=True)  
                        logging_message = name+' download_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' success'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>"+'<p>'+ output.decode("utf-8")  + "<\p>"          
                    except Exception as e:
                        logging_message = name+' backup_download_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' failed'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + str(e)+"<\p>" 
                        print (str(e) )
                        pass
                    
                    
                    command ='rsync -az --stats  '+ backup_data['user']  +'@'+ backup_data['wp_host'] + ':'+backup_data['wp_path']+ ' '+backup_path
                    try: 
                        output = subprocess.check_output(command, shell=True) 
                        logging_message = name+' download_wp' + str(wp_instance['name']) + ' on ' + str(date) + ' success'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + "<\p>"+'<p>'+ output.decode("utf-8")  + "<\p>"          
                    except Exception as e:
                        logging_message = name+' download_wp' + str(wp_instance['name']) + ' on ' + str(date) + ' failed'
                        logging.info(logging_message)
                        body += '<p>'+ logging_message + str(e) +"<\p>"    
                        
                        pass   
                except Exception as e:
                    logging_message = name+' complete' + str(wp_instance['name']) + ' on ' + str(date) + ' failed'
                    logging.info(logging_message)
                    body += '<p>'+ logging_message + str(e)+"<\p>"
             

                self.odoo.create_notification(model=model,id=id,name=name, subject=mod, body=body)


if __name__ == "__main__": 
    #fire.Fire(WpServiceWorker)
     fire.Fire({
      'core': core,
      'plugin': plugin,
      'theme': theme,
     })

    #service = WpServiceWorker()
 #   cli = cli.wp__worker_cli()

    #service.backup_all()
  #  print (cli.model)
  #  odoo = oc.odoo_connector(service.token, service.host)
  #  wp_instance = odoo.get_id_from_name(name="timetorest", model="wp_instance.plugins")
  #  print (wp_instance)

