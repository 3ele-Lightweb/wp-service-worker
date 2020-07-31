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

    def browse_records(self, model, ids):
        payload = {'token': self.token}
        api_url = str(self.host) +'/'+ str(model) +'/search'
        r = requests.get(api_url, params=payload)
        domain='[("id", "in",'+ids+')]'
        print (r.url)
        wp_instances = r.json() 
        return wp_instances


    def get_id_from_name(self, name, model):
        return  self.search_record(model=model, fields='["name", "id"]', mod="search", domain='[("name","=","'+name+'")]')
    
    def get_list_of_ids(self, model, domain='[()]' ):
            return  self.search_record(model=model, fields='["name", "id", "url"]', mod="browse", domain="[()]")
        



