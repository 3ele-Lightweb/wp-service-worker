#custom models
import os
import  odoo_connector as oc
import  wp_connector as wpc
import xmlrpc.client
from datetime import date
from pathlib import Path
import pathlib
import sys
current_dir = pathlib.Path(__file__).parent
current_file = pathlib.Path(__file__)
today = date.today()
date = today.strftime("%Y-%m-%d")
def import_themes():
    username = os.environ.get('ODOO_API_USER')
    password = os.environ.get('ODOO_API_PASSWORD')
    db = os.environ.get('ODOO_API_DB')
    url = os.environ.get('ODOO_API_URL')
    SSH_key = os.environ.get('SSH_KEY')
    odoo = oc.odoo_connector()
    wp = wpc.wp_connector()
    wp_instances = odoo.get_odoo_wp_instance(url,db,username,password)
    for wp_instance in wp_instances:
      
        command = 'wp theme list --format=csv --path="' +wp_instance['wp_path']  + '" '
        themes = wp.execute_wp_cli(wp_instance['host'],wp_instance['user'] , SSH_key, command)
        themes_list = themes.split(sep=None, maxsplit=-1)
        themes_list = iter(themes_list)       
        next(themes_list)
        themes = []
        for row in themes_list:
            column = row.split(',')       
            theme = {
                "name": column[0],
                "status": column[1],
                "update": column[2],
                "version": column[3]         
            }
            themes.append(theme)       
        wp_instance_id = wp_instance['id']
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        themes_count = models.execute_kw(db, uid, password,
        'wp_instance.themes', 'search_count',
        [[['wp_instance','=', wp_instance_id]]],
     )  
        if themes_count <= len(themes):            
            for row in themes_list:
                column = row.split(',')               
                theme = {
                    "name": column[0],
                    "status": column[1],
                    "update": column[2],
                    "version": column[3]              
                }
    
            for theme in themes:    
                odoo.import_themes(url,db,username,password, wp_instance_id, theme)

        elif themes_count >= len(themes):
            
            print ('more themes as in wp Instance')
            print (themes)
            names = [ sub['name'] for sub in themes ]
            print (type(names)) 
            
            ids = models.execute_kw(db, uid, password,
        'wp_instance.themes', 'search',
        [(('name','!=', names  ),('wp_instance','=', wp_instance_id))])
            for id in ids:
                models.execute_kw(db, uid, password, 'wp_instance.themes', 'unlink', [[id]])

            
def import_plugins():
    username = os.environ.get('ODOO_API_USER')
    password = os.environ.get('ODOO_API_PASSWORD')
    db = os.environ.get('ODOO_API_DB')
    url = os.environ.get('ODOO_API_URL')
    SSH_key = os.environ.get('SSH_KEY')
    odoo = oc.odoo_connector()
    wp = wpc.wp_connector()
    wp_instances = odoo.get_odoo_wp_instance(url,db,username,password)
    for wp_instance in wp_instances:
      
        command = 'wp plugin list --format=csv --path="' +wp_instance['wp_path']  + '" '
        plugins = wp.execute_wp_cli(wp_instance['host'],wp_instance['user'] , SSH_key, command)
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
            
            
            ids = models.execute_kw(db, uid, password,
        'wp_instance.plugins', 'search',
        [(('name','!=', names  ),('wp_instance','=', wp_instance_id))])
            for id in ids:
                models.execute_kw(db, uid, password, 'wp_instance.plugins', 'unlink', [[id]])
            
            
if __name__ == "__main__":
    if sys.argv:
        if 'import_themes' == sys.argv[1]:
            import_themes()
        elif 'import_plugins' == sys.argv[1]:
            import_plugins()
        else:
            pass
    else:
        pass