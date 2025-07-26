from app.events.base_event import Event


class TenantUserCreatedEvent(Event):
    def __init__(self, user_id: str, email: str, first_name: str, last_name: str):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


class TenantUserUpdatedEvent(Event):
    def __init__(self, user_id: str):
        self.user_id = user_id
