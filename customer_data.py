
import sys
import random
import logging
import time


from faker import Faker
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import rand


logger = logging.getLogger(__name__)


class CustomerDataGenerator:
    def __init__(self):
        self.fake = Faker()
        logger.info("CustomerDataGenerator initialized with Faker.")

    def generate_email(self):
        domains = ["gmail.com", "yahoo.com", "icloud.com", "outlook.com"]
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        number = "".join(random.choices("0123456789", k=3))
        domain = random.choice(domains)
        email = f"{first_name.lower()}{last_name.lower()}{number}@{domain}"
        return first_name, last_name, email
    

    def generate_customer_data(self, spark, num_records):
        logger.info(f"Starting data generation for {num_records} records.")
        self.frac_value = random.uniform(0.02, 0.20)
        self.duplicate_count = int(num_records * self.frac_value)
        self.original_unique_count = num_records - self.duplicate_count
        logger.info(f"Data generating completed: {self.original_unique_count} unique, {self.duplicate_count} duplicates.")

        data = []
        for i in range(self.original_unique_count):
            data.append(self.generate_email())
            if (i + 1) % 500 == 0:
                logger.debug(f"Generated {i + 1} unique records so far...")

        schema = StructType([
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("email", StringType(), True)
        ])

        logger.info("Creating Spark DataFrame...")
        df = spark.createDataFrame(data, schema)

        duplicate_rows = df.orderBy(rand()).limit(self.duplicate_count)
        df = df.unionByName(duplicate_rows)

        logger.info("Data generation and duplication successful.")
        return df

    def print_summary(self, df):
        logger.info("Calculating summary statistics...")
        total = df.count()

        # Fixed 'frist' typo to 'first' below
        total_first_names = df.select("first_name").count()
        unique_first_names = df.select("first_name").distinct().count()
        duplicate_first_names = total_first_names - unique_first_names

        total_last_names = df.select("last_name").count()
        unique_last_names = df.select("last_name").distinct().count()
        duplicate_last_names = total_last_names - unique_last_names

        total_emails = df.select("email").count()
        unique_emails = df.select("email").distinct().count()
        duplicate_emails = total_emails - unique_emails
        
        unique_rows = df.select("first_name", "last_name", "email").distinct().count()
        duplicate_rows = total - unique_rows

        unique_pct = (unique_rows / total) * 100
        duplicate_pct = (duplicate_rows / total) * 100

        print("\nDuplicate fraction selected:", round(self.frac_value, 4))
        print("Duplicate percentage selected:", round(self.frac_value * 100, 2), "%")
        print("Duplicate rows created:", self.duplicate_count)
        print("Original unique rows generated:", self.original_unique_count)

        print("\nTotal records:", total)
        print("\ntotal first names:", total_first_names)
        print("Unique first names:", unique_first_names)
        print("Duplicate first names:",  duplicate_first_names)

        print("\ntotal last names:", total_last_names)
        print("Unique last names:", unique_last_names)
        print("Duplicate last names:",  duplicate_last_names)

        print("\nUnique emails:", unique_emails)
        print("Duplicate emails:",  duplicate_emails)
        print("\nUnique percentage:", round(unique_pct, 2), "%")
        print("Duplicate rows percentage:", round(duplicate_pct, 2), "%")
        logger.info("Summary printed to console.")

if __name__ == "__main__":
    # Configure where to save logs and what level to show
    logging.basicConfig(
        level=logging.INFO,
        format='line %(lineno)d - %(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"), # Writes to file
            logging.StreamHandler(sys.stdout) # Writes to terminal
        ]
    )
    
    start_time = time.perf_counter() #Record Start Time
    logger.info("Application started.")
    spark = SparkSession.builder.master("local[*]").appName("CustomerGenerator").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    if len(sys.argv) > 1:
        try:
            num_records = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid input: '{sys.argv[1]}' is not a number")
            sys.exit(1)
    else:
        logger.warning("No record count provided. Exiting program")
        spark.stop()
        sys.exit()

    generator = CustomerDataGenerator()
    df = generator.generate_customer_data(spark, num_records)
    generator.print_summary(df)
    df.show(10, truncate=False)
    
    logger.info("Stoping Spark Session")
    spark.stop()
    logger.info("Application finished sucessfully")
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    mins, secs = divmod(total_duration, 60)
    time_format = f"{int(mins):02d}:{int(secs):02d}"
    logger.info(f"Total Execution Time: {time_format} (MM:SS)")