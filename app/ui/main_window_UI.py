from PyQt6.QtWidgets import QDialog, QMessageBox, QApplication
from PyQt6.QtCore import QSettings
from PyQt6.uic import loadUi
from pathlib import Path
from app.controller.logic import main_window_logic
from app.controller.i18n import set_lang
from app.controller.navigator import Navigator
import sys

class MainWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()

        if getattr(sys, 'frozen', False):
            self.ui_path = Path(sys._MEIPASS) / "app" / "ui" / "main_window.ui"
        else:
            self.ui_path = Path(__file__).parent / "main_window.ui"

        self.settings = QSettings("ImprestManagement", "App")
        saved_lang = self.settings.value("language", "en")
        is_fa = (saved_lang == "fa")
        set_lang(saved_lang, QApplication.instance())

        self.UI = loadUi(str(self.ui_path), self)
        self.setWindowTitle("Imprest_Management Version 1.0")
        self.success = False
        self.role = ""
        self.username = ""

        self.logic = main_window_logic()
        self.nav = Navigator()

        self.UI.lang_toggle.setChecked(is_fa)
        self.UI.lang_toggle.setText("FA" if is_fa else "EN")

        self._set_footer_text()
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.UI.btnLogin.clicked.connect(self.on_login_clicked)
        self.UI.lang_toggle.toggled.connect(self.on_language_toggled)
        self.UI.lblFooterLeft.linkActivated.connect(self.open_about_page)

    def _set_footer_text(self) -> None:
        self.UI.lblFooterLeft.setText("""
        <div align="left">
        <a href="about" style="
            color: #939495;
            text-decoration: none;
            font-family: 'Segoe UI';
            font-size: 10px;
        ">
        Nozhan Ghayati Design &amp; Developer <br>
        Kian Farooghi Project Management &amp; QA <br><br>
        © 2026
        </a>
        </div>
        """)

    def on_login_clicked(self) -> None:
        username = self.UI.leUsername.text().strip()
        password = self.UI.lePassword.text()

        result = main_window_logic.login(username, password)
        if result.ok:
            self.success = True
            self.accept()
            self.nav.main_window_navigator(self)
        else:
            QMessageBox.critical(None, "Warning", result.error_message)

    def open_about_page(self, link):
        try:
            self.nav.main_window_navigator_about_us(self)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"CRASH: {e}")

    def on_language_toggled(self, checked: bool):
        lang = "fa" if checked else "en"
        self.settings.setValue("language", lang)

        self.close()
        self.new_window = MainWindow()
        self.new_window.show()