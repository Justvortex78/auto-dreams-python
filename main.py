# main.py (исправленный)
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QTextEdit, QStackedWidget, 
                             QScrollArea, QGridLayout, QMessageBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFormLayout, QSpinBox, QFrame, QDialog, QScrollBar, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QFont

# Импортируем также get_conn для realtime stats
from auth_db import init_db, create_user, find_user_by_login_or_email, verify_password, get_conn
from car_db import (get_available_cars, get_all_cars, get_client_orders, add_review, 
                   get_client_reviews, create_order, get_or_create_client_for_user, 
                   get_available_employee, add_car, update_car, delete_car, get_car_by_id, init_car_db)

COLORS = {
    'primary_bg': '#0f172a',
    'secondary_bg': '#1e293b',
    'accent_green': '#10b981',
    'accent_teal': '#0d9488',
    'text_primary': '#f1f5f9',
    'text_secondary': '#94a3b8',
    'border': '#334155',
    'success': '#22c55e',
    'danger': '#ef4444'
}

class Line(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet(f"background-color: {COLORS['accent_green']}; margin: 10px 0;")

class LoginPage(QWidget):
    def __init__(self, on_login_success, go_register):
        super().__init__()
        self.on_login_success = on_login_success
        self.go_register = go_register
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("AUTO DREAMS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 48px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 10px;
            font-family: 'Segoe UI';
        """)
        
        subtitle = QLabel("ПРЕМИАЛЬНЫЕ АВТОМОБИЛИ")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            font-size: 20px;
            color: {COLORS['accent_teal']};
            margin-bottom: 40px;
            font-family: 'Segoe UI';
        """)
        
        form_container = QWidget()
        form_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_green']};
            border-radius: 15px;
            padding: 40px;
        """)
        form_layout = QVBoxLayout(form_container)
        
        form_title = QLabel("ВХОД В СИСТЕМУ")
        form_title.setAlignment(Qt.AlignCenter)
        form_title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин или Email")
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['primary_bg']};
                color: {COLORS['text_primary']};
                padding: 15px;
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 16px;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus {{
                border-color: {COLORS['accent_green']};
            }}
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['primary_bg']};
                color: {COLORS['text_primary']};
                padding: 15px;
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 16px;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus {{
                border-color: {COLORS['accent_green']};
            }}
        """)
        
        btn_login = QPushButton("🚀 ВОЙТИ")
        btn_login.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_login.clicked.connect(self.login)
        
        btn_register = QPushButton("📝 РЕГИСТРАЦИЯ")
        btn_register.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_green']};
                border: 2px solid {COLORS['accent_green']};
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_green']};
                color: {COLORS['text_primary']};
            }}
        """)
        btn_register.clicked.connect(self.go_register)
        
        info_label = QLabel("🔑 Тестовые пользователи:\nАдмин: admin/admin\nКлиенты: client1/123, client2/123")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 14px;
            margin-top: 20px;
            font-family: 'Segoe UI';
            background-color: {COLORS['primary_bg']};
            padding: 15px;
            border-radius: 8px;
            border: 1px solid {COLORS['border']};
        """)
        
        form_layout.addWidget(form_title)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(btn_login)
        form_layout.addWidget(btn_register)
        form_layout.addWidget(info_label)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(form_container)
        layout.addStretch()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
    
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        
        print(f"🔐 Попытка входа: {username}")
    
        try:
            user = find_user_by_login_or_email(username)
        
            if user and verify_password(password, user['password_hash']):
                print(f"✅ Вход выполнен: {user['username']} (роль: {user['role']})")
                self.on_login_success(user)
            else:
                print("❌ Неверный логин или пароль")
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
            
        except Exception as e:
            print(f"❌ Ошибка при входе: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения к базе данных:\n{str(e)}")

