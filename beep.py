
class Beep(object):

    _listeners = {}

    @classmethod
    def listen(cls, event_name, handler):
        if event_name not in cls._listeners:
            # event_name not used is an empty list
            cls._listeners[event_name] = []
            
        cls._listeners[event_name].append(handler)
        
    @classmethod
    def dispatch(cls, event_name, *args):
        if cls._listeners.get(event_name):
            for func in cls._listeners[event_name]:
                func(event_name, *args)

    @classmethod
    def remove(cls, event_name, handler):
        if event_name not in cls._listeners:
            # event_name not used is an empty list
            return
            
        handlers_array = cls._listeners[event_name]
        for idx, handler_item in enumerate(handlers_array): 
            if handler_item == handler :
                del handlers_array[idx]
    
    @classmethod
    def removeEvent(cls, event_name):
        if event_name in cls._listeners:
            del cls._listeners[event_name]
       