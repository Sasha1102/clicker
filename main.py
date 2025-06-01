import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class Clicker(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.click_count = 0
        self.click_power = 1
        self.upgrade_cost = 10
        self.init_ui()
        self.show()
        with open("style.css", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.planet = QPushButton(self)
        self.planet.setIcon(QIcon('Venus.png'))
        self.planet.setIconSize(QSize(150, 150))
        self.planet.clicked.connect(self.planet_click)
        self.planet.setObjectName("planetButton")

        self.score_label = QLabel(f"Кліків: {self.click_count}", self)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setObjectName("scoreLabel")

        self.power_label = QLabel(f"Множник: {self.click_power}", self)
        self.power_label.setAlignment(Qt.AlignCenter)
        self.power_label.setObjectName("powerLabel")

        self.upgrade_button = QPushButton(f"Покращити клік (+1) - {self.upgrade_cost} кліків", self)
        self.upgrade_button.clicked.connect(self.upgrade_click_power)
        self.upgrade_button.setObjectName("upgradeButton")

        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.power_label)
        self.layout.addWidget(self.planet)
        self.layout.addWidget(self.upgrade_button)
        self.setLayout(self.layout)

    def planet_click(self) -> None:
        self.click_count += self.click_power
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


app = QApplication(sys.argv)
window = Clicker()
sys.exit(app.exec_())