class RegisterPage(QWidget):
    def __init__(self, go_login):
        super().__init__()
        self.go_login = go_login
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("РЕГИСТРАЦИЯ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 36px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        form_container = QWidget()
        form_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_green']};
            border-radius: 15px;
            padding: 40px;
            max-width: 500px;
            margin: 0 auto;
        """)
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(20)
        
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Введите ваше имя")
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Введите вашу фамилию")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Придумайте логин")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Введите ваш email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Придумайте пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Повторите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        
        input_style = f"""
            QLineEdit {{
                background-color: {COLORS['primary_bg']};
                color: {COLORS['text_primary']};
                padding: 12px;
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Segoe UI';
                min-width: 300px;
            }}
            QLineEdit:focus {{
                border-color: {COLORS['accent_green']};
            }}
        """
        
        for input_field in [self.first_name_input, self.last_name_input, self.username_input, 
                           self.email_input, self.password_input, self.confirm_password_input]:
            input_field.setStyleSheet(input_style)
        
        form_layout.addRow("Имя:", self.first_name_input)
        form_layout.addRow("Фамилия:", self.last_name_input)
        form_layout.addRow("Логин:", self.username_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Пароль:", self.password_input)
        form_layout.addRow("Подтверждение:", self.confirm_password_input)
        
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setStyleSheet(f"color: {COLORS['accent_green']}; font-size: 14px; font-weight: bold; font-family: 'Segoe UI';")
        
        btn_register = QPushButton("✅ ЗАРЕГИСТРИРОВАТЬСЯ")
        btn_register.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_register.clicked.connect(self.register)
        
        btn_back = QPushButton("◀ НАЗАД К ВХОДУ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_green']};
                border: 2px solid {COLORS['accent_green']};
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_green']};
                color: {COLORS['text_primary']};
            }}
        """)
        btn_back.clicked.connect(self.go_login)
        
        layout.addWidget(title)
        layout.addWidget(form_container)
        layout.addWidget(btn_register)
        layout.addWidget(btn_back)
        layout.addStretch()

    def register(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        if not all([first_name, last_name, username, email, password, confirm_password]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        try:
            # ПРАВИЛЬНЫЙ ВЫЗОВ - 5 АРГУМЕНТОВ
            create_user(username, email, password, first_name, last_name)
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно! Теперь вы можете войти.")
            self.go_login()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

class CarCard(QWidget):
    def __init__(self, car, user, on_buy_callback):
        super().__init__()
        self.car = car
        self.user = user
        self.on_buy_callback = on_buy_callback
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(320, 420)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['secondary_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                margin: 8px;
            }}
            QWidget:hover {{
                border-color: {COLORS['accent_green']};
                background-color: #1e2130;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Изображение автомобиля
        image_label = QLabel()
        image_label.setFixedSize(296, 160)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['primary_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        pixmap = self.load_car_image()
        if pixmap and not pixmap.isNull():
            pixmap = pixmap.scaled(290, 155, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText(f"🚗\n{self.car['brand']}\n{self.car['model']}")
            image_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['primary_bg']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 8px;
                    color: {COLORS['accent_green']};
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                }}
            """)

        title_label = QLabel(f"{self.car['brand']} {self.car['model']}")
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']}; 
            font-size: 16px; 
            font-weight: bold;
            margin-top: 5px;
            font-family: 'Segoe UI';
        """)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)

        vin_label = QLabel(f"VIN: {self.car['vin'][:8]}...")
        vin_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-family: 'Segoe UI';")
        vin_label.setAlignment(Qt.AlignCenter)

        price_label = QLabel(f"{self.car['price']:,.0f} ₽")
        price_label.setStyleSheet(f"""
            color: {COLORS['accent_green']}; 
            font-size: 18px; 
            font-weight: bold;
            margin: 5px 0;
            font-family: 'Segoe UI';
            background-color: {COLORS['primary_bg']};
            border-radius: 6px;
            padding: 6px;
            border: 1px solid {COLORS['border']};
        """)
        price_label.setAlignment(Qt.AlignCenter)

        status_label = QLabel(f"Статус: {self.car['status']}")
        status_color = COLORS['success'] if self.car['status'] == 'в наличии' else COLORS['danger']
        status_label.setStyleSheet(f"color: {status_color}; font-size: 12px; font-weight: bold; font-family: 'Segoe UI';")
        status_label.setAlignment(Qt.AlignCenter)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        btn_details = QPushButton("🔍")
        btn_details.setToolTip("Подробнее")
        btn_details.setFixedSize(40, 35)
        btn_details.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_green']};
                border: 1px solid {COLORS['accent_green']};
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_green']};
                color: {COLORS['text_primary']};
            }}
        """)
        btn_details.clicked.connect(self.show_details)

        btn_buy = QPushButton("КУПИТЬ" if self.car['status'] == 'в наличии' else "ПРОДАНО")
        btn_buy.setEnabled(self.car['status'] == 'в наличии')
        btn_buy.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
            QPushButton:disabled {{
                background-color: {COLORS['border']};
                color: {COLORS['text_secondary']};
            }}
        """)
        if self.car['status'] == 'в наличии':
            btn_buy.clicked.connect(self.buy_car)

        buttons_layout.addWidget(btn_details)
        buttons_layout.addWidget(btn_buy)

        layout.addWidget(image_label)
        layout.addWidget(title_label)
        layout.addWidget(vin_label)
        layout.addWidget(price_label)
        layout.addWidget(status_label)
        layout.addLayout(buttons_layout)

    def load_car_image(self):
        """Загружаем изображение автомобиля"""
        try:
            images_path = os.path.join(os.path.dirname(__file__), "images")
            
            if not os.path.exists(images_path):
                os.makedirs(images_path)
                return None
            
            # Создаем список возможных имен файлов
            possible_filenames = [
                f"{self.car['brand'].lower()}_{self.car['model'].lower()}.jpg",
                f"{self.car['brand'].lower()}_{self.car['model'].lower()}.png",
                f"{self.car['brand'].lower()}_{self.car['model'].lower()}.jpeg",
                f"{self.car['id']}.jpg",
                f"{self.car['id']}.png",
                "default_car.jpg"
            ]
            
            for filename in possible_filenames:
                image_path = os.path.join(images_path, filename)
                if os.path.exists(image_path):
                    return QPixmap(image_path)
            
            return None
            
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            return None

    def show_details(self):
        msg = QMessageBox()
        msg.setWindowTitle(f"🚗 {self.car['brand']} {self.car['model']}")
        msg.setText(f"""
<b style='color: {COLORS['accent_green']};'>ДЕТАЛЬНАЯ ИНФОРМАЦИЯ:</b>

<b>Марка:</b> {self.car['brand']}
<b>Модель:</b> {self.car['model']}
<b>Год:</b> {self.car.get('year', '2024')}
<b>Цвет:</b> {self.car.get('color', 'Не указан')}
<b>VIN:</b> {self.car['vin']}
<b>Пробег:</b> {self.car.get('mileage', 0):,} км
<b>Цена:</b> {self.car['price']:,.0f} ₽
<b>Статус:</b> {self.car['status']}

<b>Описание:</b>
{self.get_car_description()}
        """)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 12px;
                font-family: 'Segoe UI';
            }}
            QMessageBox QLabel {{
                color: {COLORS['text_primary']};
                font-size: 14px;
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-family: 'Segoe UI';
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        msg.exec()

    def get_car_description(self):
        descriptions = {
            'Toyota Camry': 'Стильный седан • Надежность • Комфорт • Экономичный расход',
            'Toyota Corolla': 'Компактный седан • Экономичность • Надежность • Безопасность',
            'Honda Civic': 'Спортивный седан • Динамика • Качество • Технологии',
            'BMW X5': 'Премиальный внедорожник • Динамика • Роскошь • Технологии',
            'BMW 3 Series': 'Бизнес-седан • Спортивный характер • Комфорт • Качество',
            'Mercedes E-Class': 'Бизнес-класс • Комфорт • Инновации • Качество',
            'Audi A4': 'Премиум седан • Стиль • Технологии • Качество',
            'Ford Focus': 'Компактный хэтчбек • Практичность • Экономичность • Надежность',
            'Hyundai Tucson': 'Современный дизайн • Гарантия • Оснащение • Экономичность',
            'Kia Sportage': 'Стильный кроссовер • Цена/Качество • Гарантия • Комфорт'
        }
        
        key = f"{self.car['brand']} {self.car['model']}"
        return descriptions.get(key, "Качественный автомобиль • Надёжность • Комфорт • Безопасность")

    def buy_car(self):
        if self.car['status'] != 'в наличии':
            QMessageBox.warning(self, "Внимание", "Этот автомобиль уже продан.")
            return
        reply = QMessageBox()
        reply.setWindowTitle("🎯 ПОДТВЕРЖДЕНИЕ ПОКУПКИ")
        reply.setText(f"""
<b style='color: {COLORS['accent_green']};'>ПОДТВЕРДИТЕ ПОКУПКУ:</b>

{self.car['brand']} {self.car['model']}

<b>ЦЕНА: {self.car['price']:,.0f} ₽</b>

✅ Гарантия 3 года
✅ Бесплатная доставка  
✅ Первое ТО в подарок
✅ Коврики в салон
        """)
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply.setDefaultButton(QMessageBox.No)
        reply.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 12px;
                font-family: 'Segoe UI';
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-family: 'Segoe UI';
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        
        result = reply.exec()
        
        if result == QMessageBox.Yes:
            try:
                client_id = get_or_create_client_for_user(self.user['id'], self.user['username'])
                employee_id = get_available_employee()
                
                create_order(client_id, self.car['id'], employee_id, self.car['price'])
                
                success_msg = QMessageBox()
                success_msg.setWindowTitle("🎉 ПОЗДРАВЛЕНИЯ!")
                success_msg.setText(f"""
<b style='color: {COLORS['accent_green']};'>ПОКУПКА УСПЕШНО ОФОРМЛЕНА!</b>

{self.car['brand']} {self.car['model']}

<b>ЦЕНА: {self.car['price']:,.0f} ₽</b>

📅 Доставка: 3 рабочих дня
📞 Менеджер свяжется в течение 1 часа
🎁 Бонусы: Первое ТО + коврики

Спасибо за покупку! 🚗✨
                """)
                success_msg.setStyleSheet(f"""
                    QMessageBox {{
                        background-color: {COLORS['secondary_bg']};
                        color: {COLORS['text_primary']};
                        border: 2px solid {COLORS['accent_green']};
                        border-radius: 12px;
                        font-family: 'Segoe UI';
                    }}
                    QPushButton {{
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                            stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                        color: {COLORS['text_primary']};
                        border: none;
                        padding: 8px 16px;
                        border-radius: 6px;
                        font-weight: bold;
                        font-family: 'Segoe UI';
                    }}
                """)
                success_msg.exec()
                
                self.on_buy_callback()
                
            except Exception as e:
                QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось оформить покупку: {str(e)}")

class OrderCard(QWidget):
    def __init__(self, order):
        super().__init__()
        self.order = order
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(320, 420)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['secondary_bg']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 12px;
                margin: 8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Изображение автомобиля
        image_label = QLabel()
        image_label.setFixedSize(296, 160)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['primary_bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                color: {COLORS['text_primary']};
            }}
        """)
        
        pixmap = self.load_car_image()
        if pixmap and not pixmap.isNull():
            pixmap = pixmap.scaled(290, 155, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText(f"🚗\n{self.order['brand']}\n{self.order['model']}")
            image_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['primary_bg']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 8px;
                    color: {COLORS['accent_green']};
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                }}
            """)

        title_label = QLabel(f"{self.order['brand']} {self.order['model']}")
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']}; 
            font-size: 16px; 
            font-weight: bold;
            margin-top: 5px;
            font-family: 'Segoe UI';
        """)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)

        vin_label = QLabel(f"VIN: {self.order['vin']}")
        vin_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-family: 'Segoe UI';")
        vin_label.setAlignment(Qt.AlignCenter)

        price_label = QLabel(f"{self.order['final_price']:,.0f} ₽")
        price_label.setStyleSheet(f"""
            color: {COLORS['accent_green']}; 
            font-size: 18px; 
            font-weight: bold;
            margin: 5px 0;
            font-family: 'Segoe UI';
            background-color: {COLORS['primary_bg']};
            border-radius: 6px;
            padding: 6px;
            border: 1px solid {COLORS['border']};
        """)
        price_label.setAlignment(Qt.AlignCenter)

        date_label = QLabel(f"Дата: {self.order['sale_date']}")
        date_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-family: 'Segoe UI';")
        date_label.setAlignment(Qt.AlignCenter)

        status_label = QLabel("✅ ВЫПОЛНЕН")
        status_label.setStyleSheet(f"color: {COLORS['success']}; font-size: 14px; font-weight: bold; font-family: 'Segoe UI';")
        status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(image_label)
        layout.addWidget(title_label)
        layout.addWidget(vin_label)
        layout.addWidget(price_label)
        layout.addWidget(date_label)
        layout.addWidget(status_label)

    def load_car_image(self):
        """Загружаем изображение автомобиля"""
        try:
            images_path = os.path.join(os.path.dirname(__file__), "images")
            
            if not os.path.exists(images_path):
                return None
            
            # Создаем список возможных имен файлов
            possible_filenames = [
                f"{self.order['brand'].lower()}_{self.order['model'].lower()}.jpg",
                f"{self.order['brand'].lower()}_{self.order['model'].lower()}.png",
                f"{self.order['brand'].lower()}_{self.order['model'].lower()}.jpeg",
                "default_car.jpg"
            ]
            
            for filename in possible_filenames:
                image_path = os.path.join(images_path, filename)
                if os.path.exists(image_path):
                    return QPixmap(image_path)
            
            return None
            
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            return None

class ClientMainMenuPage(QWidget):
    def __init__(self, user, logout_callback):
        super().__init__()
        self.user = user
        self.logout_callback = logout_callback
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 20)
        
        title = QLabel("AUTO DREAMS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 42px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 10px;
            font-family: 'Segoe UI';
        """)
        
        subtitle = QLabel("ПРЕМИАЛЬНЫЕ АВТОМОБИЛИ")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            font-size: 20px;
            color: {COLORS['accent_teal']};
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        
        # Показываем ФИО пользователя
        welcome_text = f"ДОБРО ПОЖАЛОВАТЬ, {self.user['first_name']} {self.user['last_name']}!"
        welcome = QLabel(welcome_text)
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet(f"""
            font-size: 18px;
            color: {COLORS['text_secondary']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        menu_container = QWidget()
        menu_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_green']};
            border-radius: 15px;
            padding: 30px;
        """)
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setAlignment(Qt.AlignCenter)
        menu_layout.setSpacing(15)
        
        menu_label = QLabel("ГЛАВНОЕ МЕНЮ")
        menu_label.setAlignment(Qt.AlignCenter)
        menu_label.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        btn_assortment = self.create_menu_button("📦 АССОРТИМЕНТ АВТОМОБИЛЕЙ")
        btn_orders = self.create_menu_button("📋 МОИ ЗАКАЗЫ")
        btn_reviews = self.create_menu_button("⭐ ОСТАВИТЬ ОТЗЫВ")
        btn_my_reviews = self.create_menu_button("📝 МОИ ОТЗЫВЫ")
        btn_exit = self.create_menu_button("🚪 ВЫХОД")
        
        btn_assortment.clicked.connect(self.show_assortment)
        btn_orders.clicked.connect(self.show_orders)
        btn_reviews.clicked.connect(self.show_reviews)
        btn_my_reviews.clicked.connect(self.show_my_reviews)
        btn_exit.clicked.connect(self.logout_callback)
        
        menu_layout.addWidget(btn_assortment)
        menu_layout.addWidget(btn_orders)
        menu_layout.addWidget(btn_reviews)
        menu_layout.addWidget(btn_my_reviews)
        menu_layout.addWidget(btn_exit)
        
        instruction_frame = QFrame()
        instruction_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['secondary_bg']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 12px;
                margin-top: 30px;
                padding: 20px;
            }}
        """)
        
        instruction_layout = QVBoxLayout(instruction_frame)
        
        instruction_title = QLabel("ИНСТРУКЦИЯ")
        instruction_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 10px;
            font-family: 'Segoe UI';
        """)
        
        instruction_text = QLabel(
            "• АССОРТИМЕНТ - просмотр и покупка автомобилей\n"
            "• МОИ ЗАКАЗЫ - история ваших покупок\n"  
            "• ОСТАВИТЬ ОТЗЫВ - написать отзыв о покупке\n"
            "• МОИ ОТЗЫВЫ - просмотр ваших отзывов\n"
            "• ВЫХОД - возврат к окну авторизации"
        )
        instruction_text.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; line-height: 1.5; font-family: 'Segoe UI';")
        
        instruction_layout.addWidget(instruction_title)
        instruction_layout.addWidget(instruction_text)
        
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(welcome)
        main_layout.addWidget(Line())
        main_layout.addWidget(menu_label)
        main_layout.addWidget(menu_container, 1)
        main_layout.addWidget(instruction_frame)
        main_layout.addStretch()

    def create_menu_button(self, text):
        button = QPushButton(text)
        # увеличенный минимальный размер чтобы текст не обрезался
        button.setMinimumSize(420, 70)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px 25px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                margin: 5px 0;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0d9468, stop:1 #0b766c);
            }}
        """)
        return button

    def show_assortment(self):
        self.parent().parent().show_car_catalog()
    
    def show_orders(self):
        self.parent().parent().show_orders_page()
    
    def show_reviews(self):
        self.parent().parent().show_reviews_page()
    
    def show_my_reviews(self):
        self.parent().parent().show_my_reviews_page()

class EmployeeMainMenuPage(QWidget):
    def __init__(self, user, logout_callback):
        super().__init__()
        self.user = user
        self.logout_callback = logout_callback
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 20)
        
        title = QLabel("AUTO DREAMS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 42px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 10px;
            font-family: 'Segoe UI';
        """)
        
        subtitle = QLabel("ПАНЕЛЬ СОТРУДНИКА")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            font-size: 20px;
            color: {COLORS['accent_teal']};
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        
        # Показываем ФИО сотрудника
        welcome_text = f"ДОБРО ПОЖАЛОВАТЬ, {self.user['first_name']} {self.user['last_name']}!"
        welcome = QLabel(welcome_text)
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet(f"""
            font-size: 18px;
            color: {COLORS['text_secondary']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        menu_container = QWidget()
        menu_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_green']};
            border-radius: 15px;
            padding: 30px;
        """)
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setAlignment(Qt.AlignCenter)
        menu_layout.setSpacing(15)
        
        menu_label = QLabel("ПАНЕЛЬ УПРАВЛЕНИЯ")
        menu_label.setAlignment(Qt.AlignCenter)
        menu_label.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        btn_manage_cars = self.create_menu_button("🚗 УПРАВЛЕНИЕ АВТОМОБИЛЯМИ")
        btn_view_all_cars = self.create_menu_button("📋 ВЕСЬ АССОРТИМЕНТ")
        btn_realtime_stats = self.create_menu_button("📊 СТАТИСТИКА В РЕАЛЬНОМ ВРЕМЕНИ")
        btn_exit = self.create_menu_button("🚪 ВЫХОД")
        
        btn_manage_cars.clicked.connect(self.show_manage_cars)
        btn_view_all_cars.clicked.connect(self.show_all_cars)
        btn_realtime_stats.clicked.connect(self.show_realtime_stats)
        btn_exit.clicked.connect(self.logout_callback)
        
        menu_layout.addWidget(btn_manage_cars)
        menu_layout.addWidget(btn_view_all_cars)
        menu_layout.addWidget(btn_realtime_stats)
        menu_layout.addWidget(btn_exit)
        
        instruction_frame = QFrame()
        instruction_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['secondary_bg']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 12px;
                margin-top: 30px;
                padding: 20px;
            }}
        """)
        
        instruction_layout = QVBoxLayout(instruction_frame)
        
        instruction_title = QLabel("ИНСТРУКЦИЯ СОТРУДНИКА")
        instruction_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {COLORS['accent_green']};
            margin-bottom: 10px;
            font-family: 'Segoe UI';
        """)
        
        instruction_text = QLabel(
            "• УПРАВЛЕНИЕ АВТОМОБИЛЯМИ - добавление, редактирование, удаление\n"
            "• ВЕСЬ АССОРТИМЕНТ - просмотр всех автомобилей (включая проданные)\n"  
            "• СТАТИСТИКА В РЕАЛЬНОМ ВРЕМЕНИ - актуальные данные о продажах\n"
            "• ВЫХОД - возврат к окну авторизации"
        )
        instruction_text.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; line-height: 1.5; font-family: 'Segoe UI';")
        
        instruction_layout.addWidget(instruction_title)
        instruction_layout.addWidget(instruction_text)
        
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(welcome)
        main_layout.addWidget(Line())
        main_layout.addWidget(menu_label)
        main_layout.addWidget(menu_container, 1)
        main_layout.addWidget(instruction_frame)
        main_layout.addStretch()

    def create_menu_button(self, text):
        button = QPushButton(text)
        # увеличенный минимальный размер чтобы текст не обрезался
        button.setMinimumSize(420, 70)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px 25px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                margin: 5px 0;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        return button

    def show_manage_cars(self):
        self.parent().parent().show_manage_cars_page()
    
    def show_all_cars(self):
        self.parent().parent().show_all_cars_page()
    
    def show_realtime_stats(self):
        self.parent().parent().show_realtime_stats_page()

