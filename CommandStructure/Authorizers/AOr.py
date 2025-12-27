from CommandStructure.Authorizers.Authorizer import Authorizer
from DataClasses.EventContext import EventContext


class AOr:
    def __init__(self, authorizer1: Authorizer, authorizer2: Authorizer):
        self.authorizer1 = authorizer1
        self.authorizer2 = authorizer2

    def get_authorization(self, context: EventContext) -> bool:
        return (
                self.authorizer1.get_authorization(context) or self.authorizer2.get_authorization(context)
        )