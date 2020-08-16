# -*- coding: utf-8 -*-

import argparse
import  odoo_connector as oc
import  wp_connector as wpc
from  wp_service_worker import WpServiceWorker
from tabulate import tabulate
import json
class wp__worker_cli:
    def func_not_found(): # just in case we dont have the function
        print ('No Function  Found!')
    
    def __init__(self):
        parser = argparse.ArgumentParser(description='Add mod, command and target')
        parser.add_argument('mod', choices=['core', 'plugin', 'theme','db','config', 'backup'],
                            help='mod aka core, plugin theme')
        parser.add_argument('command')
        parser.add_argument('--name')
        parser.add_argument('--target', 
                            help='add Record ID to change the target')
        args = parser.parse_args()
        mod_func = getattr(self,args.mod) 
        self.mod = args.mod
        self.model = mod_func()
        self.service = WpServiceWorker()
        self.odoo = oc.odoo_connector(self.service.token, self.service.host)
        self.command = args.command
        self.name = args.name
        self.mods_of_targets(args.target)

        if (self.command == 'backup'):
   
            self.odoo = oc.odoo_connector(self.service.token, self.service.host)
            self.service = WpServiceWorker()
            self.service.backup_all('target')
      


#return modelname of args argument mod

    def plugin(self):
        global model 
        model = 'wp_instance.plugins'
        return model

    def theme(self):
        global model 
        model = 'wp_instance.themes'
        return model
    
    def core(self):
        global model 
        model = 'wp_instance.wp_core'
        return model

    def backup(self): 
        model = 'wp_instance.wp_core'
        return model


#return modelname of args argument target

    def mods_of_targets(self,argument):

        
        target_model = 'wp_instance.wp_core'
        if(argument == 'all'):
            
            self.all(argument, target_model)

 
     
            
        else:     
            self.single(argument, target_model)


    def all(self, argument, model):
        odoo = oc.odoo_connector(self.service.token, self.service.host)
        #set model

        #set mod
        mod = "search"
        data = odoo.search_record(mod=mod,model=model)
        self.instances = data
        self.show_result( data)     
    
    def single(self, argument, model):


        if (argument.isnumeric()):
            id = self.odoo.browse_records(ids=[argument], model=model )
            return argument

        else:
            id = self.odoo.get_id_from_name(name=argument, model=model)
            if (id):
                self.show_result(id[0])
            else:
                return None

    def show_result(self, data):
            values = []
            keys = []
            for dataset in data:
                values.append( list(dataset.values()))

                keys = list(dataset.keys())
            
            print(tabulate(values, headers=keys))

        