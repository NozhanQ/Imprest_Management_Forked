from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi
from pathlib import Path
from app.ui.Receipt_Entry_Page import Receipt_Entry_Page
from app.ui.Calling_Page import Calling_Page

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = Path(__file__).parent / "Dashboard.ui"
        loadUi(ui_path, self)
        self.setWindowTitle("Dashboard")
        self.btndashboard_input.clicked.connect(self.Input_Clicked)
        self.btndashboard_save.clicked.connect(self.Save_Clicked)

    def Input_Clicked(self):
        self.expense_entry = Receipt_Entry_Page.Receipt_Entry_Page()
        self.expense_entry.show()
        self.close()

    def Save_Clicked(self):
        self.calling_page = Calling_Page()
        self.calling_page.show()
        self.close()