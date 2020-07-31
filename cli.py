# -*- coding: utf-8 -*-

import argparse

class wp__worker_cli:
    def func_not_found(): # just in case we dont have the function
        print ('No Function  Found!')
    
    def __init__(self):
        parser = argparse.ArgumentParser(description='Add mod, command and target')
        parser.add_argument('mod', choices=['core', 'plugin', 'theme','db','config'],
                            help='mod aka core, plugin theme')
        parser.add_argument('command')
        parser.add_argument('target', metavar='target', type=str, nargs='+',
                            help='add Record ID to change the target')
        args = parser.parse_args()
        func = getattr(self,args.mod) 
        func()
        self.model = func()
        #return model,args.command,args.target

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

