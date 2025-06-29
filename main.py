import sys
import json
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Реєстрація")
        self.setFixedSize(300, 200)

        self.layout = QVBoxLayout()

        self.username_label = QLabel("Логін:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Зареєструватися")
        self.register_button.clicked.connect(self.register)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            all_users = {}
            try:
                with open("users.json", "r", encoding='utf-8') as file:
                    all_users = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                all_users = {}

            if username in all_users:
                QMessageBox.warning(self, "Помилка", "Користувач з таким логіном вже існує!")
                return

            user_data = {
                "username": username,
                "password": password,
                "progress": {
                    "click_count": 0,
                    "click_power": 1,
                    "upgrade_cost": 10,
                    "autoclick_rate": 0,
                    "autoclick_cost": 50
                }
            }
            all_users[username] = user_data

            with open("users.json", "w", encoding='utf-8') as file:
                json.dump(all_users, file, indent=4)

            QMessageBox.information(self, "Успіх", "Реєстрація пройшла успішно!")
            self.accept()
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, заповніть всі поля!")


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вхід")
        self.setFixedSize(300, 200)

        self.layout = QVBoxLayout()

        self.username_label = QLabel("Логін:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Увійти")
        self.login_button.clicked.connect(self.login)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            with open("users.json", "r", encoding='utf-8') as file:
                all_users = json.load(file)

            if username not in all_users:
                QMessageBox.warning(self, "Помилка", "Користувач не знайдений!")
                return

            user_data = all_users[username]
            if password == user_data["password"]:
                QMessageBox.information(self, "Успіх", f"Ласкаво просимо, {username}!")
                self.accept()
            else:
                QMessageBox.warning(self, "Помилка", "Невірний логін або пароль!")
        except FileNotFoundError:
            QMessageBox.warning(self, "Помилка", "Немає зареєстрованих користувачів. Спочатку зареєструйтесь.")
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Помилка", "Помилка читання даних користувача. Файл users.json пошкоджений.")


