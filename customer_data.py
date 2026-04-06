import logging
import sys
import random
from faker import Faker
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType

# SETUP LOGGING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
    )
logger = logging.getLogger(__name__)

class CustomerDataGenerator:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        # [FIX 1: Use self.schema and fix the StructField typo]
        self.schema = StructType([
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("email", StringType(), True)
        ])

    
    @staticmethod
    def generate_records(items):
        fake = Faker()
        # [FIX 3: Move random logic INSIDE the loop so every email is different]
        domains = ["gmail.com", "yahoo.com", "icloud.com", "outlook.com"]
        for _ in items:
            first_name = fake.first_name()
            last_name = fake.last_name()
            number = "".join(random.choices("0123456789", k=3))
            domain = random.choice(domains)
            # Fix: correctly format the email string
            email = f"{first_name.lower()}.{last_name.lower()}{number}@{domain}"
            yield (first_name, last_name, email)

    
    def create_dataset(self, num_records):
        frac_value = random.uniform(0.02, 0.20)
        duplicate_count = int(num_records * frac_value)
        original_unique_count = num_records - duplicate_count
        
        logger.info(f"Target Records to generate: {num_records} ")

        
        data_rdd = self.spark.sparkContext.parallelize(range(original_unique_count), 20)
        unique_df = self.spark.createDataFrame(data_rdd.mapPartitions(self.generate_records), self.schema)

        unique_df.cache()

        # Create duplicates by sampling
        duplicate_rows = unique_df.orderBy(F.rand()).limit(duplicate_count)

        final_df = unique_df.union(duplicate_rows)
        return final_df

    def analyze(self, df):
        logger.info("Starting Analysis...")
        df.cache()
        
        total = df.count()
        overall_unique = df.distinct().count()
        overall_duplicates = total - overall_unique
        
        # [FIX 6: Use 'first_name' to match your schema]
        unique_first_names = df.select("first_name").distinct().count()
        unique_last_names = df.select("last_name").distinct().count()
        unique_emails = df.select("email").distinct().count()

        logger.info("Analysis Completed")

        print(f"\nOverall Total : {total:} \nOverall Unique : {overall_unique:} \nOverall Duplicates : {overall_duplicates}")
        print(f"\nUnique First Names: {unique_first_names:} \nUnique Last Names: {unique_last_names:} \nUnique Emails: {unique_emails:}\n")

def main():
    # Standard Spark Startup
    spark = SparkSession.builder.appName("CustomerData").getOrCreate()
    spark.sparkContext.setLogLevel("WARN") # Keeps the console clean

    
    if len(sys.argv) < 2:
        logger.error("Usage: python script.py <num_records>")
        sys.exit(1)
    try:
        num_records = int(sys.argv[1])
    except ValueError:
        logger.error(f"Invalid input: '{sys.argv[1]}' is not a number")
        sys.exit(1)

    customers_data = CustomerDataGenerator(spark)
    customers_df = customers_data.create_dataset(num_records)
    customers_data.analyze(customers_df)

    spark.stop()

if __name__ == "__main__":
    main()