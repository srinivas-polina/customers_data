# Customer Data Generator & Duplicate Analysis

This project generates synthetic customer data using Python and analyzes duplicate records and data quality metrics.

It uses the Faker library to generate realistic names and emails, and includes logic to simulate duplicate data and calculate key metrics.

---

## 🚀 Features

- Generate random customer records
- Create realistic emails using Faker
- Introduce duplicate records randomly
- Calculate:
  - Total records
  - Unique records (based on email)
  - Duplicate records
  - Unique percentage
  - Duplicate percentage
- Display summary statistics

---

## 🛠️ Tech Stack

- Python 3.13
- Faker (for generating fake data)
- Built-in Python libraries (`random`)

## Project Structure

```text
customers_data/
├── customer_data.py
├── test_customer_data.py
├── requirements.txt
├── README.md
└── .gitignore