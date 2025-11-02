import pyodbc
from typing import List, Dict, Any, Optional
from auth_db import get_conn

def init_car_db():
    try:
        conn = get_conn()
        if not conn:
            return False

        cursor = conn.cursor()

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='cars' AND xtype='U')
        CREATE TABLE cars (
            id INT IDENTITY(1,1) PRIMARY KEY,
            brand NVARCHAR(100),
            model NVARCHAR(100),
            year INT,
            vin NVARCHAR(17) UNIQUE,
            color NVARCHAR(50),
            price FLOAT,
            status NVARCHAR(50) DEFAULT 'в наличии',
            mileage INT DEFAULT 0
        )
        """)

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='employees' AND xtype='U')
        CREATE TABLE employees (
            id INT IDENTITY(1,1) PRIMARY KEY,
            first_name NVARCHAR(100),
            last_name NVARCHAR(100),
            position NVARCHAR(100),
            phone NVARCHAR(50),
            email NVARCHAR(200),
            user_id INT NULL
        )
        """)

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='orders' AND xtype='U')
        CREATE TABLE orders (
            id INT IDENTITY(1,1) PRIMARY KEY,
            client_id INT,
            car_id INT,
            employee_id INT,
            sale_date DATETIME DEFAULT GETDATE(),
            final_price FLOAT,
            status NVARCHAR(50),
            FOREIGN KEY (car_id) REFERENCES cars(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """)

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='reviews' AND xtype='U')
        CREATE TABLE reviews (
            id INT IDENTITY(1,1) PRIMARY KEY,
            client_id INT,
            order_id INT,
            rating INT,
            comment NVARCHAR(MAX),
            review_date DATETIME DEFAULT GETDATE(),
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
        """)

        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO employees (first_name, last_name, position, phone, email)
                VALUES ('Ильяс', 'Менеджер', 'Продавец-консультант', '+7-999-000-00-00', 'manager@autodreams.local')
            """)

        cursor.execute("SELECT COUNT(*) FROM cars")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO cars (brand, model, year, vin, color, price, status, mileage)
                VALUES 
                ('Toyota', 'Camry', 2023, 'JTNBE46KX83012345', 'Черный', 3300000, 'в наличии', 0),
                ('BMW', 'X5', 2022, 'WBAKS01040C12345', 'Белый', 7200000, 'в наличии', 1000)
            """)

        conn.commit()
        conn.close()
        return True

    except Exception:
        return False

def get_all_cars() -> List[Dict[str, Any]]:
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars ORDER BY brand, model")
        rows = cursor.fetchall()
        conn.close()
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
        raise Exception(f"Не удалось загрузить автомобили: {str(e)}")

def get_available_cars() -> List[Dict[str, Any]]:
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE status = 'в наличии' ORDER BY brand, model")
        rows = cursor.fetchall()
        conn.close()
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
        raise Exception(f"Не удалось загрузить доступные автомобили: {str(e)}")

def get_car_by_id(car_id: int) -> Optional[Dict[str, Any]]:
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
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
    except Exception as e:
        raise Exception(f"Ошибка при загрузке автомобиля: {e}")

def add_car(brand, model, year, vin, color, price, mileage):
    try:
        vin = vin[:17] if len(vin) > 17 else vin
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cars (brand, model, year, vin, color, price, status, mileage)
            VALUES (?, ?, ?, ?, ?, ?, 'в наличии', ?)
        """, (brand, model, year, vin, color, price, mileage))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise Exception(f"Ошибка при добавлении автомобиля: {e}")

def update_car(car_id, brand, model, year, vin, color, price, mileage):
    try:
        vin = vin[:17] if len(vin) > 17 else vin
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cars
            SET brand=?, model=?, year=?, vin=?, color=?, price=?, mileage=?
            WHERE id=?
        """, (brand, model, year, vin, color, price, mileage, car_id))
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Ошибка при обновлении автомобиля: {e}")

def delete_car(car_id):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Ошибка при удалении автомобиля: {e}")

def create_order(client_id: int, car_id: int, employee_id: int, final_price: float):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (client_id, car_id, employee_id, final_price, status)
            VALUES (?, ?, ?, ?, 'оформлен')
        """, (client_id, car_id, employee_id, final_price))
        cursor.execute("UPDATE cars SET status = 'продан' WHERE id = ?", (car_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise Exception(f"Ошибка при создании заказа: {e}")

def get_or_create_client_for_user(user_id: int, username: str) -> int:
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clients WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return row[0]
        cursor.execute("SELECT first_name, last_name, email FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            first_name, last_name, email = user_data
        else:
            first_name, last_name, email = username, username, f"{username}@autodreams.com"
        cursor.execute("""
            INSERT INTO clients (user_id, first_name, last_name, phone, email)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, first_name, last_name, '+7-000-000-00-00', email))
        cursor.execute("SELECT SCOPE_IDENTITY()")
        new_id = int(cursor.fetchone()[0])
        conn.commit()
        conn.close()
        return new_id
    except Exception as e:
        raise Exception(f"Ошибка при получении клиента: {e}")

