import configparser
import tkinter as tk

# OnTop = 0
# Wrap = 1
# EditLock = 0
# ExitEsc = 1
# AutoSave = 0
# SearchRange = 101
# searchX = 712
# searchY = 116
# NoBackup = 1

class MemPadSettings:
 
  
    def __init__(self):
        conf = configparser.ConfigParser(default_section = "Main", allow_no_value=True ) 
        conf.optionxform = lambda option: option
        conf.read(MemPadSettings.app_path + "/settings.ini") 

        self.conf = conf
        self.values = {}
        self.tkVariables = {}
        self.types = {}
    
    @staticmethod
    def get_instance(app_path = None, is_app = None, theme = None):
        if not hasattr(MemPadSettings, '_instance'):
            MemPadSettings.app_path = app_path
            MemPadSettings.is_app = is_app
            MemPadSettings.theme = theme
            MemPadSettings._instance = MemPadSettings()
         
 
        return MemPadSettings._instance
 

    def save(self):

        with open(MemPadSettings.app_path + '/settings.ini', 'w') as configfile:
            self.conf.write(configfile)

    def getVariable(self, name, var_type = 'str'):
        if not name in self.tkVariables:
            strval = self.conf.get('Main', name)
            if(var_type == 'bool'):
                self.tkVariables[name] = tk.BooleanVar()
                value = (strval == "1") 
            elif(var_type == 'str'):
                self.tkVariables[name] = tk.Variable()
                value = strval
            elif(var_type == 'int'):
                self.tkVariables[name] = tk.IntVar()  
                value = str(strval)
            else:
                print('NOPE type not found',name,  var_type)    
            self.tkVariables[name].set(value)     
            self.types[name] = var_type     
        return self.tkVariables[name]

    def getValue(self, name, var_type = 'str'):
 
        var = self.getVariable(name, var_type)
        return var.get()
      
 

    def setValue(self, name, value):
        
  
        self.tkVariables[name].set(value) 
        self.hasChanged(name)
 
    
    def hasChanged(self, name):

        value = self.tkVariables[name].get() 

        if isinstance(value, bool):
            value = '1' if value else '0'
        self.conf.set('Main', name, str(value))