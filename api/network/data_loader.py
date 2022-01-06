import os
from dataclasses import dataclass

import psycopg2
from network.models import Edge, Node


@dataclass
class DBConfig:
    """External database configuration."""

    host: str = os.environ["EXTERNAL_DB_HOST"]
    port: int = os.environ["EXTERNAL_DB_PORT"]
    user: str = os.environ["EXTERNAL_DB_USER"]
    password: str = os.environ["EXTERNAL_DB_PASSWORD"]
    database: str = os.environ["EXTERNAL_DB_NAME"]


class Loader(DBConfig):
    """Class that loads data from the external database."""

    def _connection(self):
        return psycopg2.connect(
            dbname=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def fetch_nodes(self):
        """Fetches all records from the nodes table."""

        with self._connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    SELECT * 
                    FROM nodes;
                    """
                )
                return (Node.from_db_record(record) for record in curs.fetchall())

    def fetch_edges(self):
        """Fetches all records from the edges table."""

        with self._connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    f"""
                    SELECT * 
                    FROM edges;                   
                    """
                )
                return (Edge.from_db_record(record) for record in curs.fetchall())
