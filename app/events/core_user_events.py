from app.events.base_event import Event


class CoreUserCreatedEvent(Event):
    def __init__(self, user_id: str, email: str, is_owner: bool):
        self.user_id = user_id
        self.email = email
        self.is_owner = is_owner
