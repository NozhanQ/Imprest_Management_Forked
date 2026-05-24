import sys
import jdatetime

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal


PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد",
    "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر",
    "دی", "بهمن", "اسفند"
]

PERSIAN_WEEKDAYS = [
    "ش", "ی", "د", "س", "چ", "پ", "ج"
]


class JalaliCalendarPopup(QDialog):
    date_selected = pyqtSignal(jdatetime.date)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("انتخاب تاریخ")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        today = jdatetime.date.today()
        self.current_year = today.year
        self.current_month = today.month

        self.main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        self.prev_btn = QPushButton("ماه قبل")
        self.next_btn = QPushButton("ماه بعد")
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_btn.clicked.connect(self.previous_month)
        self.next_btn.clicked.connect(self.next_month)

        header_layout.addWidget(self.prev_btn)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.next_btn)

        self.calendar_grid = QGridLayout()

        self.main_layout.addLayout(header_layout)
        self.main_layout.addLayout(self.calendar_grid)

        self.draw_calendar()

    def clear_grid(self):
        while self.calendar_grid.count():
            item = self.calendar_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def month_length(self, year, month):
        if month <= 6:
            return 31
        elif month <= 11:
            return 30
        else:
            return 30 if jdatetime.date(year, 1, 1).isleap() else 29

    def draw_calendar(self):
        self.clear_grid()

        self.title_label.setText(
            f"{PERSIAN_MONTHS[self.current_month - 1]} {self.current_year}"
        )

        for col, name in enumerate(PERSIAN_WEEKDAYS):
            label = QLabel(name)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.calendar_grid.addWidget(label, 0, col)

        first_day = jdatetime.date(self.current_year, self.current_month, 1)

        # jdatetime weekday:
        # Saturday = 0, Sunday = 1, ..., Friday = 6
        start_col = first_day.weekday()

        days_count = self.month_length(self.current_year, self.current_month)

        row = 1
        col = start_col

        today = jdatetime.date.today()

        for day in range(1, days_count + 1):
            btn = QPushButton(str(day))

            btn.setFixedSize(55,55)

            btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    font-weight: bold;
                    border: 2px solid orange;
                    border-radius: 15px;
                }

                QPushButton:hover {
                    background-color: #333;
                }
            """)

            selected_date = jdatetime.date(
                self.current_year,
                self.current_month,
                day
            )

            if selected_date == today:
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 20px;
                        font-weight: bold;
                        border: 3px solid #666;
                        border-radius: 15px;
                        background-color: #222;
                    }
                """)

            btn.clicked.connect(
                lambda checked=False, d=selected_date: self.select_date(d)
            )

            self.calendar_grid.addWidget(btn, row, col)

            col += 1
            if col > 6:
                col = 0
                row += 1

    def select_date(self, date):
        self.date_selected.emit(date)
        self.accept()

    def previous_month(self):
        self.current_month -= 1

        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1

        self.draw_calendar()

    def next_month(self):
        self.current_month += 1

        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1

        self.draw_calendar()


class JalaliDateEdit(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_jalali_date = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("مثلاً 1403/02/15")
        self.line_edit.setReadOnly(True)

        self.button = QPushButton("📅")
        self.button.clicked.connect(self.open_calendar)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

    def open_calendar(self):
        popup = JalaliCalendarPopup(self)
        popup.date_selected.connect(self.set_date)
        popup.exec()

    def set_date(self, jalali_date):
        self.selected_jalali_date = jalali_date

        self.line_edit.setText(
            f"{jalali_date.year:04d}/{jalali_date.month:02d}/{jalali_date.day:02d}"
        )

    def get_jalali_date(self):
        return self.selected_jalali_date

    def get_gregorian_date(self):
        if self.selected_jalali_date is None:
            return None

        return self.selected_jalali_date.togregorian()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jalali Date Picker Example")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        layout = QVBoxLayout(self)

        self.date_picker = JalaliDateEdit()
        self.result_label = QLabel("")

        self.submit_btn = QPushButton("نمایش تاریخ")
        self.submit_btn.clicked.connect(self.show_selected_date)

        layout.addWidget(self.date_picker)
        layout.addWidget(self.submit_btn)
        layout.addWidget(self.result_label)

    def show_selected_date(self):
        jalali = self.date_picker.get_jalali_date()
        gregorian = self.date_picker.get_gregorian_date()

        if jalali is None:
            self.result_label.setText("هیچ تاریخی انتخاب نشده است.")
            return

        self.result_label.setText(
            f"تاریخ شمسی: {jalali.year:04d}/{jalali.month:02d}/{jalali.day:02d}\n"
            f"تاریخ میلادی برای ذخیره‌سازی: {gregorian}"
        )