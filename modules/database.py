import psycopg2
from psycopg2 import pool
from modules.logger import get_logger


class Database:
    _instance = None
    _connection_pool = None

    def __new__(cls, config):  # Corrected signature
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)  # Create new instance
            cls._instance.logger = get_logger("Database")
            # Initialize the connection pool only once
            db_config = {
                "host": config.get("omega.database.host"),
                "port": config.get("omega.database.port"),
                "database": config.get("omega.database.database"),
                "user": config.get("omega.database.user"),
                "password": config.get("omega.database.password"),
            }

            if db_config is None:
                raise ValueError(
                    "Database configuration must be provided on first instantiation."
                )
            try:
                cls._instance._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    minconn=1, maxconn=10, **db_config
                )
                cls._instance.logger.info("Database connection pool was created.")
            except Exception as e:
                cls._instance = None  # Reset _instance on failure to ensure reinitialization is possible
                raise ConnectionError(f"Failed to create connection pool: {e}")
        return cls._instance

    def get_conn(self):
        if self._connection_pool:
            return self._connection_pool.getconn()
        else:
            raise ConnectionError("Connection pool is not initialized.")

    def release_conn(self, conn):
        if self._connection_pool:
            self._connection_pool.putconn(conn)
        else:
            raise ConnectionError("Connection pool is not initialized.")

    def execute_query(self, query, params=None):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if query.lower().strip().startswith("select"):
                    result = cursor.fetchall()
                else:
                    conn.commit()
                    result = None
                self.logger.info(f"Executed query: {query}")
                return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.release_conn(conn)
