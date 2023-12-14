import os
from dotenv import load_dotenv
from colorama import init, Fore
from pyspark.sql import SparkSession


class PostgreDB:
    """
    A class for connecting to PostgreSQL database using PySpark.

    Attributes:
        spark (pyspark.sql.SparkSession): A SparkSession object for creating connections to Spark.
        DB_USER (str): The username for the PostgreSQL database.
        DB_IP (str): The IP address for the PostgreSQL database.
        DB_PASSWORD (str): The password for the PostgreSQL database.

    Methods:
        __init__(): Initialize the PostgreDB object and establish a connection to the database.
        validate_connection(table_name: str) -> bool: Validate the connection to the database by loading the given table.
    """

    def __init__(self):
        """
        Initialize the PostgreDB object and establish a connection to the database.
        """
        load_dotenv()
        init(autoreset=True)
        try:
            self.DB_USER = os.getenv('DB_USER')
            self.DB_IP = os.getenv('DB_IP')
            self.DB_PASSWORD = os.getenv('DB_PASSWORD')

            self.spark = (
                SparkSession.builder
                .appName('PostgreSQL Connection')
                .config("spark.driver.memory", "2g")
                .getOrCreate()
            )
            self.spark.sparkContext.setLogLevel('OFF')

            print(Fore.GREEN + f"SparkSession successfully created")
        except:
            print(Fore.RED + 'please check your database connection properties to the environment (env) file')
            exit()

    def validate_connection(self, table_name: str) -> bool:
        """
        Validate the connection to the PostgreSQL database by loading the given table.

        Args:
            table_name (str): The name of the table to validate the connection.

        Returns:
            bool: True if the connection is successful, False otherwise.

            This class connection on server
        """
        try:
            self.spark.read \
                .format('jdbc') \
                .option("url", f"jdbc:postgresql://{self.DB_IP}/tbot_test") \
                .option("dbtable", table_name) \
                .option("user", self.DB_USER) \
                .option("password", self.DB_PASSWORD) \
                .load()
            return True
        except:
            return False
