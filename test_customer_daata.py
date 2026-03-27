# Databricks notebook source
# MAGIC %run /Workspace/Users/polinasrinivas2022@gmail.com/customers_data/customer_data_creating_functions

# COMMAND ----------



#generating 1000 customer records
df = generate_customer_data(spark, 1000)

#duplicates to the generated DataFrame
df = add_duplicates(df)

#printing summary metrics
print_summary(df)

#displaying sample records
print("\nSample records:")
df.show(10)
