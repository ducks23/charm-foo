#! /usr/bin/env python3

import logging, sys

sys.path.append('lib')

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus
from bar import Bar
from interface_mysql import MySQLClient

logger = logging.getLogger()

class FooCharm(CharmBase):
    bar = Bar
    def __init__(self, *args):
        super().__init__(*args)

        self._bar = self.bar(self, 'bar')
        self.db = MySQLClient(self, 'db')

        self.framework.observe(
            self.db.on.database_available,
            self._on_database_available
        )
        self.framework.observe(
            self._bar.on.config_changed,
            self._on_config_changed
        )

    def _on_database_available(self, event):
        self._bar.foo()
        logger.info(event.db_info.user)
        self.unit.status = ActiveStatus("db related")

    def _on_config_changed(self, event):
        logger.info("start application")
        self.unit.status = ActiveStatus("application started")

if __name__ == "__main__":
    main(FooCharm)
