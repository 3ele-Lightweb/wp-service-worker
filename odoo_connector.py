import logging
import json
import requests

class odoo_connector:
    def __init__(self, token, host):   
        self.token=token
        self.host = host
        
    def get_record(self,model,mod, fields='["name","url","wp_path","sql_path","host","user","ssh_port"]', domain='[()]'):
       payload = {'token': self.token, 'fields':fields, 'domain':domain}
       api_url = str(self.host) +'/'+ str(model) +'/'+ str(mod)
       r = requests.get(api_url, params=payload)
    #   print (r.url)
       wp_instances = r.json()
       
       return wp_instances
    

