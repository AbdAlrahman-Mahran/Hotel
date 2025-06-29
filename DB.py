import mysql.connector

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # create the one and only instance
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]



class DB(metaclass=SingletonMeta):
    def __init__(self, host: str, user: str, password: str, database: str):
        if getattr(self, "_initialized", False):
            return
        try:
            self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            raise

        self._initialized = True


