import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent / "database" / "business.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def search_customer(name: str):
    """Search customer by name."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, phone, city
        FROM customers
        WHERE name LIKE ?
    """, (f"%{name}%",))

    results = cursor.fetchall()
    connection.close()

    if not results:
        return "No customer found."

    customers = []

    for row in results:
        customers.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "city": row[4]
        })

    return customers


def search_product(name: str):
    """Search product by name."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, category, price, stock
        FROM products
        WHERE name LIKE ?
    """, (f"%{name}%",))

    results = cursor.fetchall()
    connection.close()

    if not results:
        return "No product found."

    products = []

    for row in results:
        products.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "price": row[3],
            "stock": row[4]
        })

    return products


def get_order(order_id: int):
    """Get order details."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            o.id,
            c.name,
            p.name,
            o.quantity,
            o.total_amount,
            o.status,
            o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        JOIN products p ON o.product_id = p.id
        WHERE o.id = ?
    """, (order_id,))

    result = cursor.fetchone()
    connection.close()

    if not result:
        return "Order not found."

    return {
        "order_id": result[0],
        "customer": result[1],
        "product": result[2],
        "quantity": result[3],
        "total_amount": result[4],
        "status": result[5],
        "order_date": result[6]
    }


def check_stock(product_name: str):
    """Check product stock."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, stock
        FROM products
        WHERE name LIKE ?
    """, (f"%{product_name}%",))

    results = cursor.fetchall()
    connection.close()

    if not results:
        return "Product not found."

    return [
        {
            "product": row[0],
            "stock": row[1]
        }
        for row in results
    ]


def get_sales_report():
    """Generate sales report."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(total_amount),
            AVG(total_amount)
        FROM orders
    """)

    result = cursor.fetchone()
    connection.close()

    return {
        "total_orders": result[0] or 0,
        "total_revenue": result[1] or 0,
        "average_order_value": result[2] or 0
    }


def cancel_order(order_id: int):
    """Cancel an order."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status
        FROM orders
        WHERE id = ?
    """, (order_id,))

    result = cursor.fetchone()

    if not result:
        connection.close()
        return "Order not found."

    status = result[0]

    if status == "Delivered":
        connection.close()
        return "Delivered orders cannot be cancelled."

    if status == "Cancelled":
        connection.close()
        return "Order is already cancelled."

    cursor.execute("""
        UPDATE orders
        SET status = 'Cancelled'
        WHERE id = ?
    """, (order_id,))

    connection.commit()
    connection.close()

    return f"Order {order_id} cancelled successfully."


def create_return(order_id: int):
    """Create a return request."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status
        FROM orders
        WHERE id = ?
    """, (order_id,))

    result = cursor.fetchone()

    if not result:
        connection.close()
        return "Order not found."

    status = result[0]

    if status != "Delivered":
        connection.close()
        return "Only delivered orders can be returned."

    connection.close()

    return f"Return request created for order {order_id}."