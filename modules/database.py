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
                cls._instance.create_tables()
            except Exception as e:
                cls._instance = None  # Reset _instance on failure to ensure reinitialization is possible
                raise ConnectionError(f"Failed to create connection pool: {e}")
        return cls._instance

    def get_conn(self):
        if self._connection_pool:
            self.logger.info("Database connection acquired.")
            return self._connection_pool.getconn()
        else:
            raise ConnectionError("Connection pool is not initialized.")

    def release_conn(self, conn):
        if self._connection_pool:
            self._connection_pool.putconn(conn)
            self.logger.info("Database connection released.")
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

    def create_tables(self):
        tables_query = """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'slack_event_log'
        );
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'doc_dump'
        );
        """
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(tables_query)
                tables_exist = [row[0] for row in cursor.fetchall()]
                if all(tables_exist):
                    self.logger.info("Tables found.")
                else:
                    query = """
                    CREATE TABLE IF NOT EXISTS slack_event_log (
                        id SERIAL PRIMARY KEY,
                        event_body text,
                        event_type text,
                        event_ts text,
                        event_text text,
                        channel_id text,
                        user_id text,
                        user_fname text,
                        user_lname text,
                        user_fullname text,
                        user_email text,
                        files_info text
                    );
                    CREATE TABLE IF NOT EXISTS doc_dump (
                        id SERIAL PRIMARY KEY,
                        file bytea,
                        text text,
                        user_id text
                    );
                    """
                    cursor.execute(query)
                    conn.commit()
                    self.logger.info("Tables created.")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.release_conn(conn)
