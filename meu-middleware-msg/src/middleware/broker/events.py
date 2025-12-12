class EventStorage:
    def __init__(self):
        self.events = []  # Ou deque

    def add_event(self, topic, data):
        event = {"topic": topic, "data": data}
        self.events.append(event)
        return event

    def pop_next(self):
        return self.events.pop(0) if self.events else None
