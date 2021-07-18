# Packages
from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy import create_engine, exc
from sqlalchemy.dialects import registry
from sqlalchemy.orm import sessionmaker

from transactions import (get_user_txn)

registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect",
                  "CockroachDBDialect")


class DatabaseLayer:
    def __init__(self, conn_string, max_records=20):
        self.engine = create_engine(conn_string, convert_unicode=True)
        self.connection_string = conn_string
        self.max_records = max_records

    def get_user(self, username=None, email=None):
        return run_transaction(sessionmaker(bind=self.engine),
                               lambda session: get_user_txn(session, username))

