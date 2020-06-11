import logging

from ops.framework import (
        Object,
        StoredState,
        EventBase,
        EventSource,
        ObjectEvents,
)

logger = logging.getLogger()


class ConfigChangedEvent(EventBase):
    def __init__(self, handle):
        super().__init__(handle)
        self.config = True

    def is_configured(self):
        return self.config

class BarEvents(ObjectEvents):
    config_changed = EventSource(ConfigChangedEvent)

class Bar(Object):
    on = BarEvents()

    def __init__(self, charm, key):
        super().__init__(charm, key)
   
    def foo(self):
       logger.info("inside of foo")
       self.on.config_changed.emit()


