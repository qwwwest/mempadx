
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
    def blep(cls):
        print('blep')