class CarCatalogPage(QWidget):
    def __init__(self, user, back_callback):
        super().__init__()
        self.user = user
        self.back_callback = back_callback
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("КАТАЛОГ АВТОМОБИЛЕЙ")
        title.setStyleSheet(f"""
            font-size: 28px; 
            color: {COLORS['accent_green']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: {COLORS['secondary_bg']};
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['accent_green']};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {COLORS['accent_teal']};
            }}
        """)

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setAlignment(Qt.AlignTop)
        self.cards_layout.setHorizontalSpacing(15)
        self.cards_layout.setVerticalSpacing(15)
        self.cards_layout.setContentsMargins(10, 10, 10, 10)

        scroll_area.setWidget(self.cards_container)

        btn_back = QPushButton("◀ НАЗАД В МЕНЮ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_back.clicked.connect(self.back_callback)

        layout.addWidget(title)
        layout.addWidget(scroll_area)
        layout.addWidget(btn_back)

        self.load_cars()

    def load_cars(self):
        try:
            for i in reversed(range(self.cards_layout.count())): 
                widget = self.cards_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            
            cars = get_available_cars()
            
            if not cars:
                no_cars_label = QLabel("В НАСТОЯЩЕЕ ВРЕМЯ НЕТ ДОСТУПНЫХ АВТОМОБИЛЕЙ")
                no_cars_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 16px; font-family: 'Segoe UI';")
                no_cars_label.setAlignment(Qt.AlignCenter)
                self.cards_layout.addWidget(no_cars_label, 0, 0, 1, 3)
                return
            
            for i, car in enumerate(cars):
                row = i // 3
                col = i % 3
                car_card = CarCard(car, self.user, self.load_cars)
                self.cards_layout.addWidget(car_card, row, col)
                
        except Exception as e:
            QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось загрузить автомобили: {str(e)}")

class AllCarsPage(QWidget):
    def __init__(self, user, back_callback):
        super().__init__()
        self.user = user
        self.back_callback = back_callback
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("ВЕСЬ АССОРТИМЕНТ АВТОМОБИЛЕЙ")
        title.setStyleSheet(f"""
            font-size: 28px; 
            color: {COLORS['accent_green']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                gridline-color: {COLORS['border']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 8px;
                font-family: 'Segoe UI';
            }}
            QTableWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {COLORS['border']};
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_green']};
                color: {COLORS['text_primary']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                padding: 12px;
                font-weight: bold;
                border: none;
                font-family: 'Segoe UI';
            }}
        """)

        btn_back = QPushButton("◀ НАЗАД В МЕНЮ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_back.clicked.connect(self.back_callback)

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addWidget(btn_back)

        self.load_cars()

    def load_cars(self):
        try:
            cars = get_all_cars()
            
            self.table.setRowCount(len(cars))
            self.table.setColumnCount(7)
            self.table.setHorizontalHeaderLabels(["ID", "Марка", "Модель", "Год", "Цвет", "Цена", "Статус"])
            
            for row, car in enumerate(cars):
                self.table.setItem(row, 0, QTableWidgetItem(str(car['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(car['brand']))
                self.table.setItem(row, 2, QTableWidgetItem(car['model']))
                self.table.setItem(row, 3, QTableWidgetItem(str(car['year'])))
                self.table.setItem(row, 4, QTableWidgetItem(car['color']))
                self.table.setItem(row, 5, QTableWidgetItem(f"{car['price']:,.0f} ₽"))
                
                status_item = QTableWidgetItem(car['status'])
                if car['status'] == 'в наличии':
                    status_item.setForeground(QColor(COLORS['success']))
                else:
                    status_item.setForeground(QColor(COLORS['danger']))
                self.table.setItem(row, 6, status_item)
            
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
        except Exception as e:
            QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось загрузить автомобили: {str(e)}")

class ManageCarsPage(QWidget):
    def __init__(self, user, back_callback):
        super().__init__()
        self.user = user
        self.back_callback = back_callback
        self.setup_ui()
        # Загружаем таблицу при создании
        self.load_cars()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("УПРАВЛЕНИЕ АВТОМОБИЛЯМИ")
        title.setStyleSheet(f"""
            font-size: 28px; 
            color: {COLORS['accent_green']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # Форма добавления автомобиля
        form_container = QWidget()
        form_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_green']};
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
        """)
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(15)
        
        self.brand_edit = QLineEdit()
        self.brand_edit.setPlaceholderText("Например: Toyota")
        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText("Например: Camry")
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2030)
        self.year_spin.setValue(2024)
        self.vin_edit = QLineEdit()
        self.vin_edit.setPlaceholderText("17-значный VIN")
        self.color_edit = QLineEdit()
        self.color_edit.setPlaceholderText("Например: Черный")
        self.price_spin = QSpinBox()
        self.price_spin.setRange(0, 100000000)
        self.price_spin.setValue(1000000)
        self.price_spin.setSuffix(" ₽")
        self.mileage_spin = QSpinBox()
        self.mileage_spin.setRange(0, 1000000)
        self.mileage_spin.setValue(0)
        self.mileage_spin.setSuffix(" км")
        
        input_style = f"""
            QLineEdit, QSpinBox {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                padding: 10px;
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus, QSpinBox:focus {{
                border-color: {COLORS['accent_green']};
                background-color: {COLORS['secondary_bg']};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {COLORS['accent_green']};
                border: none;
                border-radius: 3px;
            }}
        """
        
        for edit in [self.brand_edit, self.model_edit, self.vin_edit, self.color_edit]:
            edit.setStyleSheet(input_style)
        self.year_spin.setStyleSheet(input_style)
        self.price_spin.setStyleSheet(input_style)
        self.mileage_spin.setStyleSheet(input_style)
        
        form_layout.addRow("Марка:", self.brand_edit)
        form_layout.addRow("Модель:", self.model_edit)
        form_layout.addRow("Год:", self.year_spin)
        form_layout.addRow("VIN:", self.vin_edit)
        form_layout.addRow("Цвет:", self.color_edit)
        form_layout.addRow("Цена:", self.price_spin)
        form_layout.addRow("Пробег:", self.mileage_spin)
        
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setStyleSheet(f"color: {COLORS['accent_green']}; font-size: 14px; font-family: 'Segoe UI'; font-weight: bold;")
        
        btn_add = QPushButton("➕ ДОБАВИТЬ АВТОМОБИЛЬ")
        btn_add.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_add.clicked.connect(self.add_car)
        
        # Таблица автомобилей
        self.table = QTableWidget()
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                gridline-color: {COLORS['border']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 8px;
                font-family: 'Segoe UI';
            }}
            QTableWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {COLORS['border']};
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_green']};
                color: {COLORS['text_primary']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                padding: 12px;
                font-weight: bold;
                border: none;
                font-family: 'Segoe UI';
            }}
        """)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        btn_edit = QPushButton("✏️ РЕДАКТИРОВАТЬ")
        btn_edit.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_edit.clicked.connect(self.edit_car)
        
        btn_delete = QPushButton("🗑️ УДАЛИТЬ")
        btn_delete.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: #dc2626;
            }}
        """)
        btn_delete.clicked.connect(self.delete_car)
        
        btn_refresh = QPushButton("🔄 ОБНОВИТЬ")
        btn_refresh.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_teal']};
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: #0f766e;
            }}
        """)
        btn_refresh.clicked.connect(self.load_cars)
        
        buttons_layout.addWidget(btn_edit)
        buttons_layout.addWidget(btn_delete)
        buttons_layout.addWidget(btn_refresh)
        buttons_layout.addStretch()
        
        btn_back = QPushButton("◀ НАЗАД В МЕНЮ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_back.clicked.connect(self.back_callback)
        
        layout.addWidget(title)
        layout.addWidget(form_container)
        layout.addWidget(btn_add)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)
        layout.addWidget(btn_back)
        
    def add_car(self):
        try:
            brand = self.brand_edit.text().strip()
            model = self.model_edit.text().strip()
            year = self.year_spin.value()
            vin = self.vin_edit.text().strip()
            color = self.color_edit.text().strip()
            price = self.price_spin.value()
            mileage = self.mileage_spin.value()
            
            if not brand or not model or not vin or not color:
                QMessageBox.warning(self, "ВНИМАНИЕ", "Заполните все поля.")
                return
                
            if len(vin) != 17:
                QMessageBox.warning(self, "ВНИМАНИЕ", "VIN должен содержать 17 символов.")
                return

            # Проверяем наличие изображения в папке images перед добавлением
            images_path = os.path.join(os.path.dirname(__file__), "images")
            if not os.path.exists(images_path):
                # если папки нет — считаем, что изображения нет
                QMessageBox.warning(self, "ВНИМАНИЕ", "Папка images не найдена. Поместите изображение в папку 'images'.")
                return

            # Возможные имена изображений (brand_model в нижнем регистре)
            normalized_brand = brand.strip().lower().replace(" ", "_")
            normalized_model = model.strip().lower().replace(" ", "_")
            possible_filenames = [
                f"{normalized_brand}_{normalized_model}.jpg",
                f"{normalized_brand}_{normalized_model}.png",
                f"{normalized_brand}_{normalized_model}.jpeg",
                f"{normalized_brand}-{normalized_model}.jpg",
                f"{normalized_brand}-{normalized_model}.png",
                f"{normalized_brand}{normalized_model}.jpg",
                f"{normalized_brand}{normalized_model}.png"
            ]
            image_found = False
            for fn in possible_filenames:
                if os.path.exists(os.path.join(images_path, fn)):
                    image_found = True
                    break

            if not image_found:
                QMessageBox.warning(self, "ВНИМАНИЕ", 
                    f"Изображение для {brand} {model} не найдено в папке 'images'.\n"
                    f"Имена файлов, принимаемые системой: {', '.join(possible_filenames[:3])}\n"
                    "Пожалуйста, добавьте фото и повторите.")
                return
            
            # Если изображение есть — добавляем автомобиль
            add_car(brand, model, year, vin, color, price, mileage)
            QMessageBox.information(self, "✅ УСПЕХ", "Автомобиль успешно добавлен!")
            
            # Очищаем форму
            self.brand_edit.clear()
            self.model_edit.clear()
            self.vin_edit.clear()
            self.color_edit.clear()
            self.price_spin.setValue(1000000)
            self.mileage_spin.setValue(0)
            
            # Обновляем таблицу (real-time визуальный отклик)
            self.load_cars()
            
        except Exception as e:
            QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось добавить автомобиль: {str(e)}")

    def edit_car(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "ВНИМАНИЕ", "Выберите автомобиль для редактирования.")
            return
        car_id = int(self.table.item(selected_row, 0).text())
        car = get_car_by_id(car_id)
        if not car:
            QMessageBox.critical(self, "❌ ОШИБКА", "Не удалось загрузить данные автомобиля.")
            return
        # Диалог редактирования (как у тебя был)...
        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование автомобиля")
        dialog.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        dialog.setFixedSize(400, 500)
        layout = QVBoxLayout(dialog)
        title = QLabel("РЕДАКТИРОВАНИЕ АВТОМОБИЛЯ")
        title.setStyleSheet(f"""
            font-size: 20px; 
            color: {COLORS['accent_green']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        brand_edit = QLineEdit(car['brand'])
        model_edit = QLineEdit(car['model'])
        year_spin = QSpinBox()
        year_spin.setRange(2000, 2030)
        year_spin.setValue(car['year'])
        vin_edit = QLineEdit(car['vin'])
        color_edit = QLineEdit(car['color'])
        price_spin = QSpinBox()
        price_spin.setRange(0, 100000000)
        price_spin.setValue(int(car['price']))
        price_spin.setSuffix(" ₽")
        mileage_spin = QSpinBox()
        mileage_spin.setRange(0, 1000000)
        mileage_spin.setValue(car['mileage'])
        mileage_spin.setSuffix(" км")
        input_style = f"""
            QLineEdit, QSpinBox {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                padding: 10px;
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }}
        """
        for edit in [brand_edit, model_edit, vin_edit, color_edit]:
            edit.setStyleSheet(input_style)
        year_spin.setStyleSheet(input_style)
        price_spin.setStyleSheet(input_style)
        mileage_spin.setStyleSheet(input_style)
        form_layout.addRow("Марка:", brand_edit)
        form_layout.addRow("Модель:", model_edit)
        form_layout.addRow("Год:", year_spin)
        form_layout.addRow("VIN:", vin_edit)
        form_layout.addRow("Цвет:", color_edit)
        form_layout.addRow("Цена:", price_spin)
        form_layout.addRow("Пробег:", mileage_spin)
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setStyleSheet(f"color: {COLORS['accent_green']}; font-size: 14px; font-family: 'Segoe UI'; font-weight: bold;")
        btn_save = QPushButton("💾 СОХРАНИТЬ")
        btn_save.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_cancel = QPushButton("❌ ОТМЕНА")
        btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: #dc2626;
            }}
        """)
        def save_changes():
            try:
                # если бренд или модель поменялись, стоит предупредить о соответствии фото отдельно (но мы просто обновляем данные)
                update_car(
                    car_id,
                    brand_edit.text().strip(),
                    model_edit.text().strip(),
                    year_spin.value(),
                    vin_edit.text().strip(),
                    color_edit.text().strip(),
                    price_spin.value(),
                    mileage_spin.value()
                )
                QMessageBox.information(dialog, "✅ УСПЕХ", "Данные автомобиля обновлены!")
                dialog.accept()
                self.load_cars()
            except Exception as e:
                QMessageBox.critical(dialog, "❌ ОШИБКА", f"Не удалось обновить данные: {str(e)}")
        btn_save.clicked.connect(save_changes)
        btn_cancel.clicked.connect(dialog.reject)
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(btn_save)
        layout.addWidget(btn_cancel)
        if dialog.exec() == QDialog.Accepted:
            self.load_cars()

    def delete_car(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "ВНИМАНИЕ", "Выберите автомобиль для удаления.")
            return
        car_id = int(self.table.item(selected_row, 0).text())
        brand = self.table.item(selected_row, 1).text()
        model = self.table.item(selected_row, 2).text()
        reply = QMessageBox.question(
            self, 
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить автомобиль {brand} {model}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                delete_car(car_id)
                QMessageBox.information(self, "✅ УСПЕХ", "Автомобиль успешно удален!")
                self.load_cars()
            except Exception as e:
                QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось удалить автомобиль: {str(e)}")

    def load_cars(self):
        try:
            cars = get_all_cars()
            self.table.setRowCount(len(cars))
            self.table.setColumnCount(8)
            self.table.setHorizontalHeaderLabels(["ID", "Марка", "Модель", "Год", "VIN", "Цвет", "Цена", "Статус"])
            for row, car in enumerate(cars):
                self.table.setItem(row, 0, QTableWidgetItem(str(car['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(car['brand']))
                self.table.setItem(row, 2, QTableWidgetItem(car['model']))
                self.table.setItem(row, 3, QTableWidgetItem(str(car['year'])))
                self.table.setItem(row, 4, QTableWidgetItem(car['vin']))
                self.table.setItem(row, 5, QTableWidgetItem(car['color']))
                self.table.setItem(row, 6, QTableWidgetItem(f"{car['price']:,.0f} ₽"))
                status_item = QTableWidgetItem(car['status'])
                if car['status'] == 'в наличии':
                    status_item.setForeground(QColor(COLORS['success']))
                else:
                    status_item.setForeground(QColor(COLORS['danger']))
                self.table.setItem(row, 7, status_item)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        except Exception as e:
            QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось загрузить автомобили: {str(e)}")

class RealtimeStatsPage(QWidget):
    def __init__(self, user, back_callback):
        super().__init__()
        self.user = user
        self.back_callback = back_callback
        self.setup_ui()

    def get_realtime_stats(self):
        """Получение статистики в реальном времени"""
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM CARS")
            total_cars = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM CARS WHERE status = 'в наличии'")
            available_cars = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM CARS WHERE status = 'продан'")
            sold_cars = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM ORDERS")
            total_orders = cursor.fetchone()[0]
            cursor.execute("SELECT SUM(final_price) FROM ORDERS")
            total_revenue = cursor.fetchone()[0] or 0
            cursor.execute("SELECT COUNT(*) FROM CLIENTS")
            total_clients = cursor.fetchone()[0]
            conn.close()
            stats = [
                ("Всего автомобилей", total_cars, COLORS['accent_green']),
                ("В наличии", available_cars, COLORS['success']),
                ("Продано", sold_cars, COLORS['accent_teal']),
                ("Всего заказов", total_orders, COLORS['accent_green']),
                ("Общая выручка", f"{total_revenue:,.0f} ₽", COLORS['success']),
                ("Всего клиентов", total_clients, COLORS['accent_teal'])
            ]
            return stats
        except Exception as e:
            print(f"❌ Ошибка получения статистики: {e}")
            raise Exception(f"Не удалось загрузить статистику: {str(e)}")

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("СТАТИСТИКА В РЕАЛЬНОМ ВРЕМЕНИ")
        title.setStyleSheet(f"""
            font-size: 28px; 
            color: {COLORS['accent_green']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)
        
        try:
            stats_container = QWidget()
            stats_container.setStyleSheet(f"""
                background-color: {COLORS['secondary_bg']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 12px;
                padding: 25px;
            """)
            stats_layout = QGridLayout(stats_container)
            stats_layout.setSpacing(15)
            stats = self.get_realtime_stats()
            stats_widgets = []
            for i, (label, value, color) in enumerate(stats):
                stat_widget = QWidget()
                stat_widget.setStyleSheet(f"""
                    background-color: {COLORS['primary_bg']};
                    border: 2px solid {color};
                    border-radius: 8px;
                    padding: 15px;
                """)
                stat_layout = QVBoxLayout(stat_widget)
                value_label = QLabel(str(value))
                value_label.setStyleSheet(f"""
                    color: {color};
                    font-size: 24px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                """)
                value_label.setAlignment(Qt.AlignCenter)
                name_label = QLabel(label)
                name_label.setStyleSheet(f"""
                    color: {COLORS['text_secondary']};
                    font-size: 14px;
                    font-family: 'Segoe UI';
                """)
                name_label.setAlignment(Qt.AlignCenter)
                stat_layout.addWidget(value_label)
                stat_layout.addWidget(name_label)
                stats_widgets.append(stat_widget)
            for i, widget in enumerate(stats_widgets):
                row = i // 3
                col = i % 3
                stats_layout.addWidget(widget, row, col)
            layout.addWidget(title)
            layout.addWidget(stats_container)
        except Exception as e:
            error_label = QLabel(f"❌ Не удалось загрузить статистику:\n{str(e)}")
            error_label.setStyleSheet(f"color: {COLORS['danger']}; font-size: 16px; font-family: 'Segoe UI';")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            layout.addWidget(error_label)
        
        btn_refresh = QPushButton("🔄 ОБНОВИТЬ СТАТИСТИКУ")
        btn_refresh.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 15px 0;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_refresh.clicked.connect(self.refresh_stats)
        
        btn_back = QPushButton("◀ НАЗАД В МЕНЮ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_back.clicked.connect(self.back_callback)
        
        layout.addWidget(btn_refresh)
        layout.addWidget(btn_back)
        layout.addStretch()

    def refresh_stats(self):
        self.parent().parent().show_realtime_stats_page()

class OrdersPage(QWidget):
    def __init__(self, user, back_callback):
        super().__init__()
        self.user = user
        self.back_callback = back_callback
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("МОИ ЗАКАЗЫ")
        title.setStyleSheet(f"""
            font-size: 28px; 
            color: {COLORS['accent_green']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: {COLORS['secondary_bg']};
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['accent_green']};
                min-height: 20px;
                border-radius: 5px;
            }}
        """)
        
        self.orders_container = QWidget()
        self.orders_layout = QGridLayout(self.orders_container)
        self.orders_layout.setAlignment(Qt.AlignTop)
        self.orders_layout.setHorizontalSpacing(15)
        self.orders_layout.setVerticalSpacing(15)
        self.orders_layout.setContentsMargins(10, 10, 10, 10)
        scroll_area.setWidget(self.orders_container)
        
        btn_back = QPushButton("◀ НАЗАД В МЕНЮ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_back.clicked.connect(self.back_callback)
        
        layout.addWidget(title)
        layout.addWidget(scroll_area)
        layout.addWidget(btn_back)
        
        self.load_orders()

    def load_orders(self):
        try:
            for i in reversed(range(self.orders_layout.count())): 
                widget = self.orders_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            
            client_id = get_or_create_client_for_user(self.user['id'], self.user['username'])
            orders = get_client_orders(client_id)
            
            if not orders:
                no_orders_label = QLabel("У ВАС ПОКА НЕТ ЗАКАЗОВ")
                no_orders_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 16px; font-family: 'Segoe UI';")
                no_orders_label.setAlignment(Qt.AlignCenter)
                self.orders_layout.addWidget(no_orders_label, 0, 0, 1, 3)
                return
            
            for i, order in enumerate(orders):
                row = i // 3
                col = i % 3
                order_card = OrderCard(order)
                self.orders_layout.addWidget(order_card, row, col)
            
        except Exception as e:
            QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось загрузить заказы: {str(e)}")

class ReviewsPage(QWidget):
    def __init__(self, user, back_callback):
        super().__init__()
        self.user = user
        self.back_callback = back_callback
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("ОСТАВИТЬ ОТЗЫВ")
        title.setStyleSheet(f"""
            font-size: 28px; 
            color: {COLORS['accent_green']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)
        
        form_container = QWidget()
        form_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_green']};
            border-radius: 12px;
            padding: 25px;
        """)
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(15)
        
        self.order_id_edit = QLineEdit()
        self.order_id_edit.setPlaceholderText("Введите ID заказа")
        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(1, 5)
        self.rating_spin.setValue(5)
        self.comment_edit = QTextEdit()
        self.comment_edit.setPlaceholderText("Напишите ваш отзыв...")
        self.comment_edit.setMaximumHeight(100)
        
        input_style = f"""
            QLineEdit, QSpinBox, QTextEdit {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                padding: 10px;
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus, QSpinBox:focus, QTextEdit:focus {{
                border-color: {COLORS['accent_green']};
                background-color: {COLORS['secondary_bg']};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {COLORS['accent_green']};
                border: none;
                border-radius: 3px;
            }}
        """
        
        self.order_id_edit.setStyleSheet(input_style)
        self.rating_spin.setStyleSheet(input_style)
        self.comment_edit.setStyleSheet(input_style)
        
        form_layout.addRow("ID заказа:", self.order_id_edit)
        form_layout.addRow("Оценка (1-5):", self.rating_spin)
        form_layout.addRow("Комментарий:", self.comment_edit)
        
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setStyleSheet(f"color: {COLORS['accent_green']}; font-size: 14px; font-family: 'Segoe UI'; font-weight: bold;")
        
        btn_submit = QPushButton("📝 ОТПРАВИТЬ ОТЗЫВ")
        btn_submit.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_submit.clicked.connect(self.submit_review)
        
        btn_back = QPushButton("◀ НАЗАД В МЕНЮ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_green']};
                border: 2px solid {COLORS['accent_green']};
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_green']};
                color: {COLORS['text_primary']};
            }}
        """)
        btn_back.clicked.connect(self.back_callback)
        
        layout.addWidget(title)
        layout.addWidget(form_container)
        layout.addWidget(btn_submit)
        layout.addWidget(btn_back)
        layout.addStretch()

    def submit_review(self):
        try:
            order_id = int(self.order_id_edit.text())
            rating = self.rating_spin.value()
            comment = self.comment_edit.toPlainText().strip()
            
            if not order_id or not comment:
                QMessageBox.warning(self, "ВНИМАНИЕ", "Заполните все поля.")
                return
            
            client_id = get_or_create_client_for_user(self.user['id'], self.user['username'])
            
            add_review(client_id, order_id, rating, comment)
            QMessageBox.information(self, "✅ УСПЕХ", "Отзыв успешно добавлен!")
            
            self.order_id_edit.clear()
            self.rating_spin.setValue(5)
            self.comment_edit.clear()
            
        except ValueError:
            QMessageBox.warning(self, "❌ ОШИБКА", "Введите корректный ID заказа.")
        except Exception as e:
            QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось добавить отзыв: {str(e)}")

class MyReviewsPage(QWidget):
    def __init__(self, user, back_callback):
        super().__init__()
        self.user = user
        self.back_callback = back_callback
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("МОИ ОТЗЫВЫ")
        title.setStyleSheet(f"""
            font-size: 28px; 
            color: {COLORS['accent_green']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)
        
        self.table = QTableWidget()
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                gridline-color: {COLORS['border']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 8px;
                font-family: 'Segoe UI';
            }}
            QTableWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {COLORS['border']};
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_green']};
                color: {COLORS['text_primary']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                padding: 12px;
                font-weight: bold;
                border: none;
                font-family: 'Segoe UI';
            }}
        """)
        
        btn_back = QPushButton("◀ НАЗАД В МЕНЮ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        btn_back.clicked.connect(self.back_callback)
        
        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addWidget(btn_back)
        
        self.load_reviews()

    def load_reviews(self):
        try:
            client_id = get_or_create_client_for_user(self.user['id'], self.user['username'])
            reviews = get_client_reviews(client_id)
            
            self.table.setRowCount(len(reviews))
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["Заказ", "Оценка", "Комментарий", "Дата"])
            
            for row, review in enumerate(reviews):
                self.table.setItem(row, 0, QTableWidgetItem(f"Заказ #{review['order_id']}"))
                
                rating_stars = "★" * review['rating'] + "☆" * (5 - review['rating'])
                self.table.setItem(row, 1, QTableWidgetItem(rating_stars))
                
                comment = review['comment'] if review['comment'] else "Без комментария"
                self.table.setItem(row, 2, QTableWidgetItem(comment))
                self.table.setItem(row, 3, QTableWidgetItem(str(review['review_date'])))
            
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.resizeColumnToContents(1)
            
        except Exception as e:
            QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось загрузить отзывы: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AUTO DREAMS - ПРЕМИАЛЬНЫЕ АВТОМОБИЛИ")
        self.setMinimumSize(1200, 800)
        self.resize(1200, 800)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['primary_bg']};
            }}
            QMessageBox {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['accent_green']};
                border-radius: 12px;
                font-family: 'Segoe UI';
            }}
            QMessageBox QLabel {{
                color: {COLORS['text_primary']};
            }}
            QMessageBox QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_green']}, stop:1 {COLORS['accent_teal']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QMessageBox QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0ea271, stop:1 #0c857a);
            }}
        """)
        
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        
        self.login_page = LoginPage(
            on_login_success=self.handle_login_success,
            go_register=self.show_register
        )
        
        self.register_page = RegisterPage(go_login=self.show_login)
        
        self.stacked.addWidget(self.login_page)
        self.stacked.addWidget(self.register_page)
        
        self.show_login()
    
    def show_login(self):
        self.stacked.setCurrentWidget(self.login_page)
    
    def show_register(self):
        self.stacked.setCurrentWidget(self.register_page)
    
    def handle_login_success(self, user):
        self.user = user
        
        if user['role'] == 'employee' or user['role'] == 'admin':
            self.main_menu = EmployeeMainMenuPage(user, logout_callback=self.show_login)
        else:
            self.main_menu = ClientMainMenuPage(user, logout_callback=self.show_login)
            
        self.stacked.addWidget(self.main_menu)
        self.stacked.setCurrentWidget(self.main_menu)
    
    def show_car_catalog(self):
        self.car_catalog = CarCatalogPage(self.user, back_callback=self.show_main_menu)
        self.stacked.addWidget(self.car_catalog)
        self.stacked.setCurrentWidget(self.car_catalog)
    
    def show_all_cars_page(self):
        self.all_cars = AllCarsPage(self.user, back_callback=self.show_main_menu)
        self.stacked.addWidget(self.all_cars)
        self.stacked.setCurrentWidget(self.all_cars)
    
    def show_manage_cars_page(self):
        self.manage_cars = ManageCarsPage(self.user, back_callback=self.show_main_menu)
        self.stacked.addWidget(self.manage_cars)
        self.stacked.setCurrentWidget(self.manage_cars)
    
    def show_realtime_stats_page(self):
        self.realtime_stats = RealtimeStatsPage(self.user, back_callback=self.show_main_menu)
        self.stacked.addWidget(self.realtime_stats)
        self.stacked.setCurrentWidget(self.realtime_stats)
    
    def show_orders_page(self):
        self.orders_page = OrdersPage(self.user, back_callback=self.show_main_menu)
        self.stacked.addWidget(self.orders_page)
        self.stacked.setCurrentWidget(self.orders_page)
    
    def show_reviews_page(self):
        self.reviews_page = ReviewsPage(self.user, back_callback=self.show_main_menu)
        self.stacked.addWidget(self.reviews_page)
        self.stacked.setCurrentWidget(self.reviews_page)
    
    def show_my_reviews_page(self):
        self.my_reviews_page = MyReviewsPage(self.user, back_callback=self.show_main_menu)
        self.stacked.addWidget(self.my_reviews_page)
        self.stacked.setCurrentWidget(self.my_reviews_page)
    
    def show_main_menu(self):
        self.stacked.setCurrentWidget(self.main_menu)

if __name__ == "__main__":
    try:
        init_db()
        init_car_db()
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")
        QMessageBox.critical(None, "Ошибка запуска", f"Не удалось запустить приложение:\n{str(e)}")