def get_client_orders(client_id: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id, c.brand, c.model, c.vin, o.final_price, o.sale_date
            FROM orders o
            JOIN cars c ON o.car_id = c.id
            WHERE o.client_id = ?
            ORDER BY o.sale_date DESC
        """, (client_id,))
        rows = cursor.fetchall()
        conn.close()
        orders = []
        for row in rows:
            orders.append({
                'id': row[0],
                'brand': row[1],
                'model': row[2],
                'vin': row[3],
                'final_price': float(row[4]),
                'sale_date': row[5]
            })
        return orders
    except Exception as e:
        raise Exception(f"Ошибка при загрузке заказов: {e}")

def add_review(client_id: int, order_id: int, rating: int, comment: str):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM orders WHERE id = ? AND client_id = ?", (order_id, client_id))
        order = cursor.fetchone()
        if not order:
            raise Exception("Этот заказ не принадлежит вам или не существует")
        cursor.execute("SELECT id FROM reviews WHERE order_id = ? AND client_id = ?", (order_id, client_id))
        existing_review = cursor.fetchone()
        if existing_review:
            raise Exception("Вы уже оставляли отзыв на этот заказ")
        cursor.execute("""
            INSERT INTO reviews (client_id, order_id, rating, comment)
            VALUES (?, ?, ?, ?)
        """, (client_id, order_id, rating, comment))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise Exception(f"Ошибка при добавлении отзыва: {e}")

def get_client_reviews(client_id=None):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        if client_id:
            cursor.execute("""
                SELECT r.order_id, r.rating, r.comment, r.review_date, 
                       c.first_name + ' ' + c.last_name as client_name
                FROM reviews r
                JOIN clients c ON r.client_id = c.id
                WHERE r.client_id = ?
                ORDER BY r.review_date DESC
            """, (client_id,))
        else:
            cursor.execute("""
                SELECT r.order_id, r.rating, r.comment, r.review_date, 
                       c.first_name + ' ' + c.last_name as client_name
                FROM reviews r
                JOIN clients c ON r.client_id = c.id
                ORDER BY r.review_date DESC
            """)
        rows = cursor.fetchall()
        conn.close()
        reviews = []
        for row in rows:
            reviews.append({
                'order_id': row[0],
                'rating': row[1],
                'comment': row[2],
                'review_date': row[3],
                'client_name': row[4]
            })
        return reviews
    except Exception as e:
        raise Exception(f"Ошибка при загрузке отзывов: {e}")

def get_available_employee():
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 id FROM employees ORDER BY id")
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        else:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees (first_name, last_name, position, phone, email)
                VALUES ('Авто', 'Менеджер', 'Продавец', '+7-999-000-00-00', 'manager@autodreams.local')
            """)
            cursor.execute("SELECT SCOPE_IDENTITY()")
            new_id = int(cursor.fetchone()[0])
            conn.commit()
            conn.close()
            return new_id
    except Exception:
        return 1

def get_all_orders():
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                o.id,
                c.first_name + ' ' + c.last_name as client_name,
                car.brand,
                car.model,
                o.final_price,
                o.sale_date,
                e.first_name + ' ' + e.last_name as employee_name
            FROM orders o
            JOIN clients c ON o.client_id = c.id
            JOIN cars car ON o.car_id = car.id
            JOIN employees e ON o.employee_id = e.id
            ORDER BY o.sale_date DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        orders = []
        for row in rows:
            orders.append({
                'id': row[0],
                'client_name': row[1],
                'brand': row[2],
                'model': row[3],
                'final_price': float(row[4]),
                'sale_date': row[5],
                'employee_name': row[6]
            })
        return orders
    except Exception as e:
        raise Exception(f"Ошибка при загрузке всех заказов: {e}")

def get_car_quantity(car_id: int) -> int:
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM cars 
            WHERE brand = (SELECT brand FROM cars WHERE id = ?) 
            AND model = (SELECT model FROM cars WHERE id = ?)
            AND status = 'в наличии'
        """, (car_id, car_id))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0

def add_car_quantity(brand: str, model: str, quantity: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        import random
        import time
        added_count = 0
        for i in range(quantity):
            try:
                base_vin = f"{brand[:3]}{model[:3]}"
                timestamp = str(int(time.time() * 1000))[-6:]
                random_part = str(random.randint(1000, 9999))
                unique_vin = base_vin + timestamp + random_part
                vin = unique_vin[:17]
                cursor.execute("SELECT price, year FROM cars WHERE brand = ? AND model = ?", (brand, model))
                existing_car = cursor.fetchone()
                if existing_car:
                    price = existing_car[0]
                    year = existing_car[1]
                else:
                    price = 3000000
                    year = 2023
                cursor.execute("""
                    INSERT INTO cars (brand, model, year, vin, color, price, status, mileage)
                    VALUES (?, ?, ?, ?, 'Разные цвета', ?, 'в наличии', 0)
                """, (brand, model, year, vin, price))
                added_count += 1
            except Exception as e:
                if "UNIQUE KEY" in str(e) or "повторяющийся ключ" in str(e):
                    continue
                else:
                    raise e
        conn.commit()
        conn.close()
        return added_count
    except Exception as e:
        raise Exception(f"Ошибка при добавлении автомобилей: {e}")