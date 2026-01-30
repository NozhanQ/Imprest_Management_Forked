from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
from pathlib import Path
from app.ui.Dashboard import Dashboard


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()


        ui_path = Path(__file__).parent / "main_window.ui"
        loadUi(ui_path, self)


        self.dashboard = None
        self.setWindowTitle("My App")
        self.btnLogin.clicked.connect(self.on_test_clicked)

    def check_if_data_is_entered(self, username, password):
        if not username:
            print("Username is empty") #TODO(NG): Replace this with message box to let user know.
            return False
        elif not password:
            print("password is empty") #TODO(NG): Replace this with message box to let user know.
            return False
        return True

    def on_test_clicked(self):
        username = self.leUsername.text()
        password = self.lePassword.text()

        if not self.check_if_data_is_entered(username, password):
            return

        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()
