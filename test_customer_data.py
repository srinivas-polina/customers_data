
import unittest
import logging


from pyspark.sql import SparkSession
from customer_data import CustomerDataGenerator

logger = logging.getLogger(__name__)

class TestCustomerDataGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.master("local[1]").appName("Unit_test").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")

    def setUp(self):
        self.generator = CustomerDataGenerator(self.spark)
        self.test_target_count = 100

    def test_schema_integrity(self):
        logger.info("-----Testing the Schema----")
        df = self.generator.create_dataset(self.test_target_count)
        expected_columns = ["first_name","last_name","email"]
        self.assertListEqual(df.columns, expected_columns)

    def test_exact_record_count(self):
        logger.info("-----Testing the Exact Record Count----")
        df = self.generator.create_dataset(self.test_target_count)
        actual_count = df.count()
        self.assertEqual(actual_count, self.test_target_count)

    def test_duplication_logic_triggers(self):
        logger.info("-----Checking the Duplication logic----")
        df = self.generator.create_dataset(self.test_target_count)

        total_count = df.count()
        unique_count = df.distinct().count()

        self.assertLess(unique_count, total_count)

    def test_email_formatting_rules(self):
        logger.info("-----Testing the Email Formating----")
        sample_records = list(CustomerDataGenerator.generate_records(range(10)))

        valid_domains = ["gmail.com", "yahoo.com", "icloud.com", "outlook.com"]

        for record in sample_records:
            first_name, last_name, email = record

            self.assertIn("@",email)
            actual_domain = email.split("@")[-1]

            self.assertIn(actual_domain, valid_domains)

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

if __name__ == "__main__":
    unittest.main()