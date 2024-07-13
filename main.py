import tkinter as tk
from tkinter import ttk
from views.main_view import MainView
from controllers.main_controller import MainController
 
import settings



def main():

    conf = settings.MemPadSettings.get_instance()
  
    controller = MainController(conf)
    controller.init_view(MainView)
    controller.open(conf.getValue('MRU'))
    

    controller.view.mainloop()

    conf.save()



if __name__ == "__main__":
    main()





 


