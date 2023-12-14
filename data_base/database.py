import os
from dotenv import load_dotenv
from colorama import init, Fore
from pyspark.sql import SparkSession


class PostgreDB:
    def __init__(self):
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
