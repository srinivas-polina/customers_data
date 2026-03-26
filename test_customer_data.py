# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %run /Workspace/Users/polinasrinivas2022@gmail.com/customers_data/customer_data

# COMMAND ----------

import re
from pyspark.sql.functions import col, countDistinct

#defining smaller row count for testing instead of using the 1000000 row DataFrame
test_num_records = 1000

test_data = []

#generating only the required number of rows for unit testing
for i in range(test_num_records):
    first_name, last_name, email = generate_email()
    test_data.append((i, first_name, last_name, email))

#creating a smaller DataFrame using the same schema
test_df = spark.createDataFrame(test_data, schema)

frac_value = random.uniform(0.02, 0.2)
test_duplicate_data = test_df.sample(withReplacement=False, fraction=frac_value)

test_df = test_df.union(test_duplicate_data)

#validating generate_name and generate_email functions
first_name, last_name = generate_name()
assert first_name != "", "generate_name returned empty first_name"
assert last_name != "", "generate_name returned empty last_name"
assert first_name is not None, "generate_name returned null first_name"
assert last_name is not None, "generate_name returned null last_name"
assert isinstance(first_name, str), "generate_name first_name is not string"
assert isinstance(last_name, str), "generate_name last_name is not string"
print("generate_name function test passed")

# validating generate_email function output
first_name, last_name, email = generate_email()
assert first_name is not None, "generate_email returned null first_name"
assert last_name is not None, "generate_email returned null last_name"
assert email is not None, "generate_email returned null email"
assert last_name != "", "generate_email returned empty last_name"
assert email != "", "generate_email returned empty email"
email_pattern = r"^[a-z0-9]+@(gmail\.com|yahoo\.com|icloud\.com|outlook\.com)$"
assert re.match(email_pattern, email) is not None, f"generate_email returned invalid email format: {email}"
print("generate_email function test passed")


#vadilating test_df
assert "first_name" in test_df.columns, "first_name column is missing"
assert "last_name" in test_df.columns, "last_name column is missing"
assert "email" in test_df.columns, "email column is missing"
assert "customer_id" in test_df.columns, "customer_id column is missing"
assert test_df.columns == ["customer_id", "first_name", "last_name", "email"], "Column structure is incorrect"
print("df_test Schema validation passed")


total_test_records = test_df.count()
test_unique_records = test_df.select(countDistinct("email")).collect()[0][0]
test_duplicate_records = total_test_records - test_unique_records
test_unique_percentage = (test_unique_records / total_test_records) * 100
test_duplicate_percentage = (test_duplicate_records / total_test_records) * 100

print("\nDuplicate percentage used:", (round(frac_value, 2))*100,"%")
print("\nTotal test records:", total_test_records)
print("Test Unique records:", test_unique_records)
print("Test Unique percentage:", round(test_unique_percentage, 2), "%")
print("Test Duplicate percentage:", round(test_duplicate_percentage, 2), "%")
print("\nNumber of duplicated emails test:", test_duplicate_records)