class Clicker(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.current_username = None
        self.click_count = 0
        self.click_power = 1
        self.upgrade_cost = 10
        self.autoclick_rate = 0
        self.autoclick_cost = 50

        self.init_ui()
        self.show()

        try:
            with open("style.css", "r", encoding='utf-8') as stylesheet:
                self.setStyleSheet(stylesheet.read())
        except FileNotFoundError:
            print("Помилка: Файл style.css не знайдено.")
        except Exception as e:
            print(f"Помилка завантаження стилів: {e}")

        self.autoclick_timer = QTimer(self)
        self.autoclick_timer.setInterval(1000)
        self.autoclick_timer.timeout.connect(self.autoclick)
        self.autoclick_timer.start()

        self._set_game_state_enabled(False)
        self.update_labels()

    def _load_current_user_progress(self):
        if not self.current_username:
            print("Немає активного користувача для завантаження прогресу.")
            return

        try:
            with open("users.json", "r", encoding='utf-8') as file:
                all_users = json.load(file)
                if self.current_username in all_users:
                    user_data = all_users[self.current_username]
                    self.click_count = user_data["progress"]["click_count"]
                    self.click_power = user_data["progress"]["click_power"]
                    self.upgrade_cost = user_data["progress"]["upgrade_cost"]
                    self.autoclick_rate = user_data["progress"]["autoclick_rate"]
                    self.autoclick_cost = user_data["progress"]["autoclick_cost"]
                    print(f"Прогрес користувача {self.current_username} завантажено.")
                else:
                    print(f"Дані прогресу для {self.current_username} не знайдено в users.json.")
        except FileNotFoundError:
            print("Файл users.json не знайдено. Прогрес не завантажено.")
        except json.JSONDecodeError:
            print("Помилка читання users.json. Файл пошкоджений або порожній.")
        except KeyError as e:
            print(f"Помилка: Відсутній ключ у даних користувача в users.json - {e}")

    def save_user_data(self):
        if not self.current_username:
            print("Немає активного користувача для збереження даних.")
            return

        all_users = {}
        try:
            with open("users.json", "r", encoding='utf-8') as file:
                all_users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_users = {}

        if self.current_username not in all_users:
            print(f"Помилка: Не вдалося знайти користувача {self.current_username} для збереження.")
            return

        all_users[self.current_username]["progress"] = {
            "click_count": self.click_count,
            "click_power": self.click_power,
            "upgrade_cost": self.upgrade_cost,
            "autoclick_rate": self.autoclick_rate,
            "autoclick_cost": self.autoclick_cost
        }
        try:
            with open("users.json", "w", encoding='utf-8') as file:
                json.dump(all_users, file, indent=4)
        except Exception as e:
            print(f"Помилка збереження даних користувача: {e}")

    def init_ui(self):
        self.setWindowTitle("Клікер гра")
        self.setFixedSize(500, 600)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.register_button = QPushButton("Реєстрація", self)
        self.register_button.clicked.connect(self.show_register_dialog)
        self.register_button.setObjectName("authButton")

        self.login_button = QPushButton("Вхід", self)
        self.login_button.clicked.connect(self.show_login_dialog)
        self.login_button.setObjectName("authButton")

        auth_buttons_layout = QHBoxLayout()
        auth_buttons_layout.addWidget(self.register_button)
        auth_buttons_layout.addWidget(self.login_button)
        self.layout.addLayout(auth_buttons_layout)

        self.score_label = QLabel(f"Кліків: {self.click_count}", self)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setObjectName("scoreLabel")

        self.power_label = QLabel(f"Множник: {self.click_power}", self)
        self.power_label.setAlignment(Qt.AlignCenter)
        self.power_label.setObjectName("powerLabel")

        self.autoclick_rate_label = QLabel(f"Кліків/сек: {self.autoclick_rate}", self)
        self.autoclick_rate_label.setAlignment(Qt.AlignCenter)
        self.autoclick_rate_label.setObjectName("autoclickRateLabel")

        self.planet = QPushButton(self)
        self.planet.setIcon(QIcon('Venus.png'))
        self.planet.setIconSize(QSize(250, 250))
        self.planet.clicked.connect(self.planet_click)
        self.planet.setObjectName("planetButton")

        self.upgrade_button = QPushButton(f"Покращити клік (+1) - {self.upgrade_cost} кліків", self)
        self.upgrade_button.clicked.connect(self.upgrade_click_power)
        self.upgrade_button.setObjectName("upgradeButton")

        self.autoclick_button = QPushButton(f"Автоклікер (+1/сек) - {self.autoclick_cost} кліків", self)
        self.autoclick_button.clicked.connect(self.upgrade_autoclick)
        self.autoclick_button.setObjectName("autoclickButton")

        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.power_label)
        self.layout.addWidget(self.autoclick_rate_label)
        self.layout.addWidget(self.planet)
        self.layout.addWidget(self.upgrade_button)
        self.layout.addWidget(self.autoclick_button)

        self.setLayout(self.layout)

    def _set_game_state_enabled(self, enabled: bool):
        self.planet.setEnabled(enabled)
        self.upgrade_button.setEnabled(enabled)
        self.autoclick_button.setEnabled(enabled)
        self.update_labels()

    def update_labels(self):
        self.score_label.setText(f"Кліків: {self.click_count}")
        self.power_label.setText(f"Множник: {self.click_power}")
        self.autoclick_rate_label.setText(f"Кліків/сек: {self.autoclick_rate}")
        self.upgrade_button.setText(f"Покращити клік (+1) - {self.upgrade_cost} кліків")
        self.autoclick_button.setText(f"Автоклікер (+1/сек) - {self.autoclick_cost} кліків")

    def planet_click(self) -> None:
        self.click_count += self.click_power
        self.update_labels()
        self.save_user_data()

    def autoclick(self) -> None:
        if self.current_username:
            self.click_count += self.autoclick_rate
            self.update_labels()
            self.save_user_data()

    def upgrade_click_power(self) -> None:
        if self.click_count >= self.upgrade_cost:
            self.click_count -= self.upgrade_cost
            self.click_power += 1
            self.upgrade_cost = int(self.upgrade_cost * 2)
            self.update_labels()
            self.save_user_data()
        else:
            QMessageBox.information(self, "Недостатньо кліків", "У вас недостатньо кліків для апгрейду!")

    def upgrade_autoclick(self) -> None:
        if self.click_count >= self.autoclick_cost:
            self.click_count -= self.autoclick_cost
            self.autoclick_rate += 1
            self.autoclick_cost = int(self.autoclick_cost * 1.5)
            self.update_labels()
            self.save_user_data()
        else:
            QMessageBox.information(self, "Недостатньо кліків", "У вас недостатньо кліків для автоклікеру!")

    def show_register_dialog(self):
        register_dialog = RegisterDialog()
        if register_dialog.exec_() == QDialog.Accepted:
            self.current_username = register_dialog.username_input.text()
            self._load_current_user_progress()
            self._set_game_state_enabled(True)
            self.update_labels()
            QMessageBox.information(self, "Ласкаво просимо!", f"Вітаємо, {self.current_username}!")
        else:
            QMessageBox.information(self, "Відміна", "Реєстрацію скасовано.")

    def show_login_dialog(self):
        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            self.current_username = login_dialog.username_input.text()
            self._load_current_user_progress()
            self._set_game_state_enabled(True)
            self.update_labels()
        else:
            QMessageBox.information(self, "Відміна", "Вхід скасовано.")


app = QApplication(sys.argv)
window = Clicker()
sys.exit(app.exec_())
