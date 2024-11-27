import sqlite3
from getpass import getpass

DB_NAME = 'orders.db'

# Підключення до бази даних
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


# Створення таблиць
def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        phone TEXT,
                        address TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        description TEXT,
                        price REAL,
                        stock INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER,
                        total_price REAL,
                        status TEXT DEFAULT 'Pending',
                        created_at TEXT,
                        FOREIGN KEY(client_id) REFERENCES clients(id))''')
    conn.commit()


# Реєстрація користувача
def register():
    username = input("Enter new username: ")
    password = getpass("Enter new password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")


# Вхід користувача
def login():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return True
    print("Invalid credentials!")
    return False


# Функції для управління клієнтами
def add_client():
    name = input("Client Name: ")
    email = input("Client Email: ")
    phone = input("Client Phone: ")
    address = input("Client Address: ")
    cursor.execute("INSERT INTO clients (name, email, phone, address) VALUES (?, ?, ?, ?)",
                   (name, email, phone, address))
    conn.commit()
    print("Client added successfully!")


def list_clients():
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    for client in clients:
        print(f"ID: {client[0]}, Name: {client[1]}, Email: {client[2]}, Phone: {client[3]}, Address: {client[4]}")


# Функції для управління товарами
def add_product():
    name = input("Product Name: ")
    description = input("Product Description: ")
    price = float(input("Product Price: "))
    stock = int(input("Product Stock: "))
    cursor.execute("INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
                   (name, description, price, stock))
    conn.commit()
    print("Product added successfully!")


def list_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[3]}, Stock: {product[4]}")


# Функції для управління замовленнями
def create_order():
    list_clients()
    client_id = int(input("Enter Client ID: "))
    total_price = float(input("Enter Total Price: "))
    cursor.execute(
        "INSERT INTO orders (client_id, total_price, status, created_at) VALUES (?, ?, 'Pending', datetime('now'))",
        (client_id, total_price))
    conn.commit()
    print("Order created successfully!")


def list_orders():
    cursor.execute(
        "SELECT orders.id, clients.name, orders.total_price, orders.status FROM orders JOIN clients ON orders.client_id = clients.id")
    orders = cursor.fetchall()
    for order in orders:
        print(f"Order ID: {order[0]}, Client: {order[1]}, Total Price: {order[2]}, Status: {order[3]}")


# Головне меню
def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            if login():
                user_menu()
        elif choice == '0':
            break
        else:
            print("Invalid option, try again.")


# Меню після входу користувача
def user_menu():
    while True:
        print("\n--- User Menu ---")
        print("1. Manage Clients")
        print("2. Manage Products")
        print("3. Manage Orders")
        print("0. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            client_menu()
        elif choice == '2':
            product_menu()
        elif choice == '3':
            order_menu()
        elif choice == '0':
            break
        else:
            print("Invalid option, try again.")


# Меню управління клієнтами
def client_menu():
    while True:
        print("\n--- Client Menu ---")
        print("1. Add Client")
        print("2. List Clients")
        print("0. Back")
        choice = input("Select an option: ")

        if choice == '1':
            add_client()
        elif choice == '2':
            list_clients()
        elif choice == '0':
            break
        else:
            print("Invalid option, try again.")


# Меню управління товарами
def product_menu():
    while True:
        print("\n--- Product Menu ---")
        print("1. Add Product")
        print("2. List Products")
        print("0. Back")
        choice = input("Select an option: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            list_products()
        elif choice == '0':
            break
        else:
            print("Invalid option, try again.")


# Меню управління замовленнями
def order_menu():
    while True:
        print("\n--- Order Menu ---")
        print("1. Create Order")
        print("2. List Orders")
        print("0. Back")
        choice = input("Select an option: ")

        if choice == '1':
            create_order()
        elif choice == '2':
            list_orders()
        elif choice == '0':
            break
        else:
            print("Invalid option, try again.")


def seed_data():
    # Додавання тестового користувача
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'password123')")

    # Додавання клієнтів
    cursor.execute(
        "INSERT OR IGNORE INTO clients (name, email, phone, address) VALUES ('John Doe', 'john@example.com', '+123456789', '123 Main St')")
    cursor.execute(
        "INSERT OR IGNORE INTO clients (name, email, phone, address) VALUES ('Jane Smith', 'jane@example.com', '+987654321', '456 Oak Ave')")

    # Додавання товарів
    cursor.execute(
        "INSERT OR IGNORE INTO products (name, description, price, stock) VALUES ('Laptop', 'Powerful laptop with 16GB RAM', 1200.00, 10)")
    cursor.execute(
        "INSERT OR IGNORE INTO products (name, description, price, stock) VALUES ('Smartphone', 'Latest model smartphone', 800.00, 15)")
    cursor.execute(
        "INSERT OR IGNORE INTO products (name, description, price, stock) VALUES ('Headphones', 'Noise-cancelling headphones', 150.00, 25)")

    # Додавання замовлень
    cursor.execute(
        "INSERT OR IGNORE INTO orders (client_id, total_price, status, created_at) VALUES (1, 1200.00, 'Pending', datetime('now'))")
    cursor.execute(
        "INSERT OR IGNORE INTO orders (client_id, total_price, status, created_at) VALUES (2, 800.00, 'Completed', datetime('now'))")

    conn.commit()
    print("Demo data added successfully!")

if __name__ == '__main__':
    create_tables()
    seed_data()
    main_menu()
    conn.close()
