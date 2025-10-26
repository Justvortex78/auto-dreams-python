import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QStackedWidget, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QSpinBox,
    QScrollArea, QGridLayout
)
from PySide6.QtGui import QFont, QPixmap, QColor
from auth_db import init_db, create_user, find_user_by_login_or_email, verify_password
from car_db import get_all_cars, get_client_orders, add_review, get_client_reviews, create_order, get_or_create_client_for_user

# Цветовая палитра нового дизайна
COLORS = {
    'primary_bg': '#0f1117',
    'secondary_bg': '#1a1d29',
    'accent_blue': '#3b82f6',
    'accent_purple': '#8b5cf6',
    'text_primary': '#f1f5f9',
    'text_secondary': '#94a3b8',
    'success': '#10b981',
    'danger': '#ef4444',
    'border': '#334155'
}

class Line(QWidget):
    def __init__(self):
        super().__init__()
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {COLORS['accent_blue']}; height: 2px;")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 8, 0, 8)
        lay.addWidget(line)

class RegisterPage(QWidget):
    def __init__(self, go_login):
        super().__init__()
        self.go_login = go_login
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(100, 50, 100, 50)
        
        title = QLabel("РЕГИСТРАЦИЯ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {COLORS['accent_blue']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        # Контейнер формы
        form_container = QWidget()
        form_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_blue']};
            border-radius: 15px;
            padding: 30px;
        """)
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(20)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Введите логин (мин. 3 символа)")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Введите email")
        self.pass1_edit = QLineEdit()
        self.pass1_edit.setPlaceholderText("Введите пароль (мин. 6 символов)")
        self.pass2_edit = QLineEdit()
        self.pass2_edit.setPlaceholderText("Повторите пароль")
        
        # Стиль для полей ввода
        input_style = f"""
            QLineEdit {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                padding: 12px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 14px;
                margin: 5px 0;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus {{
                border-color: {COLORS['accent_blue']};
                background-color: {COLORS['secondary_bg']};
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_secondary']};
            }}
        """
        
        for edit in [self.username_edit, self.email_edit, self.pass1_edit, self.pass2_edit]:
            edit.setStyleSheet(input_style)
        
        self.pass1_edit.setEchoMode(QLineEdit.Password)
        self.pass2_edit.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("ЛОГИН:", self.username_edit)
        form_layout.addRow("EMAIL:", self.email_edit)
        form_layout.addRow("ПАРОЛЬ:", self.pass1_edit)
        form_layout.addRow("ПОВТОР ПАРОЛЯ:", self.pass2_edit)
        
        # Стиль для меток формы
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setStyleSheet(f"color: {COLORS['accent_blue']}; font-size: 14px; font-family: 'Segoe UI'; font-weight: bold;")
        
        btn_create = QPushButton("СОЗДАТЬ АККАУНТ")
        btn_create.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1d4ed8, stop:1 #6d28d9);
            }}
            QPushButton:disabled {{
                background-color: #555555;
                color: #888888;
            }}
        """)
        btn_create.clicked.connect(self.handle_register)
        
        btn_back = QPushButton("◀ НАЗАД К ВХОДУ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_blue']};
                border: 2px solid {COLORS['accent_blue']};
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                margin-top: 15px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_blue']};
                color: {COLORS['text_primary']};
            }}
        """)
        btn_back.clicked.connect(self.go_login)
        
        main_layout.addWidget(title)
        main_layout.addWidget(form_container)
        main_layout.addWidget(btn_create)
        main_layout.addWidget(btn_back)
        main_layout.addStretch()

    def handle_register(self):
        u = self.username_edit.text().strip()
        e = self.email_edit.text().strip()
        p1 = self.pass1_edit.text()
        p2 = self.pass2_edit.text()

        if not u or not e or not p1 or not p2:
            QMessageBox.warning(self, "ВНИМАНИЕ", "Заполните все поля.")
            return
            
        if len(u) < 3:
            QMessageBox.warning(self, "ВНИМАНИЕ", "Логин должен быть не короче 3 символов.")
            return
            
        if len(p1) < 6:
            QMessageBox.warning(self, "ВНИМАНИЕ", "Пароль должен быть не короче 6 символов.")
            return
            
        if p1 != p2:
            QMessageBox.critical(self, "❌ ОШИБКА", "Пароли не совпадают.")
            return

        try:
            create_user(u, e, p1)
            QMessageBox.information(self, "✅ УСПЕХ", "Аккаунт создан. Теперь войдите.")
            self.go_login()
            
        except Exception as err:
            error_msg = str(err)
            if "username" in error_msg.lower():
                QMessageBox.critical(self, "❌ ОШИБКА", "Логин уже занят.")
            elif "email" in error_msg.lower():
                QMessageBox.critical(self, "❌ ОШИБКА", "Email уже зарегистрирован.")
            else:
                QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось создать пользователя: {error_msg}")

class LoginPage(QWidget):
    def __init__(self, on_login_success, go_register):
        super().__init__()
        self.on_login_success = on_login_success
        self.go_register = go_register
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        
        # Левая панель - форма авторизации
        left_panel = QWidget()
        left_panel.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_blue']};
            border-radius: 15px;
            margin: 20px;
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)
        
        # Заголовок
        title = QLabel("АВТОРИЗАЦИЯ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {COLORS['accent_blue']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        # Поля ввода
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setSpacing(20)
        
        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Введите логин или email")
        self.login_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                padding: 12px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus {{
                border-color: {COLORS['accent_blue']};
                background-color: {COLORS['secondary_bg']};
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_secondary']};
            }}
        """)
        
        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("Введите пароль")
        self.pass_edit.setEchoMode(QLineEdit.Password)
        self.pass_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                padding: 12px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus {{
                border-color: {COLORS['accent_blue']};
                background-color: {COLORS['secondary_bg']};
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_secondary']};
            }}
        """)
        
        form_layout.addRow("Логин/Email:", self.login_edit)
        form_layout.addRow("Пароль:", self.pass_edit)
        
        # Стиль для меток формы
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setStyleSheet(f"color: {COLORS['accent_blue']}; font-size: 14px; font-family: 'Segoe UI'; font-weight: bold;")
        
        # Кнопка входа
        btn_login = QPushButton("ВОЙТИ")
        btn_login.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
                color: {COLORS['text_primary']};
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1d4ed8, stop:1 #6d28d9);
            }}
        """)
        btn_login.clicked.connect(self.handle_login)
        
        # Кнопка регистрации
        btn_register = QPushButton("СОЗДАТЬ АККАУНТ")
        btn_register.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_blue']};
                border: 2px solid {COLORS['accent_blue']};
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_blue']};
                color: {COLORS['text_primary']};
            }}
        """)
        btn_register.clicked.connect(self.go_register)
        
        # Демо доступ
        demo_label = QLabel("Демо доступ: vortex / vortex")
        demo_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 12px;
            margin-top: 20px;
            text-align: center;
            font-family: 'Segoe UI';
        """)
        
        # Собираем левую панель
        left_layout.addWidget(title)
        left_layout.addLayout(form_layout)
        left_layout.addWidget(btn_login)
        left_layout.addWidget(btn_register)
        left_layout.addWidget(demo_label)
        left_layout.addStretch()
        
        # Правая панель - логотип и слоган
        right_panel = QWidget()
        right_panel.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_blue']};
            border-radius: 15px;
            margin: 20px;
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # Логотип
        logo_label = QLabel("AUTO DREAMS")
        logo_label.setStyleSheet(f"""
            color: {COLORS['accent_blue']};
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        
        # Слоган
        slogan_label = QLabel("ПРЕМИАЛЬНЫЕ АВТОМОБИЛИ")
        slogan_label.setStyleSheet(f"""
            color: {COLORS['accent_purple']};
            font-size: 18px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """)
        
        # Декор
        decor_label = QLabel("🚗 💨 ✨")
        decor_label.setStyleSheet(f"""
            color: {COLORS['accent_blue']};
            font-size: 24px;
            margin-top: 20px;
        """)
        
        right_layout.addWidget(logo_label)
        right_layout.addWidget(slogan_label)
        right_layout.addWidget(decor_label)
        right_layout.addStretch()
        
        # Распределение пространства
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)

    def handle_login(self):
        login = self.login_edit.text().strip()
        password = self.pass_edit.text()
        
        if not login or not password:
            QMessageBox.warning(self, "Внимание", "Введите логин и пароль.")
            return
            
        # Демо доступ
        if login == "vortex" and password == "vortex":
            demo_user = {'username': 'Демо пользователь', 'id': 1}
            self.on_login_success(demo_user)
            return
            
        user = find_user_by_login_or_email(login)
        if not user:
            QMessageBox.critical(self, "Ошибка входа", "Пользователь не найден.")
            return
            
        if not verify_password(password, user["password_hash"]):
            QMessageBox.critical(self, "Ошибка входа", "Неверный пароль.")
            return
            
        self.on_login_success(user)

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
                border-color: {COLORS['accent_blue']};
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
        
        # Загружаем изображение
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
                    color: {COLORS['accent_blue']};
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                }}
            """)

        # Марка и модель
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

        # VIN номер
        vin_label = QLabel(f"VIN: {self.car['vin'][:8]}...")
        vin_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-family: 'Segoe UI';")
        vin_label.setAlignment(Qt.AlignCenter)

        # Цена
        price_label = QLabel(f"{self.car['price']:,.0f} ₽")
        price_label.setStyleSheet(f"""
            color: {COLORS['accent_blue']}; 
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

        # Статус
        status_label = QLabel(f"Статус: {self.car['status']}")
        status_color = COLORS['success'] if self.car['status'] == 'в наличии' else COLORS['danger']
        status_label.setStyleSheet(f"color: {status_color}; font-size: 12px; font-weight: bold; font-family: 'Segoe UI';")
        status_label.setAlignment(Qt.AlignCenter)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        btn_details = QPushButton("🔍")
        btn_details.setToolTip("Подробнее")
        btn_details.setFixedSize(40, 35)
        btn_details.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_blue']};
                border: 1px solid {COLORS['accent_blue']};
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_blue']};
                color: {COLORS['text_primary']};
            }}
        """)
        btn_details.clicked.connect(self.show_details)

        btn_buy = QPushButton("КУПИТЬ" if self.car['status'] == 'в наличии' else "ПРОДАНО")
        btn_buy.setEnabled(self.car['status'] == 'в наличии')
        btn_buy.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
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
        """Загружаем изображение автомобиля из папки images"""
        try:
            images_path = os.path.join(os.path.dirname(__file__), "images")
            
            if not os.path.exists(images_path):
                os.makedirs(images_path)
                print(f"Создана папка для изображений: {images_path}")
                return None
            
            brand_clean = self.car['brand'].replace(' ', '_').replace('-', '_')
            model_clean = self.car['model'].replace(' ', '_').replace('-', '_')
            possible_filenames = [
                f"{brand_clean}_{model_clean}.jpg",
                f"{brand_clean}_{model_clean}.png",
                f"{self.car['brand']}_{self.car['model']}.jpg",
                f"{self.car['brand']}_{self.car['model']}.png",
            ]
            
            for filename in possible_filenames:
                image_path = os.path.join(images_path, filename)
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        print(f"Загружено изображение: {filename}")
                        return pixmap
            
            print(f"Не найдено изображение для: {self.car['brand']} {self.car['model']}")
            return None
            
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            return None

    def show_details(self):
        msg = QMessageBox()
        msg.setWindowTitle(f"🚗 {self.car['brand']} {self.car['model']}")
        msg.setText(f"""
<b style='color: {COLORS['accent_blue']};'>ДЕТАЛЬНАЯ ИНФОРМАЦИЯ:</b>

<b>Марка:</b> {self.car['brand']}
<b>Модель:</b> {self.car['model']}
<b>VIN:</b> {self.car['vin']}
<b>Цена:</b> {self.car['price']:,.0f} ₽
<b>Статус:</b> {self.car['status']}

<b>Описание:</b>
{self.get_car_description()}
        """)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['accent_blue']};
                border-radius: 12px;
                font-family: 'Segoe UI';
            }}
            QMessageBox QLabel {{
                color: {COLORS['text_primary']};
                font-size: 14px;
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
        """)
        msg.exec()

    def get_car_description(self):
        descriptions = {
            'Toyota Camry': 'Стильный седан • Надежность • Комфорт',
            'Honda CR-V': 'Практичный кроссовер • Экономичность • Простор',
            'BMW X5': 'Премиальный внедорожник • Динамика • Роскошь',
            'Mercedes E-Class': 'Бизнес-класс • Комфорт • Технологии',
            'Audi Q7': 'Семейный внедорожник • Качество • Безопасность',
            'Lexus RX': 'Премиум-кроссовер • Тишина • Надежность',
            'Hyundai Tucson': 'Современный дизайн • Гарантия • Оснащение',
            'Kia Sportage': 'Стильный кроссовер • Цена/Качество • Гарантия'
        }
        
        key = f"{self.car['brand']} {self.car['model']}"
        return descriptions.get(key, "Качественный автомобиль • Надежность • Комфорт")

    def buy_car(self):
        if self.car['status'] != 'в наличии':
            QMessageBox.warning(self, "Внимание", "Этот автомобиль уже продан.")
            return
            
        reply = QMessageBox()
        reply.setWindowTitle("🎯 ПОДТВЕРЖДЕНИЕ ПОКУПКИ")
        reply.setText(f"""
<b style='color: {COLORS['accent_blue']};'>ПОДТВЕРДИТЕ ПОКУПКУ:</b>

{self.car['brand']} {self.car['model']}

<b>ЦЕНА: {self.car['price']:,.0f} ₽</b>

✅ Гарантия 3 года
✅ Бесплатная доставка  
✅ Первое ТО в подарок
        """)
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply.setDefaultButton(QMessageBox.No)
        reply.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['secondary_bg']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['accent_blue']};
                border-radius: 12px;
                font-family: 'Segoe UI';
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
        """)
        
        result = reply.exec()
        
        if result == QMessageBox.Yes:
            try:
                client_id = get_or_create_client_for_user(self.user['id'], self.user['username'])
                create_order(client_id, self.car['id'], 1, self.car['price'])
                
                success_msg = QMessageBox()
                success_msg.setWindowTitle("🎉 ПОЗДРАВЛЯЕМ!")
                success_msg.setText(f"""
<b style='color: {COLORS['accent_blue']};'>ПОКУПКА УСПЕШНО ОФОРМЛЕНА!</b>

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
                        border: 2px solid {COLORS['accent_blue']};
                        border-radius: 12px;
                        font-family: 'Segoe UI';
                    }}
                    QPushButton {{
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                            stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
                        color: {COLORS['text_primary']};
                        border: none;
                        padding: 8px 16px;
                        border-radius: 6px;
                        font-weight: bold;
                        font-family: 'Segoe UI';
                    }}
                    QPushButton:hover {{
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                            stop:0 #2563eb, stop:1 #7c3aed);
                    }}
                """)
                success_msg.exec()
                
                self.on_buy_callback()
                
            except Exception as e:
                QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось оформить покупку: {str(e)}")

class MainMenuPage(QWidget):
    def __init__(self, user, logout_callback):
        super().__init__()
        self.user = user
        self.logout_callback = logout_callback
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLORS['primary_bg']};")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 20)
        
        # Заголовок
        title = QLabel("AUTO DREAMS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 42px;
            font-weight: bold;
            color: {COLORS['accent_blue']};
            margin-bottom: 10px;
            font-family: 'Segoe UI';
        """)
        
        subtitle = QLabel("ПРЕМИАЛЬНЫЕ АВТОМОБИЛИ")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            font-size: 20px;
            color: {COLORS['accent_purple']};
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        
        # Приветствие
        welcome = QLabel(f"ДОБРО ПОЖАЛОВАТЬ, {self.user['username'].upper()}!")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet(f"""
            font-size: 18px;
            color: {COLORS['text_secondary']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        # Главное меню
        menu_container = QWidget()
        menu_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_blue']};
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
            color: {COLORS['accent_blue']};
            margin-bottom: 30px;
            font-family: 'Segoe UI';
        """)
        
        # Кнопки меню
        btn_assortment = self.create_menu_button("📦 АССОРТИМЕНТ АВТОМОБИЛЕЙ")
        btn_orders = self.create_menu_button("📋 МОИ ЗАКАЗЫ")
        btn_reviews = self.create_menu_button("⭐ ОСТАВИТЬ ОТЗЫВ")
        btn_my_reviews = self.create_menu_button("📝 МОИ ОТЗЫВЫ")
        btn_exit = self.create_menu_button("🚪 ВЫХОД")
        
        # Подключаем кнопки
        btn_assortment.clicked.connect(self.show_assortment)
        btn_orders.clicked.connect(self.show_orders)
        btn_reviews.clicked.connect(self.show_reviews)
        btn_my_reviews.clicked.connect(self.show_my_reviews)
        btn_exit.clicked.connect(self.logout_callback)
        
        # Добавляем кнопки в меню
        menu_layout.addWidget(btn_assortment)
        menu_layout.addWidget(btn_orders)
        menu_layout.addWidget(btn_reviews)
        menu_layout.addWidget(btn_my_reviews)
        menu_layout.addWidget(btn_exit)
        
        # Инструкция
        instruction_frame = QFrame()
        instruction_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['secondary_bg']};
                border: 2px solid {COLORS['accent_blue']};
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
            color: {COLORS['accent_blue']};
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
        
        # Собираем интерфейс
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
        button.setMinimumSize(400, 60)
        button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1d4ed8, stop:1 #6d28d9);
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
            color: {COLORS['accent_blue']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)

        # Создаем область прокрутки
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
                background-color: {COLORS['accent_blue']};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {COLORS['accent_purple']};
            }}
        """)

        # Контейнер для карточек
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
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
        """)
        btn_back.clicked.connect(self.back_callback)

        layout.addWidget(title)
        layout.addWidget(scroll_area)
        layout.addWidget(btn_back)

        self.load_cars()

    def load_cars(self):
        try:
            # Очищаем старые карточки
            for i in reversed(range(self.cards_layout.count())): 
                widget = self.cards_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            
            cars = get_all_cars()
            
            if not cars:
                no_cars_label = QLabel("В НАСТОЯЩЕЕ ВРЕМЯ НЕТ ДОСТУПНЫХ АВТОМОБИЛЕЙ")
                no_cars_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 16px; font-family: 'Segoe UI';")
                no_cars_label.setAlignment(Qt.AlignCenter)
                self.cards_layout.addWidget(no_cars_label, 0, 0, 1, 3)
                return
            
            # Добавляем карточки автомобилей
            for i, car in enumerate(cars):
                row = i // 3
                col = i % 3
                car_card = CarCard(car, self.user, self.load_cars)
                self.cards_layout.addWidget(car_card, row, col)
                
        except Exception as e:
            QMessageBox.critical(self, "❌ ОШИБКА", f"Не удалось загрузить автомобили: {str(e)}")

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
            color: {COLORS['accent_blue']}; 
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
                border: 2px solid {COLORS['accent_blue']};
                border-radius: 8px;
                font-family: 'Segoe UI';
            }}
            QTableWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {COLORS['border']};
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_blue']};
                color: {COLORS['text_primary']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
        """)
        btn_back.clicked.connect(self.back_callback)
        
        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addWidget(btn_back)
        
        self.load_orders()

    def load_orders(self):
        try:
            client_id = get_or_create_client_for_user(self.user['id'], self.user['username'])
            orders = get_client_orders(client_id)
            
            self.table.setRowCount(len(orders))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["Автомобиль", "Дата покупки", "Цена", "Продавец", "Статус"])
            
            for row, order in enumerate(orders):
                car_info = f"{order['brand']} {order['model']}"
                self.table.setItem(row, 0, QTableWidgetItem(car_info))
                self.table.setItem(row, 1, QTableWidgetItem(str(order['sale_date'])))
                self.table.setItem(row, 2, QTableWidgetItem(f"{order['final_price']:,.0f} ₽"))
                self.table.setItem(row, 3, QTableWidgetItem(order['employee_name']))
                self.table.setItem(row, 4, QTableWidgetItem("✅ Выполнен"))
            
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
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
            color: {COLORS['accent_blue']}; 
            font-weight: bold; 
            margin-bottom: 20px;
            font-family: 'Segoe UI';
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # Форма отзыва
        form_container = QWidget()
        form_container.setStyleSheet(f"""
            background-color: {COLORS['secondary_bg']};
            border: 2px solid {COLORS['accent_blue']};
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
        
        # Стилизация полей
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
                border-color: {COLORS['accent_blue']};
                background-color: {COLORS['secondary_bg']};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {COLORS['accent_blue']};
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
        
        # Стиль для меток формы
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setStyleSheet(f"color: {COLORS['accent_blue']}; font-size: 14px; font-family: 'Segoe UI'; font-weight: bold;")
        
        btn_submit = QPushButton("📝 ОТПРАВИТЬ ОТЗЫВ")
        btn_submit.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
        """)
        btn_submit.clicked.connect(self.submit_review)
        
        btn_back = QPushButton("◀ НАЗАД В МЕНЮ")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['accent_blue']};
                border: 2px solid {COLORS['accent_blue']};
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_blue']};
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
            color: {COLORS['accent_blue']}; 
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
                border: 2px solid {COLORS['accent_blue']};
                border-radius: 8px;
                font-family: 'Segoe UI';
            }}
            QTableWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {COLORS['border']};
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_blue']};
                color: {COLORS['text_primary']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
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
                border: 2px solid {COLORS['accent_blue']};
                border-radius: 12px;
                font-family: 'Segoe UI';
            }}
            QMessageBox QLabel {{
                color: {COLORS['text_primary']};
            }}
            QMessageBox QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_purple']});
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
                    stop:0 #2563eb, stop:1 #7c3aed);
            }}
        """)
        
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        
        # Страница входа
        self.login_page = LoginPage(
            on_login_success=self.handle_login_success,
            go_register=self.show_register
        )
        
        # Страница регистрации
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
        self.main_menu = MainMenuPage(user, logout_callback=self.show_login)
        self.stacked.addWidget(self.main_menu)
        self.stacked.setCurrentWidget(self.main_menu)
    
    def show_car_catalog(self):
        self.car_catalog = CarCatalogPage(self.user, back_callback=self.show_main_menu)
        self.stacked.addWidget(self.car_catalog)
        self.stacked.setCurrentWidget(self.car_catalog)
    
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
    # Инициализируем базу данных
    init_db()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())