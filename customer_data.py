# Databricks notebook source
spark


from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col, count, countDistinct



# importing Faker to generate fake names
!pip install Faker
from faker import Faker
import random


fake = Faker()

num_records = 1000000

#creating empty list to store customer data
data = []

#creating a function to generate first name and last name
def generate_name():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name

# creating a function to generate email
def generate_email():
    numbers = "0123456789"
    domains = ["gmail.com", "yahoo.com", "icloud.com", "outlook.com"]
    first_name, last_name = generate_name()
    number = ""
    
    for i in range(3):
        # adding one random digit each time
        number += random.choice(numbers)
    
    # selecting one random domain
    domain = random.choice(domains)
    
    # building email using first name, last name, number, and domain
    email = first_name.lower() + last_name.lower() + number + "@" + domain
    
    #returning first name, last name, and email
    return first_name, last_name, email

# generating customer records
for i in range(num_records):
    # generating customer details
    first_name, last_name, email = generate_email()
    # creating one customer row as tuple
    customer = (i, first_name, last_name, email)
    # I am adding row into list
    data.append(customer)


#defining schema for Spark DataFrame
schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True)
])


#creating Spark DataFrame from Python list
df = spark.createDataFrame(data, schema)

# random duplicate fraction between 2% and 20%
frac_value = random.uniform(0.02, 0.2)
# taking a random sample from existing DataFrame to create duplicates
duplicate_data = df.sample(withReplacement=False, fraction=frac_value)
#printing duplicate fraction used
print("\nDuplicate fraction used:", round(frac_value, 2))

#adding duplicate rows to original DataFrame
df = df.union(duplicate_data)

total_records = df.count()
unique_records = df.select(countDistinct("email")).collect()[0][0]
duplicate_records = total_records - unique_records
unique_percentage = (unique_records / total_records) * 100
duplicate_percentage = (duplicate_records / total_records) * 100

print("\nTotal records:", total_records)
print("Unique records:", unique_records)
print("Unique percentage:", round(unique_percentage, 2), "%")
print("Duplicate percentage:", round(duplicate_percentage, 2), "%")
print("\nNumber of duplicated emails:", duplicate_records)


# COMMAND ----------

df.show(10)