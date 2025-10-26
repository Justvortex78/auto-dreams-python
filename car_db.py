import pyodbc
from typing import List, Dict, Any

SERVER = 'ILYAS'
DATABASE = 'CarDealership'
USERNAME = 'sa'
PASSWORD = '11111'

def get_conn():
    conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    return pyodbc.connect(conn_str)

def get_all_cars() -> List[Dict[str, Any]]:
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CARS WHERE status = 'в наличии'")
            rows = cursor.fetchall()
            
            cars = []
            for row in rows:
                columns = [column[0] for column in cursor.description]
                cars.append(dict(zip(columns, row)))
            return cars
    except Exception as e:
        print(f"Ошибка при получении автомобилей: {e}")
        return []

def get_client_orders(client_id: int) -> List[Dict[str, Any]]:
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, c.brand, c.model, c.vin, emp.first_name + ' ' + emp.last_name as employee_name
                FROM ORDERS o
                JOIN CARS c ON o.car_id = c.id
                JOIN EMPLOYEES emp ON o.employee_id = emp.id
                WHERE o.client_id = ?
            """, (client_id,))
            
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                columns = [column[0] for column in cursor.description]
                orders.append(dict(zip(columns, row)))
            return orders
    except Exception as e:
        print(f"Ошибка при получении заказов: {e}")
        return []

def add_review(client_id: int, order_id: int, rating: int, comment: str):
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO REVIEWS (client_id, order_id, rating, comment, review_date) VALUES (?, ?, ?, ?, GETDATE())",
                (client_id, order_id, rating, comment)
            )
            conn.commit()
    except Exception as e:
        print(f"Ошибка при добавлении отзыва: {e}")
        raise

def get_client_reviews(client_id: int) -> List[Dict[str, Any]]:
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, c.brand, c.model 
                FROM REVIEWS r
                JOIN ORDERS o ON r.order_id = o.id
                JOIN CARS c ON o.car_id = c.id
                WHERE r.client_id = ?
                ORDER BY r.review_date DESC
            """, (client_id,))
            
            rows = cursor.fetchall()
            reviews = []
            for row in rows:
                columns = [column[0] for column in cursor.description]
                reviews.append(dict(zip(columns, row)))
            return reviews
    except Exception as e:
        print(f"Ошибка при получении отзывов: {e}")
        return []

def create_order(client_id: int, car_id: int):
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT TOP 1 id FROM EMPLOYEES ORDER BY NEWID()")
            employee = cursor.fetchone()
            employee_id = employee[0] if employee else 1
            
            cursor.execute("SELECT price FROM CARS WHERE id = ?", (car_id,))
            car = cursor.fetchone()
            price = car[0] if car else 0
            
            cursor.execute(
                "INSERT INTO ORDERS (client_id, car_id, employee_id, sale_date, final_price) VALUES (?, ?, ?, GETDATE(), ?)",
                (client_id, car_id, employee_id, price)
            )
            
            cursor.execute("UPDATE CARS SET status = 'продан' WHERE id = ?", (car_id,))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при создании заказа: {e}")
        raise

def get_or_create_client_for_user(user_id: int, username: str):
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM CLIENTS WHERE first_name = ?", (username,))
            client = cursor.fetchone()
            
            if client:
                return client[0]
            else:
                cursor.execute(
                    "INSERT INTO CLIENTS (first_name, last_name, phone) VALUES (?, ?, ?)",
                    (username, "User", "+7-000-000-00-00")
                )
                cursor.execute("SELECT SCOPE_IDENTITY()")
                new_client_id = cursor.fetchone()[0]
                conn.commit()
                return new_client_id
    except Exception as e:
        print(f"Ошибка при получении/создании клиента: {e}")
        return 1