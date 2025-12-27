from DataClasses.EventContext import EventContext


class AOnId:
    def __init__(self, id: int):
        self.id = id

    def get_authorization(self, context: EventContext) -> bool:
        return (
                context.id is not None
                and context.id == self.id
        )