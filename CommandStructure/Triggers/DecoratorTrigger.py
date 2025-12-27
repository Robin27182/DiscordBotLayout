from DataClasses.EventContext import EventContext
from DataClasses.EventType import EventType
from CommandStructure.Triggers.Trigger import Trigger


class DecoratorTrigger(Trigger):
    def __init__(self):
        """
        The hard part about DecoratorTrigger is that it needs to form its own context by blindly plucking args.
        Multiple functions exist to properly construct context.
        """
        super().__init__()

    def emit_interaction_event(self, event_type: EventType):
        """
        Assumes an Interaction as the first argument to the function
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                context = EventContext(event_type, args[0])
                self.emit(context)
                return func(*args, **kwargs)
            return wrapper
        return decorator