import psycopg2
import csv
import sys
import os

DB_CONFIG = {
    "dbname": "phonebook_db",
    "user": "postgres",
    "password": "badapple123",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def setup_database():
    query = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        phone_number VARCHAR(20) UNIQUE NOT NULL
    );
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def import_csv(filename):
    # This line finds the folder where main.py is located
    base_path = os.path.dirname(os.path.abspath(__file__))
    # This joins that folder path with your filename
    full_path = os.path.join(base_path, filename)

    print(f"Looking for file at: {full_path}")

    if not os.path.exists(full_path):
        print(f"Error: The file '{filename}' was not found in {base_path}")
        return

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        with open(full_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
                """, (row['first_name'], row['last_name'], row['phone_number']))
        conn.commit()
        print("CSV imported successfully!")
    except Exception as e:
        print(f"Error reading CSV: {e}")
    finally:
        cur.close()
        conn.close()

def add_contact():
    fname = input("First Name: ")
    lname = input("Last Name: ")
    phone = input("Phone: ")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)", (fname, lname, phone))
        conn.commit()
        print("Contact added!")
    except Exception as e:
        print(f"Error: {e}")
    cur.close()
    conn.close()

def update_contact():
    phone = input("Enter the Phone Number of the contact to update: ")
    new_name = input("Enter new First Name (leave blank to skip): ")
    new_phone = input("Enter new Phone (leave blank to skip): ")
    
    conn = get_db_connection()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE contacts SET first_name = %s WHERE phone_number = %s", (new_name, phone))
    if new_phone:
        cur.execute("UPDATE contacts SET phone_number = %s WHERE phone_number = %s", (new_phone, phone))
    conn.commit()
    print("Update complete.")
    cur.close()
    conn.close()

def search_contacts():
    term = input("Search by name or phone prefix: ")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE first_name ILIKE %s OR phone_number LIKE %s", (f'%{term}%', f'{term}%'))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def delete_contact():
    identifier = input("Enter Name or Phone to delete: ")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE first_name = %s OR phone_number = %s", (identifier, identifier))
    conn.commit()
    print("Deleted.")
    cur.close()
    conn.close()

def main():
    setup_database()
    while True:
        print("\n--- PhoneBook ---")
        print("1. Import CSV\n2. Add Contact\n3. Update Contact\n4. Search\n5. Delete\n6. Exit")
        choice = input("Select: ")
        if choice == '1': import_csv('contacts.csv')
        elif choice == '2': add_contact()
        elif choice == '3': update_contact()
        elif choice == '4': search_contacts()
        elif choice == '5': delete_contact()
        elif choice == '6': break

if __name__ == "__main__":
    main()