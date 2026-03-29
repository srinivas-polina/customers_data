# I am importing unittest module
import unittest

# I am importing functions from my main file
from customer_data import (
    generate_name,
    generate_email,
    generate_customer_data,
    add_duplicates,
    total_count,
    distinct_count,
    total_duplicates,
    unique_percentage,
    duplicate_percentage
)

# I am creating test class
class TestCustomerData(unittest.TestCase):

    # I am testing generate_name function
    def test_generate_name(self):
        first_name, last_name = generate_name()

        self.assertIsInstance(first_name, str)
        self.assertIsInstance(last_name, str)

        self.assertTrue(len(first_name) > 0)
        self.assertTrue(len(last_name) > 0)

   #testing generate_email function (clean version)
    def test_generate_email(self):
        #calling the function
        first_name, last_name, email = generate_email()
        #checking email contains first and last name
        self.assertIn(first_name.lower(), email)
        self.assertIn(last_name.lower(), email)
        #checking email contains @
        self.assertIn("@", email)
        #checking email ends with valid domain
        self.assertTrue(
            email.endswith("gmail.com") or
            email.endswith("yahoo.com") or
            email.endswith("icloud.com") or
            email.endswith("outlook.com")
        )
        #checking email is not empty
        self.assertTrue(len(email) > 0)
        #checking local part ends with exactly 3 digits
        local_part = email.split("@")[0]
        self.assertTrue(local_part[-3:].isdigit())
        self.assertFalse(local_part[-4].isdigit())

    def test_generate_customer_data(self):
            data = generate_customer_data(10)
            self.assertEqual(len(data), 10)
            self.assertIsInstance(data, list)


    # I am testing add_duplicates function
    def test_add_duplicates(self):
        data = generate_customer_data(10)

        new_data = add_duplicates(data)

        # After adding duplicates, count should increase
        self.assertTrue(len(new_data) >= len(data))

    # I am testing total_count function
    def test_total_count(self):
        data = generate_customer_data(5)
        self.assertEqual(total_count(data), 5)

    # I am testing distinct_count function
    def test_distinct_count(self):
        data = generate_customer_data(5)
        # Initially all emails should be unique
        self.assertEqual(distinct_count(data), 5)

    #testing total_duplicates function
    def test_total_duplicates(self):
        data = generate_customer_data(20)
        new_data = add_duplicates(data)

        self.assertTrue(total_duplicates(new_data) >= 0)
    
    #testing unique_percentage function
    def test_unique_percentage(self):
        data = generate_customer_data(20)
        new_data = add_duplicates(data)

        self.assertTrue(unique_percentage(new_data) >= 0)
        self.assertTrue(unique_percentage(new_data) <= 100)

        #testing duplicate_percentage function
    def test_duplicate_percentage(self):
        data = generate_customer_data(20)
        new_data = add_duplicates(data)

        self.assertTrue(duplicate_percentage(new_data) >= 0)
        self.assertTrue(duplicate_percentage(new_data) <= 100)
    
    # testing percentage total
    def test_percentage_total(self):
        data = generate_customer_data(20)
        new_data = add_duplicates(data)

        total_pct = unique_percentage(new_data) + duplicate_percentage(new_data)

        self.assertAlmostEqual(total_pct, 100.0)

# I am running tests
if __name__ == "__main__":
    unittest.main()