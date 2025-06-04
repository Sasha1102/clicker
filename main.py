import sys

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class Clicker(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.click_count = 0
        self.click_power = 1
        self.upgrade_cost = 10
        self.autoclick_rate = 0
        self.autoclick_cost = 50
        self.init_ui()
        self.show()
        with open("style.css", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.autoclick_timer = QTimer(self)
        self.autoclick_timer.setInterval(1000)
        self.autoclick_timer.timeout.connect(self.autoclick)
        self.autoclick_timer.start()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.planet = QPushButton(self)
        self.planet.setIcon(QIcon('Venus.png'))
        self.planet.setIconSize(QSize(250, 250))
        self.planet.clicked.connect(self.planet_click)
        self.planet.setObjectName("planetButton")

        self.score_label = QLabel(f"Кліків: {self.click_count}", self)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setObjectName("scoreLabel")

        self.power_label = QLabel(f"Множник: {self.click_power}", self)
        self.power_label.setAlignment(Qt.AlignCenter)
        self.power_label.setObjectName("powerLabel")

        self.autoclick_rate_label = QLabel(f"Кліків/сек: {self.autoclick_rate}", self)
        self.autoclick_rate_label.setAlignment(Qt.AlignCenter)
        self.autoclick_rate_label.setObjectName("autoclickRateLabel")

        self.upgrade_button = QPushButton(f"Покращити клік (+1) - {self.upgrade_cost} кліків", self)
        self.upgrade_button.clicked.connect(self.upgrade_click_power)
        self.upgrade_button.setObjectName("upgradeButton")

        self.autoclick_button = QPushButton(f"Автоклікер (+1/сек) - {self.autoclick_cost} кліків", self)
        self.autoclick_button.clicked.connect(self.upgrade_autoclick)
        self.autoclick_button.setObjectName("autoclickButton")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.upgrade_button)
        self.buttons_layout.addWidget(self.autoclick_button)
        self.buttons_layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.power_label)
        self.layout.addWidget(self.autoclick_rate_label)
        self.layout.addWidget(self.planet)
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def planet_click(self) -> None:
        self.click_count += self.click_power
        self.score_label.setText(f"Кліків: {self.click_count}")

    def autoclick(self) -> None:
        self.click_count += self.autoclick_rate
        self.score_label.setText(f"Кліків: {self.click_count}")

    def upgrade_click_power(self) -> None:
        if self.click_count >= self.upgrade_cost:
            self.click_count -= self.upgrade_cost
            self.click_power += 1
            self.upgrade_cost = int(self.upgrade_cost * 2)
            self.score_label.setText(f"Кліків: {self.click_count}")
            self.power_label.setText(f"Множник: {self.click_power}")
            self.upgrade_button.setText(f"Покращити клік (+1) - {self.upgrade_cost} кліків")
        else:
            QMessageBox.information(self, "Недостатньо кліків", "У вас недостатньо кліків для апгрейду!")

    def upgrade_autoclick(self) -> None:
        if self.click_count >= self.autoclick_cost:
            self.click_count -= self.autoclick_cost
            self.autoclick_rate += 1
            self.autoclick_cost = int(self.autoclick_cost * 1.5)
            self.score_label.setText(f"Кліків: {self.click_count}")
            self.autoclick_rate_label.setText(f"Автокліків/сек: {self.autoclick_rate}")
            self.autoclick_button.setText(f"Автоклікер (+1/сек) - {self.autoclick_cost} кліків")
        else:
            QMessageBox.information(self, "Недостатньо кліків", "У вас недостатньо кліків для автоклікеру!")


app = QApplication(sys.argv)
window = Clicker()
sys.exit(app.exec_())
