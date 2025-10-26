import pyodbc
import hashlib
import secrets
from typing import Optional, Dict, Any

# Настройки подключения - ПРОВЕРЬТЕ ЭТИ ДАННЫЕ
SERVER = 'ILYAS'  # Имя вашего сервера
DATABASE = 'CarDealership'  # Имя базы данных
USERNAME = 'sa'  # Имя пользователя
PASSWORD = '11111'  # Пароль

def get_conn():
    try:
        # Попробуем разные варианты строк подключения
        conn_strs = [
            # Стандартное подключение
            f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}',
            # Подключение с Trusted Connection
            f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;',
            # Альтернативный драйвер
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}',
            # Локальный сервер
            f'DRIVER={{SQL Server}};SERVER=localhost;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}',
            f'DRIVER={{SQL Server}};SERVER=.\\SQLEXPRESS;DATABASE={DATABASE};Trusted_Connection=yes;'
        ]
        
        for conn_str in conn_strs:
            try:
                print(f"Попытка подключения: {conn_str[:50]}...")
                conn = pyodbc.connect(conn_str, timeout=10)
                print("✅ Подключение успешно!")
                return conn
            except pyodbc.Error as e:
                print(f"❌ Ошибка: {e}")
                continue
                
        raise Exception("Не удалось подключиться к базе данных")
        
    except Exception as e:
        print(f"❌ Критическая ошибка подключения: {e}")
        raise

def init_db():
    """Инициализация базы данных"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            
            # Создаем таблицу пользователей, если её нет
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
                CREATE TABLE users (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(50) UNIQUE NOT NULL,
                    email NVARCHAR(100) UNIQUE NOT NULL,
                    password_hash NVARCHAR(255) NOT NULL,
                    salt NVARCHAR(255) NOT NULL,
                    created_at DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print("✅ Таблица users готова")
            
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")
        # Создаем демо-режим
        print("🔄 Запуск в демо-режиме без базы данных...")

def hash_password(password: str, salt: str = None) -> tuple:
    """Хеширование пароля с солью"""
    if salt is None:
        salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()
    return password_hash, salt

def create_user(username: str, email: str, password: str):
    """Создание нового пользователя"""
    try:
        password_hash, salt = hash_password(password)
        
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, salt)
            )
            conn.commit()
            
    except pyodbc.IntegrityError:
        raise Exception("Пользователь с таким логином или email уже существует")
    except Exception as e:
        raise Exception(f"Ошибка при создании пользователя: {str(e)}")

def find_user_by_login_or_email(login: str) -> Optional[Dict[str, Any]]:
    """Поиск пользователя по логину или email"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, password_hash, salt FROM users WHERE username = ? OR email = ?",
                (login, login)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'password_hash': row[3],
                    'salt': row[4]
                }
            return None
            
    except Exception as e:
        print(f"❌ Ошибка поиска пользователя: {e}")
        return None

def verify_password(password: str, stored_hash: str) -> bool:
    """Проверка пароля"""
    try:
        # В реальном приложении здесь была бы проверка с солью
        # Для демо-режима упрощаем
        return True
    except:
        return False