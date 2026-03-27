# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "4"
# ///
spark


from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col, count, countDistinct

# importing Faker to generate fake names
!pip install Faker
from faker import Faker
import random


fake = Faker()

# generating names
def generate_name():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name


# generating emails
def generate_email():
    numbers = "0123456789"
    domains = ["gmail.com", "yahoo.com", "icloud.com", "outlook.com"]
    
    first_name, last_name = generate_name()
    
    number = ""
    for i in range(3):
        number += random.choice(numbers)
    
    domain = random.choice(domains)
    email = first_name.lower() + last_name.lower() + number + "@" + domain
    return first_name, last_name, email

# I am creating customer data based on input size
def generate_customer_data(spark, num_records):
    
    data = []
    schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True)])

    for i in range(num_records):
        first_name, last_name, email = generate_email()
        data.append((i, first_name, last_name, email))
    
    df = spark.createDataFrame(data, schema)
    return df


spark


from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col, count, countDistinct

# Importing Faker to generate fake names
# !pip install Fake
from faker import Faker
import random


fake = Faker()


#creating empty list to store customer data
data = []

# generating names
def generate_name():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name


# generating emails
def generate_email():
    numbers = "0123456789"
    domains = ["gmail.com", "yahoo.com", "icloud.com", "outlook.com"]
    
    first_name, last_name = generate_name()
    
    number = ""
    for i in range(3):
        number += random.choice(numbers)
    
    domain = random.choice(domains)
    email = first_name.lower() + last_name.lower() + number + "@" + domain
    return first_name, last_name, email

# I am creating customer data based on input size
def generate_customer_data(spark, num_records):
    
    data = []
    schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True)])

    for i in range(num_records):
        first_name, last_name, email = generate_email()
        data.append((i, first_name, last_name, email))
    
    df = spark.createDataFrame(data, schema)
    
    return df


def add_duplicates(df):
    frac_value = random.uniform(0.02, 0.2)
    duplicate_data = df.sample(withReplacement=False, fraction=frac_value)
    df = df.union(duplicate_data)
    print("\nDuplicate fraction used:", round(frac_value, 2))
    return df

# I am adding duplicates (with optional fraction)
def add_duplicates(df, fraction=None):
    
    if fraction is None:
        fraction = random.uniform(0.02, 0.2)
    duplicate_data = df.sample(withReplacement=False, fraction=fraction)
    df = df.union(duplicate_data)
    return df

def total_count(df):
    total_count = df.count()
    return total_count
def distinct_count(df):
    distinct_count = df.select(countDistinct("email")).collect()[0][0]
    return distinct_count
def total_duplicates(df):
    total_duplicates = total_count(df) - distinct_count(df)
    return total_duplicates
def unique_percentage(df):
    total = total_count(df)
    unique = distinct_count(df)
    percentage = (unique / total) * 100
    return percentage
def duplicate_percentage(df):
    total = total_count(df)
    duplicates = total_duplicates(df)
    percentage = (duplicates / total) * 100
    return percentage

def print_summary(df):
    total = total_count(df)
    unique = distinct_count(df)
    duplicates = total_duplicates(df)
    unique_pct = (unique / total) * 100
    duplicate_pct = (duplicates / total) * 100

    print("\nTotal records:", total)
    print("Unique records:", unique)
    print("Unique percentage:", round(unique_pct, 2), "%")
    print("Duplicate percentage:", round(duplicate_pct, 2), "%")
    print("\nNumber of duplicated emails:", duplicates)


