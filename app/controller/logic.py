from __future__ import annotations
from pathlib import Path
from typing import Optional, Tuple
from PyQt6.QtWidgets import QFileDialog, QWidget
from dataclasses import dataclass


class receipt_entry_logic:
    def browse_image(
            self,
            parent: QWidget,
            title: str = "Select an image",
            start_dir: Optional[str | Path] = None,
    ) -> Optional[str]:
        """
        Opens a file dialog and returns the selected image path as a string.
        Returns None if the user cancels.
        """
        start_dir_str = str(start_dir) if start_dir else ""

        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            title,
            start_dir_str,
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp);;All Files (*)",
        )

        return file_path or None


@dataclass
class LoginResult:
    ok: bool
    error: str = ""

class main_window_logic:
    def validate_inputs(self, username: str, password: str) -> LoginResult:
        if not username:
            return LoginResult(False, "Username is empty")
        if not password:
            return LoginResult(False, "Password is empty")
        return LoginResult(True)

    def login(self, username: str, password: str) -> LoginResult:
        # later: check DB / API
        return self.validate_inputs(username, password)

