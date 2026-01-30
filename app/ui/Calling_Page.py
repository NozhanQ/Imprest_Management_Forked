from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QDate
from PyQt6.uic import loadUi
from pathlib import Path


class Calling_Page(QWidget):
    def __init__(self):
        super().__init__()

        ui_path = Path(__file__).parent / "Calling_Page.ui"
        loadUi(ui_path, self)
        self.stackedWidget.setCurrentIndex(3)
        self.setWindowTitle("Calling_Page")

        # Radio buttons
        self.radioButton1.setChecked(True)
        self.radioButton1.toggled.connect(lambda: self.change_page(3))
        self.radioButton2.toggled.connect(lambda: self.change_page(2))
        self.radioButton3.toggled.connect(lambda: self.change_page(1))
        self.radioButton4.toggled.connect(lambda: self.change_page(0))

        # DateEdit 2 (Start)
        self.dateEdit_2.setMinimumDate(QDate(2000, 1, 1))
        self.dateEdit_2.setSpecialValueText("Start")
        self.dateEdit_2.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit_2.setDate(self.dateEdit_2.minimumDate())

        # DateEdit 3 (End)
        self.dateEdit_3.setMinimumDate(QDate(2000, 1, 1))
        self.dateEdit_3.setSpecialValueText("End")
        self.dateEdit_3.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit_3.setDate(self.dateEdit_3.minimumDate())

    def change_page(self, index):
        if self.sender().isChecked():
            self.stackedWidget.setCurrentIndex(index)
