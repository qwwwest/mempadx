import tkinter as tk
from tkinter import ttk
from views.main_view import MainView
from controllers.main_controller import MainController
import sys
import os
import os.path
import settings



def main():

  # If the 'frozen' flag is set, we are in bundled-app mode!
    if getattr(sys, "frozen", False):
        # bundled-app mode. Everything is relative to executable folder before extraction
        mempadpath = os.path.abspath(os.path.dirname(sys.executable))
        is_app = True
        theme = sys._MEIPASS + '/views/themes/Forest-ttk-theme/forest-dark.tcl'
   
       
        ## to check: sys._MEIPASS
    else:
        # Normal mode. Everything relative to "main.py"
        mempadpath = os.path.abspath(os.path.dirname(__file__))
        is_app = False
        theme = os.path.abspath(os.path.dirname(__file__)) + '/views/themes/Forest-ttk-theme/forest-dark.tcl'
     
   
    os.chdir(mempadpath)
    
    conf = settings.MemPadSettings.get_instance(mempadpath, is_app, theme)
  
    controller = MainController(conf)
    controller.init_view(MainView)
    if conf.getValue('MRU'):
        controller.open(conf.getValue('MRU'))
    

    controller.view.mainloop()

    conf.save()



if __name__ == "__main__":
    main()





 


