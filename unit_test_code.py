
import sys

import unittest

import logging
from pyspark.sql import SparkSession
from customer_data import CustomerDataGenerator


# Configure where to save logs and what level to show
logging.basicConfig(
    level=logging.INFO,
    format='line %(lineno)d - %(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_app.log", mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

TEST_COUNT = 100

class TestCustomerDataGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("---Initializing Spark ---")
        cls.spark = SparkSession.builder.master("local").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")

    def setUp(self):
        logger.info(f"Running: {self._testMethodName}")
        self.generator = CustomerDataGenerator()
        self.df = self.generator.generate_customer_data(self.spark, TEST_COUNT)

    def test_generate_email(self):
        logger.info("Checking first_name, last_name, email...")
        first_name, last_name, email = self.generator.generate_email()

        self.assertIsInstance(first_name, str)
        self.assertIsInstance(last_name, str)
        self.assertIsInstance(email, str)

        self.assertTrue(len(first_name) > 0)
        self.assertTrue(len(last_name) > 0)
        self.assertTrue(len(email) > 0)
        self.assertIn("@", email)
        self.assertTrue(
            email.endswith("gmail.com") or
            email.endswith("yahoo.com") or
            email.endswith("icloud.com") or
            email.endswith("outlook.com"))
        local_part = email.split("@")[0]
        self.assertTrue(local_part[-3:].isdigit())
        self.assertFalse(local_part[-4].isdigit())

   #
    def test_generate_customer_data(self):
        logger.info("Verifying DataFrame structure...")
        self.assertEqual(self.df.count(), TEST_COUNT)
        self.assertListEqual(
            self.df.columns,
            ["first_name", "last_name", "email"]
        )

    def test_duplication_properties(self):
        logger.info("Verifying duplication logic")
        self.assertGreaterEqual(self.generator.frac_value, 0.02)
        self.assertLessEqual(self.generator.frac_value, 0.20)

        total_records = self.generator.original_unique_count + self.generator.duplicate_count
        self.assertEqual(total_records, TEST_COUNT)

        unique_count = self.df.distinct().count()
        actual_duplicates = TEST_COUNT - unique_count
        self.assertEqual(actual_duplicates, self.generator.duplicate_count)

    @classmethod
    def tearDownClass(cls):
        logger.info("--- Stopping Spark ---")
        cls.spark.stop()




#running tests
if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            TEST_COUNT = int(sys.argv.pop())
            logger.info(f"Custom count detected: Testing with {TEST_COUNT} records.")
        except ValueError:
            logger.error(f"Invalid input. Using default: {TEST_COUNT}")
    
    unittest.main()