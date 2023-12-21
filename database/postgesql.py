import os
from dotenv import load_dotenv
from colorama import init, Fore
from pyspark.sql import SparkSession, DataFrame


class PostgreDB:
    """
    A class for connecting to PostgreSQL database using PySpark.
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

        :param table_name: The name of the table to validate the connection.
        :type table_name: str
        :return: True if the connection is successful, False otherwise.
        :rtype: bool
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

    def get_table(self, table_name: str) -> DataFrame:
        """
        Retrieve a table from the PostgreSQL database and return it as a DataFrame.

        :param table_name: The name of the table to retrieve.
        :type table_name: str
        :return: The DataFrame containing the data from the specified table.
        :rtype: DataFrame
        """
        df = self.spark.read \
            .format('jdbc') \
            .option("url", f"jdbc:postgresql://{self.DB_IP}/tbot_test") \
            .option("dbtable", table_name) \
            .option("user", self.DB_USER) \
            .option("password", self.DB_PASSWORD) \
            .load()
        return df
