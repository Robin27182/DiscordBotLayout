from DataClasses.EventContext import EventContext


class AlwaysAccept:
    def __init__(self):
        return

    def get_authorization(self, context: EventContext) -> bool:
        return True