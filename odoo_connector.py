 #-*- coding: utf-8 -*-
import logging
import json
import requests

class odoo_connector:
    def __init__(self, token, host):   
        self.token=token
        self.host = host
        
    def search_record(self,model,mod, fields='["id","name","url","wp_path","sql_path","host","user","ssh_port"]', domain='[]'):
       payload = {'token': self.token, 'fields':fields, 'domain':domain}
       api_url = str(self.host) +'/'+ str(model) +'/'+ str(mod)
       r = requests.get(api_url, params=payload)
       wp_instances = r.json() 
       return wp_instances

    def call_record_method(self,id,mod,model):
       payload = {'token': self.token}
       api_url = str(self.host)+'/'+ str(model) +'/'+ str(id) +'/method/'+ str(mod)
       r = requests.get(api_url, params=payload)

       action = r.json() 
       return action

    def browse_records(self, model, ids):
        payload = {'token': self.token}
        api_url = str(self.host) +'/'+ str(model) +'/search'
        r = requests.get(api_url, params=payload)
        domain='[("id", "in",'+ids+')]'
        wp_instances = r.json() 
        return wp_instances


    def get_id_from_name(self, name, model):
        return  self.search_record(model=model, fields='["name", "id"]', mod="search", domain='[("name","=","'+name+'")]')
    
    def get_list_of_ids(self, model, domain='[()]' ):
            return  self.search_record(model=model, fields='["name", "id", "url"]', mod="browse", domain="[()]")

    def backup_all(self):
       #init connector

        #set model
        model ="wp_instance.wp_core"
        #set mod
        mod = "search"
        #set domain
        #set fields, we need from the plugin
        fields='["id","name"]'
        wp_instances = self.search_record(fields=fields,mod=mod,model=model)
        for wp_instance in wp_instances:  
                model = 'wp_instance.wp_core'
                mod = 'backup_data'
                
                try:
                    backup_data = self.call_record_method(id=str(wp_instance['id']), mod=mod,  model=model)
            
                    backup_data = backup_data['success']

                    
                    backup_data = json.loads(backup_data.replace("'",'"'))[0]



                
                    backup_path = str(home)+"/daily_backups/"+wp_instance['name']+"/"+str(date)
                    Path(backup_path).mkdir(parents=True, exist_ok=True)
                    Path(backup_path+'/sql/').mkdir(parents=True, exist_ok=True)
                    #export sql File
                    command ='ssh '+ backup_data['user']  +'@'+ backup_data['wp_host'] +' '+ backup_data['wp_cli_path'] +' db export --path='+backup_data['wp_path']+' '+ backup_data['sql_path']+'/export-'+str(date)+'.sql'
                    try:  
                        os.system(command)
                    except:
                        logging.info('daily backup export_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' failed')
                        pass
                    #download sql File
                    command ='rsync -az -q -b '+ backup_data['user']  +'@'+ backup_data['wp_host'] +':' + backup_data['sql_path']+'/export-'+str(date)+'.sql '+backup_path+'/sql/export-'+str(date)+'.sql'
                    try: 
                        os.system(command)           
                    except:
                        logging.info('daily backup_download_sql_file' + str(wp_instance['name']) + ' on ' + str(date) + ' failed')
                        pass
                    
                    
                    command ='rsync -az --stats  '+ backup_data['user']  +'@'+ backup_data['wp_host'] + ':'+backup_data['wp_path']+ ' '+backup_path
                    try: 
                        os.system(command)           
                    except:
                        logging.info('daily backup download_wp_file' + str(wp_instance['name']) + ' on ' + str(date) + ' failed')
                        pass
                
                    
                except:
                    logging.info('daily complete failed')
        



