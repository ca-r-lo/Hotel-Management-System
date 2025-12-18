from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QComboBox, QFrame, QMessageBox, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit,
    QAbstractItemView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from models import purchase as purchase_model


class ReportDamagesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Report Damages")
        self.setMinimumSize(900, 700)
        
        # Use a very clean, high-contrast theme like the mockup
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #000000;
                font-family: 'Inter', sans-serif;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                border: 2px solid #000000;
                border-radius: 0px;
                padding: 6px;
                background-color: #ffffff;
                color: #000000;
            }
            QPushButton {
                border: 2px solid #000000;
                border-radius: 0px;
                padding: 8px 24px;
                font-weight: bold;
                background-color: #ffffff;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
            QTableWidget {
                border: 2px solid #000000;
                gridline-color: #000000;
                background-color: #ffffff;
                color: #000000;
            }
            QTableWidget::item {
                color: #000000;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #ffffff;
                color: #000000;
                font-weight: bold;
                border: 1px solid #000000;
                padding: 4px;
            }
        """)

        self.init_ui()
        
        # Load data safely
        try:
            self.load_orders()
            self.load_damages()
        except Exception as e:
            print(f"Error loading data: {e}")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 1. HEADER
        title = QLabel("REPORT DAMAGES")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # 2. TABLE SECTION
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Report ID", "Report Date", "Category", "Status"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setFixedHeight(200)
        main_layout.addWidget(self.table)

        # 3. SUB-HEADER (Details row from mockup)
        details_row = QHBoxLayout()
        for text in ["Report ID", "Report Date", "Category", "Status"]:
            lbl = QLabel(text)
            lbl.setFont(QFont("Inter", 10, QFont.Weight.Bold))
            details_row.addWidget(lbl)
        main_layout.addLayout(details_row)

        details_vals = QHBoxLayout()
        for text in ["Order ID", "Order Date", "Category", "Status"]:
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #666;")
            details_vals.addWidget(lbl)
        main_layout.addLayout(details_vals)

        # 4. NEW REPORT LINK
        self.new_report_btn = QPushButton("+ New Report...")
        self.new_report_btn.setStyleSheet("border: none; text-align: left; color: #000; text-decoration: underline;")
        self.new_report_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        main_layout.addWidget(self.new_report_btn)

        # 5. ADD REPORT FORM (The centered box)
        form_container = QFrame()
        form_container.setFrameShape(QFrame.Shape.Box)
        form_container.setLineWidth(2)
        form_container.setStyleSheet("background-color: #ffffff; border: 2px solid #000000;")
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(40, 20, 40, 20)
        form_layout.setSpacing(15)

        form_title = QLabel("ADD REPORT")
        form_title.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        form_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(form_title)

        # Grid-like fields
        grid = QVBoxLayout()
        
        # Row 1
        r1 = QHBoxLayout()
        l1 = QVBoxLayout(); l1.addWidget(QLabel("REPORT ID:")); self.report_id = QLineEdit(); self.report_id.setReadOnly(True); l1.addWidget(self.report_id); r1.addLayout(l1)
        l2 = QVBoxLayout(); l2.addWidget(QLabel("REPORT DATE:")); self.report_date = QDateEdit(); self.report_date.setDate(QDate.currentDate()); l2.addWidget(self.report_date); r1.addLayout(l2)
        grid.addLayout(r1)

        # Row 2
        r2 = QHBoxLayout()
        l3 = QVBoxLayout(); l3.addWidget(QLabel("ORDER ID:")); self.order_combo = QComboBox(); l3.addWidget(self.order_combo); r2.addLayout(l3)
        l4 = QVBoxLayout(); l4.addWidget(QLabel("CATEGORY:")); self.category_combo = QComboBox(); self.category_combo.addItems(["Delivery Issue", "Storage Damage", "Expired", "Other"]); l4.addWidget(self.category_combo); r2.addLayout(l4)
        grid.addLayout(r2)

        # Row 3 (Item - needed for logic)
        r3 = QHBoxLayout()
        l5 = QVBoxLayout(); l5.addWidget(QLabel("ITEM:")); self.item_combo = QComboBox(); l5.addWidget(self.item_combo); r3.addLayout(l5)
        l6 = QVBoxLayout(); l6.addWidget(QLabel("QTY:")); self.qty_input = QLineEdit(); l6.addWidget(self.qty_input); r3.addLayout(l6)
        grid.addLayout(r3)

        # Row 4 (Description)
        l7 = QVBoxLayout(); l7.addWidget(QLabel("DESCRIPTION:")); self.desc_input = QTextEdit(); self.desc_input.setMaximumHeight(80); l7.addWidget(self.desc_input); grid.addLayout(l7)
        
        form_layout.addLayout(grid)

        # Form Buttons
        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("ADD")
        self.cancel_btn = QPushButton("CANCEL")
        btn_row.addStretch()
        btn_row.addWidget(self.add_btn)
        btn_row.addSpacing(20)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addStretch()
        form_layout.addLayout(btn_row)

        main_layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        # Connections
        self.add_btn.clicked.connect(self.handle_add)
        self.cancel_btn.clicked.connect(self.reject)
        self.order_combo.currentIndexChanged.connect(self.on_order_changed)

    def load_orders(self):
        try:
            orders = purchase_model.PurchaseModel.list_purchases()
            self.order_combo.clear()
            self.order_combo.addItem("Select...", None)
            for o in orders:
                self.order_combo.addItem(f"Order #{o['id']}", o['id'])
        except Exception as e:
            print(f"Error listing purchases: {e}")

    def on_order_changed(self):
        try:
            order_id = self.order_combo.currentData()
            self.item_combo.clear()
            if order_id:
                # Fallback to all items for now
                items = purchase_model.ItemModel.list_items()
                for it in items:
                    self.item_combo.addItem(it['name'], it['id'])
        except Exception as e:
            print(f"Error on order change: {e}")

    def load_damages(self):
        try:
            damages = purchase_model.DamageModel.list_damages()
            self.table.setRowCount(0)
            for r, d in enumerate(damages):
                self.table.insertRow(r)
                self.table.setItem(r, 0, QTableWidgetItem(str(d.get('id', ''))))
                self.table.setItem(r, 1, QTableWidgetItem(str(d.get('created_at', ''))[:10]))
                self.table.setItem(r, 2, QTableWidgetItem(str(d.get('category', ''))))
                self.table.setItem(r, 3, QTableWidgetItem(str(d.get('status', 'Reported')).upper()))
        except Exception as e:
            print(f"Error loading damages: {e}")

    def handle_add(self):
        order_id = self.order_combo.currentData()
        item_id = self.item_combo.currentData()
        category = self.category_combo.currentText()
        description = self.desc_input.toPlainText().strip()
        qty_str = self.qty_input.text().strip()

        if not order_id or not item_id or not description or not qty_str:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if not qty_str.isdigit():
            QMessageBox.warning(self, "Error", "Quantity must be a number.")
            return

        try:
            success = purchase_model.DamageModel.log_damage(
                item_id=item_id,
                quantity=int(qty_str),
                reason=description,
                created_by="Admin",
                purchase_id=order_id,
                category=category
            )
            if success:
                QMessageBox.information(self, "Success", "Report added.")
                self.load_damages()
                self.desc_input.clear()
                self.qty_input.clear()
            else:
                QMessageBox.critical(self, "Error", "Failed to save report.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            
