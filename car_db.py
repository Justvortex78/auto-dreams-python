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
    """Получить все автомобили"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CARS ORDER BY brand, model")
            rows = cursor.fetchall()
            
            cars = []
            for row in rows:
                cars.append({
                    'id': row[0],
                    'brand': row[1],
                    'model': row[2],
                    'year': row[3],
                    'vin': row[4],
                    'color': row[5],
                    'price': float(row[6]),
                    'status': row[7],
                    'mileage': row[8]
                })
            return cars
    except Exception as e:
        print(f"Ошибка при получении автомобилей: {e}")
        return []

def get_available_cars() -> List[Dict[str, Any]]:
    """Получить только доступные автомобили (в наличии)"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CARS WHERE status = 'в наличии' ORDER BY brand, model")
            rows = cursor.fetchall()
            
            cars = []
            for row in rows:
                cars.append({
                    'id': row[0],
                    'brand': row[1],
                    'model': row[2],
                    'year': row[3],
                    'vin': row[4],
                    'color': row[5],
                    'price': float(row[6]),
                    'status': row[7],
                    'mileage': row[8]
                })
            return cars
    except Exception as e:
        print(f"Ошибка при получении доступных автомобилей: {e}")
        return []

def get_client_orders(client_id: int) -> List[Dict[str, Any]]:
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, c.brand, c.model, c.vin, c.price, c.color, c.year,
                       emp.first_name + ' ' + emp.last_name as employee_name
                FROM ORDERS o
                JOIN CARS c ON o.car_id = c.id
                JOIN EMPLOYEES emp ON o.employee_id = emp.id
                WHERE o.client_id = ?
                ORDER BY o.sale_date DESC
            """, (client_id,))
            
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                orders.append({
                    'id': row[0],
                    'client_id': row[1],
                    'car_id': row[2],
                    'employee_id': row[3],
                    'sale_date': row[4],
                    'final_price': float(row[5]),
                    'status': row[6],
                    'brand': row[7],
                    'model': row[8],
                    'vin': row[9],
                    'price': float(row[10]),
                    'color': row[11],
                    'year': row[12],
                    'employee_name': row[13]
                })
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
                reviews.append({
                    'id': row[0],
                    'client_id': row[1],
                    'order_id': row[2],
                    'rating': row[3],
                    'comment': row[4],
                    'review_date': row[5],
                    'brand': row[6],
                    'model': row[7]
                })
            return reviews
    except Exception as e:
        print(f"Ошибка при получении отзывов: {e}")
        return []

def create_order(client_id: int, car_id: int, employee_id: int, final_price: float):
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO ORDERS (client_id, car_id, employee_id, sale_date, final_price, status) VALUES (?, ?, ?, GETDATE(), ?, 'выполнен')",
                (client_id, car_id, employee_id, final_price)
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
            
            cursor.execute("SELECT id FROM CLIENTS WHERE user_id = ?", (user_id,))
            client = cursor.fetchone()
            
            if client:
                return client[0]
            else:
                cursor.execute(
                    "INSERT INTO CLIENTS (first_name, last_name, phone, email, user_id) VALUES (?, ?, ?, ?, ?)",
                    (username, "User", "+7-000-000-00-00", f"{username}@example.com", user_id)
                )
                cursor.execute("SELECT SCOPE_IDENTITY()")
                new_client_id = cursor.fetchone()[0]
                conn.commit()
                return new_client_id
    except Exception as e:
        print(f"Ошибка при получении/создании клиента: {e}")
        return 1

def get_available_employee():
    """Получаем случайного доступного сотрудника"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT TOP 1 id FROM EMPLOYEES ORDER BY NEWID()")
            employee = cursor.fetchone()
            return employee[0] if employee else 1
    except Exception as e:
        print(f"Ошибка при получении сотрудника: {e}")
        return 1

def add_car(brand: str, model: str, year: int, vin: str, color: str, price: float, mileage: int = 0):
    """Добавить новый автомобиль"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO CARS (brand, model, year, vin, color, price, status, mileage) VALUES (?, ?, ?, ?, ?, ?, 'в наличии', ?)",
                (brand, model, year, vin, color, price, mileage)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при добавлении автомобиля: {e}")
        raise

def update_car(car_id: int, brand: str, model: str, year: int, vin: str, color: str, price: float, mileage: int):
    """Обновить данные автомобиля"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE CARS SET brand=?, model=?, year=?, vin=?, color=?, price=?, mileage=? WHERE id=?",
                (brand, model, year, vin, color, price, mileage, car_id)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при обновлении автомобиля: {e}")
        raise

def delete_car(car_id: int):
    """Удалить автомобиль"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CARS WHERE id = ?", (car_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при удалении автомобиля: {e}")
        raise

def get_car_by_id(car_id: int) -> Dict[str, Any]:
    """Получить автомобиль по ID"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CARS WHERE id = ?", (car_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'brand': row[1],
                    'model': row[2],
                    'year': row[3],
                    'vin': row[4],
                    'color': row[5],
                    'price': float(row[6]),
                    'status': row[7],
                    'mileage': row[8]
                }
            return None
    except Exception as e:
        print(f"Ошибка при получении автомобиля: {e}")
        return None