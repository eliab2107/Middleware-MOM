class NotificationEngine:
    def __init__(self, storage, consumer, sub_manager):
        self.storage = storage
        self.consumer = consumer
        self.sub_manager = sub_manager

    def handle_request(self, command, payload):
        if command == "PUBLISH":
            event = self.storage.store(payload)
            self.consumer.notify(event)
            return {"status": "ok"}
        
        elif command == "SUBSCRIBE":
            self.sub_manager.add(payload["topic"], payload["client"])
            return {"status": "subscribed"}