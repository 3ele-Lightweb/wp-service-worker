 #-*- coding: utf-8 -*-
import logging
import json
import requests
import logging
import  odoo_connector as oc
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
        if action.get('success'):
            action = action['success'].replace("'",'"')
            action = action.replace("False","false")

            if("false" not in action): 
                return json.loads(action)[0]
        else:
            print (action)
            pass
            

    def get_record(self, model, id, fields='["id","name","url","wp_path","sql_path","host","user","ssh_port"]'):
        payload = {'token': self.token, 'fields':fields}
        api_url = str(self.host) +'/'+ str(model) +'/search/'+str(id)
        r = requests.get(api_url, params=payload)
        print (r.url)
        
        wp_instances = r.json() 
        return wp_instances


    def get_id_from_name(self, name, model):
        return  self.search_record(model=model, fields='["id"]', mod="search", domain='[("name","=","'+name+'")]')
    
    def get_list_of_ids(self, model, domain='[()]' ):
            return  self.search_record(model=model, fields='["name", "id", "url"]', mod="browse", domain="[()]")
    
  #  def get_project_id_from_record_id(self, wp_instance_id):
  #      return  self.search_record(model=model, fields='["name", "id"]', mod="search", domain='[("name","=","'+name+'")]')


    def create_notification(self, model, id,name, subject, body):
        create_vals= {
            'name' : name,
            'model': model,
            'subject' : subject,
            'body' : body,
            'res_id' : id,
        }
        api_url = str(self.host) +'/mail.message/create/'
        payload = {'token': self.token, 'create_vals': json.dumps(create_vals)}
        r = requests.get(api_url, params=payload)


    def create_record(self, model,create_vals):
        api_url = str(self.host) +'/'+str(model)+'/create/'
        payload = {'token': self.token, 'create_vals': json.dumps(create_vals)}
        r = requests.get(api_url, params=payload)
        print (r.json())
        return r.json()


    def update_record(self, model, id, create_vals):
        api_url = str(self.host) +'/'+str(model)+'/update/'+str(id)
        payload = {'token': self.token, 'update_vals': json.dumps(create_vals)}
        r = requests.get(api_url, params=payload)  
        print (r.url)    
        return r.json() 



