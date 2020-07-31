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
                complete_command = "ssh -t "+ username+"@"+ hostname + " \"bash -ic ' " +command+ " --path="+wp_path+" '\""
             #   print (complete_command)
                result = subprocess.check_output(complete_command, shell=True)
                result = complete_command
            except:
               # return err
    
               print ("Unexpected error:", sys.exc_info())
               result = sys.exc_info()
            finally:
                return result
            
          #  try:
          #      complete_command = "ssh -t "+ username+"@"+ hostname + " \"bash -ic ' " +command+ " '\""
          #      args = shlex.split(complete_command)
          #      print (args)
          #      process = subprocess.check_output(complete_command, shell=False)
          #      (stdout, stderr) = process.communicate()
          #      print(stdout.decode())
          #  except:
          #      print("ERROR {} while running {}".format(sys.exc_info()[1], command))
    def read_stdout_csv(self,source, skipline=1):
        self.source = source
        list = self.source.split(sep=None, maxsplit=-1)
        iter_list = iter(list)
        next(iter_list, skipline)
        return iter_list

    def wp_update(self,mod, wp_instances):
        if mod == 'core':
                base_command = 'core update'
        elif mod == 'theme':
                base_command = 'theme update --all'
        elif mod == 'plugin':  
                base_command = 'plugin update --all' 
    
                
               
            
        for wp_instance in wp_instances:
                user = str(wp_instance['user'][4:])
                wp_cli_path ="www/htdocs/"+ str(user) +"/wp-cli/wp-cli.phar"
                wp_path = str(wp_instance['wp_path'])
                
        
                command =  wp_cli_path +' ' + base_command +' --path="' + wp_path + '" '

                try:
                    
                    msg = self.execute_wp_cli(wp_instance['host'], wp_instance['user'], mySSHK, command)
                    print (msg)
                except:
        
                    pass
def import_plugins():
    
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
            
            
            
