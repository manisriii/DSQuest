import sqlite3
import os

# Define the path to the `test_cases.sqlite` database in the `instance` folder
db_path = os.path.join('/Users/sandeepkumarrudhravaram/WorkSpace/SupportWrok/Manisree/DSQuest/instance', 'test_cases.sqlite')
print(db_path)
# Ensure the instance directory exists
os.makedirs('instance', exist_ok=True)

# Connect to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables as needed for setting up test cases
# This example includes `Person` and `Address` tables, similar to the example you provided earlier.

# Define a setup for test tables
def create_tables():
    # Create the Person table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            personId INTEGER PRIMARY KEY,
            lastName TEXT,
            firstName TEXT
        )
    ''')

    # Create the Address table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Address (
            addressId INTEGER PRIMARY KEY,
            personId INTEGER,
            city TEXT,
            state TEXT,
            FOREIGN KEY (personId) REFERENCES Person(personId)
        )
    ''')

    print("Tables created successfully in test_cases.sqlite.")

# Insert sample data for testing purposes (optional)
def insert_sample_data():
    # Insert data into Person table
    cursor.execute("INSERT INTO Person (personId, lastName, firstName) VALUES (1, 'Wang', 'Allen')")
    cursor.execute("INSERT INTO Person (personId, lastName, firstName) VALUES (2, 'Alice', 'Bob')")

    # Insert data into Address table
    cursor.execute("INSERT INTO Address (addressId, personId, city, state) VALUES (1, 2, 'New York City', 'New York')")
    cursor.execute("INSERT INTO Address (addressId, personId, city, state) VALUES (2, 3, 'Leetcode', 'California')")

    print("Sample data inserted into test_cases.sqlite.")

# Run the table creation and sample data insertion functions
create_tables()
insert_sample_data()

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database `test_cases.sqlite` has been created and initialized successfully.")
