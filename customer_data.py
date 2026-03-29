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

    return data

#defining function to add duplicate records
def add_duplicates(data):
    frac_value = random.uniform(0.02, 0.2)
    num_duplicates = int(len(data) * frac_value)
    duplicate_data = random.sample(data, num_duplicates)
    data = data + duplicate_data
    return data

#-----METRICS----

def total_count(data):
    return len(data)

def distinct_count(data):
    emails = [record["email"] for record in data]
    unique_emails = set(emails)
    return len(unique_emails)

def total_duplicates(data):
    return total_count(data) - distinct_count(data)


def unique_percentage(data):
    total = total_count(data)
    unique = distinct_count(data)
    return (unique / total) * 100



def duplicate_percentage(data):
    total = total_count(data)
    duplicates = total_duplicates(data)
    return (duplicates / total) * 100


#function to print summary
def print_summary(data):
    
    total = total_count(data)
    unique = distinct_count(data)
    duplicates = total_duplicates(data)
    
    unique_pct = (unique / total) * 100
    duplicate_pct = (duplicates / total) * 100

    
    print("\nTotal records:", total)
    print("Unique records:", unique)
    print("Unique percentage:", round(unique_pct, 2), "%")
    print("Duplicate percentage:", round(duplicate_pct, 2), "%")
    print("\nNumber of duplicated emails:", duplicates)


# -------------------- MAIN TEST --------------------

if __name__ == "__main__":
    
    #generating customer data
    data = generate_customer_data(100)
    
    #adding duplicates
    data = add_duplicates(data)
    #printing summary
    print_summary(data)
    #converting list to DataFrame
    df = pd.DataFrame(data)
    #printing first few rows
    print(df.head(10))