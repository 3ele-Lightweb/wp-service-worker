import paramiko
import sys
#global paths
import os


class wp_connector:
    def execute_wp_cli(self, hostname, username, command):
            try:
                complete_command = "ssh -t "+ hostname+"@"+ username + " \"bash -ic '"+command+"'\""
                result = subprocess.check_output(complete_command, shell=True,stderr=subprocess.STDOUT)
                
            except:
               # return err
    
               print ("Unexpected error:", sys.exc_info())
               result = sys.exc_info()
            finally:
                return result
    

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
