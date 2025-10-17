# database.py
import mysql.connector
from config import DB_CONFIG

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def create_tables():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT,
            username VARCHAR(255),
            product VARCHAR(255),
            price INT,
            payment_method VARCHAR(50),
            status VARCHAR(50) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()

def add_order(user_id, username, product, price, payment_method):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO orders (user_id, username, product, price, payment_method)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, username, product, price, payment_method))
    db.commit()
    db.close()

def get_orders():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    result = cursor.fetchall()
    db.close()
    return result

def update_status(order_id, status):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
    db.commit()
    db.close()
