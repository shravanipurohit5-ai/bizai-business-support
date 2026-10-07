import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "business.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            city TEXT
        )
    """)

    # Products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    """)

    # Orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total_amount REAL,
            status TEXT,
            order_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # Sample customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]

    if customer_count == 0:
        customers = [
            ("Rahul Sharma", "rahul@gmail.com", "9876543210", "Hyderabad"),
            ("Priya Patil", "priya@gmail.com", "9876543211", "Pune"),
            ("Amit Kumar", "amit@gmail.com", "9876543212", "Mumbai"),
            ("Sneha Joshi", "sneha@gmail.com", "9876543213", "Bangalore")
        ]

        cursor.executemany("""
            INSERT INTO customers
            (name, email, phone, city)
            VALUES (?, ?, ?, ?)
        """, customers)

    # Sample products
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    if product_count == 0:
        products = [
            ("AI Laptop", "Electronics", 65000, 15),
            ("Wireless Headphones", "Electronics", 2500, 50),
            ("Smart Watch", "Electronics", 4500, 25),
            ("Office Chair", "Furniture", 8500, 10),
            ("Mechanical Keyboard", "Accessories", 3500, 30)
        ]

        cursor.executemany("""
            INSERT INTO products
            (name, category, price, stock)
            VALUES (?, ?, ?, ?)
        """, products)

    # Sample orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    if order_count == 0:
        orders = [
            (1, 1, 1, 65000, "Delivered", "2026-09-20"),
            (2, 2, 2, 5000, "Shipped", "2026-09-25"),
            (3, 3, 3, 4500, "Delivered", "2026-09-28"),
            (4, 4, 4, 8500, "Processing", "2026-10-01"),
            (1, 5, 2, 7000, "Delivered", "2026-10-02")
        ]

        cursor.executemany("""
            INSERT INTO orders
            (customer_id, product_id, quantity, total_amount, status, order_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, orders)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("✅ Business database created successfully!")