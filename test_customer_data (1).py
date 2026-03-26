# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %run /Workspace/Users/polinasrinivas2022@gmail.com/customer_daata

# COMMAND ----------

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
print("\nDuplicate percentage used:", (round(frac_value, 2))*100,"%")

test_df = test_df.union(test_duplicate_data)

total_test_records = test_df.count()
test_unique_records = test_df.select(countDistinct("email")).collect()[0][0]
test_duplicate_records = total_test_records - test_unique_records
test_unique_percentage = (test_unique_records / total_test_records) * 100
test_duplicate_percentage = (test_duplicate_records / total_test_records) * 100

print("\nTotal test records:", total_test_records)
print("Test Unique records:", test_unique_records)
print("Test Unique percentage:", round(test_unique_percentage, 2), "%")
print("Test Duplicate percentage:", round(test_duplicate_percentage, 2), "%")
print("\nNumber of duplicated emails test:", test_duplicate_records)

