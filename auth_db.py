import pyodbc
import hashlib
from typing import Optional, Dict, Any

# === НАСТРОЙКИ ПОДКЛЮЧЕНИЯ ===
SERVER = 'ILYAS'
DATABASE = 'CarDealership'
USERNAME = 'sa'
PASSWORD = '11111'


# === ПОДКЛЮЧЕНИЕ К БД ===
def get_conn():
    """Создание подключения к базе данных"""
    try:
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return None


# === ИНИЦИАЛИЗАЦИЯ БД ===
def init_db():
    """Создание таблиц при первом запуске"""
    try:
        conn = get_conn()
        if not conn:
            print("❌ Нет соединения с базой данных")
            return False

        cursor = conn.cursor()

        # Таблица пользователей
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(100) UNIQUE NOT NULL,
            email NVARCHAR(200) UNIQUE NOT NULL,
            password_hash NVARCHAR(256) NOT NULL,
            role NVARCHAR(50) DEFAULT 'client',
            first_name NVARCHAR(100),
            last_name NVARCHAR(100)
        )
        """)

        # Таблица клиентов
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='clients' AND xtype='U')
        CREATE TABLE clients (
            id INT IDENTITY(1,1) PRIMARY KEY,
            first_name NVARCHAR(100),
            last_name NVARCHAR(100),
            phone NVARCHAR(50),
            email NVARCHAR(200),
            user_id INT FOREIGN KEY REFERENCES users(id)
        )
        """)

        # Таблица сотрудников
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='employees' AND xtype='U')
        CREATE TABLE employees (
            id INT IDENTITY(1,1) PRIMARY KEY,
            first_name NVARCHAR(100),
            last_name NVARCHAR(100),
            position NVARCHAR(100),
            phone NVARCHAR(50),
            email NVARCHAR(200),
            user_id INT FOREIGN KEY REFERENCES users(id)
        )
        """)

        # Добавляем тестового администратора
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            password_hash = hash_password("admin")
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name)
                VALUES ('admin', 'admin@autodreams.local', ?, 'employee', 'Админ', 'Системы')
            """, (password_hash,))
            
        # Добавляем тестовых клиентов
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'client1'")
        if cursor.fetchone()[0] == 0:
            password_hash = hash_password("123")
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name)
                VALUES ('client1', 'client1@autodreams.local', ?, 'client', 'Иван', 'Петров')
            """, (password_hash,))
            
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'client2'")
        if cursor.fetchone()[0] == 0:
            password_hash = hash_password("123")
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name)
                VALUES ('client2', 'client2@autodreams.local', ?, 'client', 'Мария', 'Сидорова')
            """, (password_hash,))

        conn.commit()
        conn.close()
        print("✅ Таблицы инициализированы успешно")
        return True

    except Exception as e:
        print(f"❌ Ошибка инициализации базы данных: {e}")
        return False


# === ХЕШИРОВАНИЕ ===
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(password: str, stored_hash: str) -> bool:
    return hash_password(password) == stored_hash


# === РЕГИСТРАЦИЯ ===
def create_user(username: str, email: str, password: str, first_name: str, last_name: str):
    try:
        conn = get_conn()
        if not conn:
            raise Exception("Нет подключения к базе данных")

        cursor = conn.cursor()

        # Проверяем, существует ли пользователь с таким логином или email
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            raise Exception("Пользователь с таким логином или email уже существует")

        password_hash = hash_password(password)

        # Вставляем пользователя
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role, first_name, last_name)
            VALUES (?, ?, ?, 'client', ?, ?)
        """, (username, email, password_hash, first_name, last_name))

        # Получаем ID нового пользователя
        cursor.execute("SELECT @@IDENTITY")
        user_id_result = cursor.fetchone()
        
        if not user_id_result or user_id_result[0] is None:
            raise Exception("Не удалось получить ID нового пользователя")
        
        user_id = int(user_id_result[0])

        # Создаем запись клиента
        cursor.execute("""
            INSERT INTO clients (first_name, last_name, phone, email, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (first_name, last_name, '+7-000-000-00-00', email, user_id))

        conn.commit()
        conn.close()
        print(f"✅ Пользователь {username} успешно зарегистрирован")
        return True

    except Exception as e:
        # Откатываем транзакцию в случае ошибки
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise Exception(f"Ошибка при создании пользователя: {str(e)}")


# === ПОИСК ПОЛЬЗОВАТЕЛЯ ===
def find_user_by_login_or_email(login: str) -> Optional[Dict[str, Any]]:
    try:
        conn = get_conn()
        if not conn:
            raise Exception("Нет подключения к базе данных")

        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, email, password_hash, role, first_name, last_name
            FROM users
            WHERE username = ? OR email = ?
        """, (login, login))

        row = cursor.fetchone()
        conn.close()

        if not row:
            print(f"❌ Пользователь {login} не найден")
            return None

        user = {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'password_hash': row[3],
            'role': row[4],
            'first_name': row[5],
            'last_name': row[6]
        }
        print(f"✅ Найден пользователь: {user['username']} (роль: {user['role']})")
        return user

    except Exception as e:
        print(f"❌ Ошибка поиска пользователя: {e}")
        return None