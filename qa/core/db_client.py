import psycopg


class DBClient:

    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.connection = psycopg.connect(**self.connection_params)
        self.cursor = self.connection.cursor()

    def close(self):
        """Close cursor and connection"""
        self.cursor.close()
        self.connection.close()

    def commit(self):
        self.connection.commit()
