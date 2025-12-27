from DataClasses.EventType import EventType, EventContext


class AOnEventType:
    def __init__(self, event_type: EventType):
        self.event_type = event_type

    def get_authorization(self, context: EventContext) -> bool:
        return (
                context.event_type == self.event_type
        )