#import paramiko
import sys
#global paths
path = sys.path[0]
import os
path = '/home/piep/.ssh/'
mySSHK = path + 'id_rsa.pub'
mySSHK = os.environ.get('SSH_KEY')
class wp_connector:
    def execute_wp_cli(self, hostname, username, mySSHK, command):
            self.hostname = hostname
            self.mySSHK = mySSHK
            self.command = command
            self.username = username

            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=self.hostname, username=self.username, key_filename=self.mySSHK)
                stdin, stdout, stderr = ssh_client.exec_command(self.command)
                msg = stdout.read().decode('utf-8')
                print (stdout.read().decode('utf-8'), flush=True)
                print (stderr.read().decode('utf-8'), flush=True)
            finally:
                ssh_client.close()
                return msg

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
