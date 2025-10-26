import pyodbc
import hashlib
import secrets
from typing import Optional, Dict, Any

SERVER = 'ILYAS'
DATABASE = 'CarDealership'
USERNAME = 'sa'
PASSWORD = '11111'

def get_conn():
    try:
        conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        return pyodbc.connect(conn_str)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        raise

def init_db():
    """Инициализация базы данных"""
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            print("✅ Подключение к базе данных успешно")
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")

def hash_password(password: str, salt: str = None) -> tuple:
    """Хеширование пароля с солью"""
    if salt is None:
        salt = secrets.token_hex(16)
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password_hash, salt

def verify_password(password: str, stored_hash: str) -> bool:
    """Проверка пароля"""
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password_hash == stored_hash

def create_user(username: str, email: str, password: str):
    """Создание нового пользователя"""
    try:
        password_hash, salt = hash_password(password)
        
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, salt, role) VALUES (?, ?, ?, ?, 'client')",
                (username, email, password_hash, salt)
            )
            conn.commit()
            return True
            
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
                "SELECT id, username, email, password_hash, salt, role FROM users WHERE username = ? OR email = ?",
                (login, login)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'password_hash': row[3],
                    'salt': row[4],
                    'role': row[5]
                }
            return None
            
    except Exception as e:
        print(f"❌ Ошибка поиска пользователя: {e}")
        return None