from PyQt6.QtWidgets import QWidget, QFileDialog,QMessageBox
from PyQt6.uic import loadUi
from pathlib import Path
from app.data.data_base import insert_record


class Expense_Receipt_Entry(QWidget):
    def __init__(self):
        super().__init__()

        ui_path = Path(__file__).parent / "Expense_Receipt_Entry.ui"
        loadUi(ui_path, self)
        self.setWindowTitle("Expense_Receipt_Entry")
        self.selected_image_path = None
        self.btnBrowse.clicked.connect(self.browse_image)
        self.btnClear.clicked.connect(self.clear_image)
        self.btnSave.clicked.connect(self.save_record)


    def browse_image(self): #TODO(KF): This function should be written in another layer. this is not pure UI.
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            self.selected_image_path = file_path
            self.lblSelectPicture.setText(file_path)


    def clear_image(self):
        self.selected_image_path = None
        self.lblSelectPicture.setText("No file selected")

    def open_dashboard(self):
        from app.ui.Dashboard import Dashboard
        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()

    def save_record(self): #TODO(KF): This function should be written in another layer. this is not pure UI.
        title = self.leInvoiceNumber.text()
        description = self.textEdit.toPlainText()
        amount = self.leExpense.text()
        record_date = self.dateEdit.date().toString("yyyy-MM-dd")
        image_path = self.selected_image_path
        expense_center=self.cbExpenseCenter.currentText()
        expense_type=self.cbExpenseCenter.currentText()
        company_name=self.cbCompany.currentText()
        source_pc = "PC-1"  # later we automate this
        self.open_dashboard()
        if not title:
            return  # add QMessageBox later

        insert_record( #TODO(KF): This function should be written in another layer. this is not pure UI.
            title=title,
            description=description,
            amount=amount,
            record_date=record_date,
            image_path=image_path,
            expense_center=expense_center,
            expense_type=expense_type,
            company_name=company_name,
            source_pc=source_pc
        )
