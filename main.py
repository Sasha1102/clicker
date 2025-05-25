import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class Clicker(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.planet = QPushButton(self)
        self.planet.setIcon(QIcon('Venus.png'))
        self.planet.setIconSize(QSize(75, 75))
        self.planet.clicked.connect(self.planet_click)
        self.layout.addWidget(self.planet)
        self.setLayout(self.layout)


    def planet_click(self) -> None:


app = QApplication(sys.argv)
window = Clicker()
sys.exit(app.exec_())
