# -*- coding: utf-8 -*-
import paramiko
import sys
#global paths
import os
import subprocess
import shlex

class wp_connector:
    def execute_wp_cli(self, hostname, username, wp_path, command):
            try:
                complete_command = "ssh  "+ username+"@"+ hostname + " "  +command
                result = subprocess.check_output(complete_command, shell=True)     
            except:  
               print ("Unexpected error:", sys.exc_info())
              # result = sys.exc_info()
               result = ''
                
            finally:
                return result.decode('utf-8')
            
    def read_stdout_csv(self,source, skipline=1):
        self.source = source
        list = self.source.split(sep=None, maxsplit=-1)
        iter_list = iter(list)

        next(iter_list, skipline)
        

        return iter_list

    def import_plugins(self, host):

        command = host['wp_cli_path'] + ' plugin list --format=csv --path="' +host['wp_path'] + '" '

        stout_csv = self.execute_wp_cli(host['wp_host'],host['user'] ,host['wp_path'], command)
        iter_list = self.read_stdout_csv(stout_csv)
        plugins = []
        for row in iter_list:
            column = row.split(',')       
            obj = {
                "name": column[0],
                "status": column[1],
                "update": column[2],
                "version": column[3]         
            }
            plugins.append(obj)
        
        return plugins
       
    def import_themes(self, host):
        command = host['wp_cli_path'] + ' theme list --format=csv --path="' +host['wp_path'] + '" '
        stout_csv = self.execute_wp_cli(host['wp_host'],host['user'] ,host['wp_path'], command)
        iter_list = self.read_stdout_csv(stout_csv)
        themes = []
        for row in iter_list:
            column = row.split(',')       
            obj = {
                "name": column[0],
                "status": column[1],
                "update": column[2],
                "version": column[3]         
            }
            themes.append(obj)
        
        return themes

                
               
            
     
def import_plugins2():
    
    for wp_instance in wp_instances:
      
        command = 'wp plugin list --format=csv --path="' +wp_instance['wp_path']  + '" '
        plugins = wp.execute_wp_cli(wp_instance['host'],wp_instance['user'] , command)
        plugins_list = plugins.split(sep=None, maxsplit=-1)
        plugins_list = iter(plugins_list)       
        next(plugins_list)
        plugins = []
        for row in plugins_list:
            column = row.split(',')       
            plugin = {
                "name": column[0],
                "status": column[1],
                "update": column[2],
                "version": column[3]         
            }
            plugins.append(plugin)
        print ()       
        wp_instance_id = wp_instance['id']
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        plugins_count = models.execute_kw(db, uid, password,
        'wp_instance.plugins', 'search_count',
        [[['wp_instance','=', wp_instance_id]]],
     )  
  
        
        
        if plugins_count <= len(plugins):          
            for row in plugins_list:
                column = row.split(',')
                
                plugin = {
                    "name": column[0],
                    "status": column[1],
                    "update": column[2],
                    "version": column[3]
                
                }
    
            for plugin in plugins:    

                odoo.import_plugins(url,db,username,password, wp_instance_id, plugin)
        elif plugins_count >= len(plugins):
            
            
            
            names = [ sub['name'] for sub in plugins ]
            
            
            
