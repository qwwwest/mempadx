import configparser
import tkinter as tk
import os 
  


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

        self.settings_file = MemPadSettings.app_path + "/settings.ini"
  
        if not os.path.exists(self.settings_file): 
            with open(self.settings_file, 'w') as file: 
                file.write(self.get_default_settings()) 
                file.close()

        conf.read(self.settings_file ) 

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
 

    def get_default_settings(self):
        return """
[Main]
ext = .lst
Iwidth = 296
Font = Tahoma,16,0,$FFFFFF
iFont = Tahoma,11,0,$FFFFFF
BGcolor = $804000
BGIcolor = $224488
OnTop = 0
Wrap = 1
EditLock = 0
ExitEsc = 1
AutoSave = 0
SearchRange = 101
searchX = 0
searchY = 0
NoBackup = 1
Win98crypt = 0
DecryptFailWarn = 0
MRU =  MemPadX.lst
LatestFiles = MemPadX.lst
NumKeep = 10
winX = 0
winY = 136
WinWidth = 800
WinHeight = 600
"""

    def save(self):

        with open(self.settings_file, 'w') as configfile:
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