class PluginEventManager:
    def __init__(self, app):
        self.app = app
        self._listeners = {}

    def subscribe(self, event_name, listener):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)
        self.app.log.info(f"{listener} Subscribed to {event_name}")

    def publish(self, event_name, *args, **kwargs):
        listeners = self._listeners.get(event_name, [])
        if not listeners:
            self.app.log.info(f"No listeners for event: {event_name}")
        for listener in listeners:
            listener(*args, **kwargs)
