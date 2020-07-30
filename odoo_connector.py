import logging
import json
import requests

class odoo_connector:
    def get_odoo_wp_instance(self,url,token):
       payload = {'token': token, 'fields':'["name","url","wp_path","sql_path","host","user","ssh_port"]'}
       r = requests.get(url, params=payload)
       print(r.url)
       print(r.text)
       print (r)
       # common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
       # common.version()
       # uid = common.authenticate(db, username, password, {})
       # models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
       wp_instances = r.json()
      #wp_instances = models.execute_kw(db, uid, password,
       # 'wp_instance.wp_core', 'search_read',
       # [ [['extern_backups', '=',True ]]],
       # {'fields': ['url', 'host','name', 'user', 'wp_path','sql_path', 'ssh_port']})
       return wp_instances

    
