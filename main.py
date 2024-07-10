import tkinter as tk
from tkinter import ttk
from views.main_view import MainView
from controllers.main_controller import MainController
 
import configparser



def main():

    conf = configparser.ConfigParser(default_section = "Main", allow_no_value=True ) 
    conf.optionxform = lambda option: option
    conf.read("settings.ini") 
  
    controller = MainController(conf)
    controller.init_view(MainView)
    controller.open(conf.get('Main', 'MRU' ))
    

    controller.view.mainloop()

    with open('settings.ini', 'w') as configfile:
        conf.write(configfile)



if __name__ == "__main__":
    main()





 


