import sqlite3
import random
import string

# Connect to the database
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              website TEXT,
              username TEXT,
              password TEXT)''')

# Function to generate a random password
def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Function to add a password to the database
def add_password(website, username, password):
    c.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)',
              (website, username, password))
    conn.commit()

# Function to get a password from the database
def get_password(website):
    c.execute('SELECT password FROM passwords WHERE website = ?', (website,))
    password = c.fetchone()
    if password:
        return password[0]
    else:
        return None

# Menu function
def menu():
    print("1. Generate a password for a new website")
    print("2. Get a password for an existing website")
    print("3. Quit")
    choice = input("Enter your choice: ")
    if choice == "1":
        website = input("Enter the website: ")
        username = input("Enter the username: ")
        password = generate_password()
        print("Generated password:", password)
        add_password(website, username, password)
    elif choice == "2":
        website = input("Enter the website: ")
        password = get_password(website)
        if password:
            print("Password:", password)
        else:
            print("No password found for", website)
    elif choice == "3":
        print("Goodbye!")
        conn.close()
        quit()
    else:
        print("Invalid choice, try again.")
    menu()

# Start the program
menu()