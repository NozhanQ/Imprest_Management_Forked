from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from pathlib import Path
from app.controller.navigator import Navigator
from app.controller.logic import main_window_logic


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        ui_path = Path(__file__).parent / "main_window.ui"
        loadUi(ui_path, self)

        self.dashboard = None
        self.setWindowTitle("My App")

        self.logic = main_window_logic()
        self.nav=Navigator()
        self.btnLogin.clicked.connect(self.on_login_clicked)

    def on_login_clicked(self) -> None:
        username = self.leUsername.text().strip()
        password = self.lePassword.text()

        result = self.logic.login(username, password)
        if not result.ok:
            QMessageBox.warning(self, "Login", result.error)
            return
        self.dashboard = self.nav.open_dashboard(self)
