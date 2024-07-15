import tkinter as tk
from tkinter import ttk
from views.main_view import MainView
from controllers.main_controller import MainController
import os
import settings



def main():

    mempadpath = os.path.abspath(os.path.dirname(__file__))
    os.chdir(mempadpath)
    
    conf = settings.MemPadSettings.get_instance(mempadpath)
  
    controller = MainController(conf)
    controller.init_view(MainView)
    if conf.getValue('MRU'):
        controller.open(conf.getValue('MRU'))
    

    controller.view.mainloop()

    conf.save()



if __name__ == "__main__":
    main()





 


