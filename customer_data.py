# installing Faker (run this once in your environment, if not faker installed)
#pip install Faker
import pandas as pd
#importing Faker to generate fake names
from faker import Faker

#importing random for randomness
import random

#creating Faker object
fake = Faker()

# defining function to generate first and last name
def generate_name():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name

# defining function to generate email
def generate_email():
    domains = ["gmail.com", "yahoo.com", "icloud.com", "outlook.com"]
    first_name, last_name = generate_name()
    
    number = "".join(random.choices("0123456789", k=3))

    domain = random.choice(domains)
    email = first_name.lower() + last_name.lower() + number + "@" + domain
    return first_name, last_name, email

# defining function to generate customer data
def generate_customer_data(num_records):
    
    data = []

    for i in range(num_records):
        first_name, last_name, email = generate_email()
        
        record = {
            "customer_id": i,
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }
        
        data.append(record)
    df = pd.DataFrame(data)
    return df

#defining function to add duplicate records
def add_duplicates(df):
    frac_value = random.uniform(0.02, 0.2)
    num_duplicates = int(len(df) * frac_value)
    duplicate_rows = df.sample(n=num_duplicates, random_state=None)
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    return df

#-----METRICS----

def total_count(df):
    return len(df)

def distinct_count(df):
    return df["email"].nunique()

def total_duplicates(df):
    return total_count(df) - distinct_count(df)


def unique_percentage(df):
    total = total_count(df)
    unique = distinct_count(df)
    return (unique / total) * 100



def duplicate_percentage(df):
    total = total_count(df)
    duplicates = total_duplicates(df)
    return (duplicates / total) * 100


#function to print summary
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


# -------------------- MAIN TEST --------------------

# I am starting the main program
if __name__ == "__main__":
    # I am generating customer data as DataFrame directly
    df = generate_customer_data(100)
    # I am adding duplicates to the DataFrame
    df = add_duplicates(df)
    # I am printing summary of the DataFrame
    print_summary(df)
    # I am printing first 10 rows of the DataFrame
    print(df.head(10))