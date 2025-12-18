from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QComboBox, 
    QDateEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from models import purchase as purchase_model

# ---------------------------------------------------------
# 1. ADD ITEM DIALOG
# ---------------------------------------------------------
class AddItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADD NEW LINE ITEM")
        self.setFixedSize(450, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        self.setStyleSheet("""
            QDialog { background-color: #ffffff; }
            QLabel { 
                font-size: 10px; font-weight: 800; color: #6b7280; 
                letter-spacing: 1px; margin-bottom: 2px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #d1d5db; border-radius: 2px;
                padding: 10px; color: #111827; background-color: #ffffff;
            }
            QLineEdit:focus { border: 1.5px solid #0056b3; }
        """)

        # Fields
        self.name_le = QLineEdit()
        self.category_cb = QComboBox()
        self.category_cb.addItems(["Room Supplies", "F&B", "Cleaning", "Maintenance", "Others"])
        self.unit_le = QLineEdit()

        row = QHBoxLayout()
        v1 = QVBoxLayout(); v1.addWidget(QLabel("QUANTITY")); self.qty_sb = QSpinBox(); v1.addWidget(self.qty_sb)
        v2 = QVBoxLayout(); v2.addWidget(QLabel("UNIT PRICE (₱)")); self.price_ds = QDoubleSpinBox(); v2.addWidget(self.price_ds)
        row.addLayout(v1); row.addLayout(v2)
        
        self.qty_sb.setRange(1, 99999); self.price_ds.setRange(0, 1000000); self.price_ds.setDecimals(2)

        # Calculation Area
        total_frame = QFrame()
        total_frame.setStyleSheet("background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 1px;")
        total_frame.setMinimumHeight(80)

        total_lay = QVBoxLayout(total_frame)
        total_lay.setContentsMargins(15, 10, 15, 10) # Added explicit margins
        total_lay.setSpacing(0)

        self.total_le = QLineEdit("₱ 0.00")
        self.total_le.setReadOnly(True)
        self.total_le.setStyleSheet("""
            QLineEdit {
                border: none; 
                background: transparent; 
                font-size: 22px; 
                font-weight: bold; 
                color: #0056b3; 
                padding-top: 2px;
                padding-bottom: 2px;
            }
        """)
        total_lay.addWidget(QLabel("TOTAL AMOUNT"))
        total_lay.addWidget(self.total_le)

        layout.addWidget(QLabel("ITEM NAME"))
        layout.addWidget(self.name_le)
        layout.addWidget(QLabel("CATEGORY"))
        layout.addWidget(self.category_cb)
        layout.addWidget(QLabel("UNIT"))
        layout.addWidget(self.unit_le)
        layout.addLayout(row)
        layout.addWidget(total_frame)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("ADD TO LIST")
        self.add_btn.setStyleSheet("background-color: #111827; color: white; padding: 12px; font-weight: bold; border-radius: 2px;")
        btn_row.addWidget(self.add_btn)
        layout.addLayout(btn_row)

        self.qty_sb.valueChanged.connect(self.recalc)
        self.price_ds.valueChanged.connect(self.recalc)
        self.add_btn.clicked.connect(self.on_add)

    def recalc(self):
        total = self.qty_sb.value() * self.price_ds.value()
        self.total_le.setText(f"₱ {total:,.2f}")

    def get_data(self):
        return {
            'item_name': self.name_le.text().strip(),
            'category': self.category_cb.currentText(),
            'unit': self.unit_le.text().strip(),
            'qty': self.qty_sb.value(),
            'price': self.price_ds.value(),
            'total': self.qty_sb.value() * self.price_ds.value()
        }

    def on_add(self):
        if not self.name_le.text().strip():
            QMessageBox.warning(self, "Validation", "Item name is required.")
            return
        self.accept()


# ---------------------------------------------------------
# 2. ORDER STOCKS DIALOG (Clean Table-Only View)
# ---------------------------------------------------------
class OrderStocksDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PROCUREMENT ORDER ENTRY")
        self.resize(1100, 700)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(20)
        self.setStyleSheet("QDialog { background-color: #f4f7f9; }")

        # ITEMS TABLE (The primary focus)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ITEM", "CATEGORY", "UNIT", "QTY", "PRICE", "TOTAL", "ACTION"])
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white; border: 1px solid #d1d5db; 
                alternate-background-color: #fcfcfd; border-radius: 2px;
                color: #111827; font-size: 13px;
            }
            QHeaderView::section {
                background-color: #f9fafb; padding: 12px; border: none;
                border-bottom: 2px solid #e5e7eb; font-weight: bold; font-size: 10px; color: #4b5563;
                text-transform: uppercase;
            }
            QTableWidget::item { border-bottom: 1px solid #f3f4f6; padding: 10px; }
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table)

        # FOOTER LOGIC
        footer_row = QHBoxLayout()
        self.add_item_btn = QPushButton("+ ADD NEW LINE")
        self.add_item_btn.setStyleSheet("border: 1px dashed #0056b3; color: #0056b3; font-weight: bold; padding: 12px; border-radius: 2px;")
        
        self.total_lbl = QLabel("TOTAL AMOUNT: ₱ 0.00")
        self.total_lbl.setStyleSheet("font-size: 22px; font-weight: 900; color: #111827; border: none;")
        
        footer_row.addWidget(self.add_item_btn)
        footer_row.addStretch()
        footer_row.addWidget(self.total_lbl)
        root.addLayout(footer_row)

        # CONFIRMATION
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.save_btn = QPushButton("CONFIRM PURCHASE ORDER")
        self.save_btn.setStyleSheet("background-color: #0056b3; color: white; padding: 15px 40px; font-weight: 900; border-radius: 2px;")
        btn_row.addWidget(self.save_btn)
        root.addLayout(btn_row)

        # Connections
        self.add_item_btn.clicked.connect(self.open_add_item)
        self.save_btn.clicked.connect(self.on_save)

    def open_add_item(self):
        dlg = AddItemDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d = dlg.get_data()
            r = self.table.rowCount()
            self.table.insertRow(r)
            
            items = [d['item_name'], d['category'], d['unit'], str(d['qty']), 
                     f"₱ {d['price']:,.2f}", f"₱ {d['total']:,.2f}"]
            
            for i, val in enumerate(items):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(r, i, item)

            rm_btn = QPushButton("REMOVE")
            rm_btn.setStyleSheet("color: #dc3545; border: none; font-size: 9px; font-weight: bold; background: transparent;")
            # connect to a handler that finds the button's row and removes it, then recalculates total
            rm_btn.clicked.connect(lambda _, b=rm_btn: self.remove_row(b))
            self.table.setCellWidget(r, 6, rm_btn)
            self.recalc_total()

    def remove_row(self, button):
        """Find the row that contains the given button and remove it."""
        for rr in range(self.table.rowCount()):
            w = self.table.cellWidget(rr, 6)
            if w is button:
                self.table.removeRow(rr)
                self.recalc_total()
                return

    def recalc_total(self):
        total = 0.0
        for r in range(self.table.rowCount()):
            try:
                txt = self.table.item(r, 5).text().replace("₱", "").replace(",", "").strip()
                total += float(txt)
            except: continue
        self.total_lbl.setText(f"TOTAL AMOUNT: ₱ {total:,.2f}")

    def on_save(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Validation", "Please add at least one item.")
            return
        # collect items from table
        items = []
        for r in range(self.table.rowCount()):
            try:
                name = self.table.item(r, 0).text().strip()
                qty = int(self.table.item(r, 3).text())
                price_txt = self.table.item(r, 4).text().replace("₱", "").replace(",", "").strip()
                price = float(price_txt) if price_txt else 0.0
                items.append({ 'item_name': name, 'qty': qty, 'price': price })
            except Exception:
                continue

        try:
            # supplier_id / expected_date not provided in this dialog; pass None
            pid = purchase_model.PurchaseModel.create_purchase(None, items, None, None)
            QMessageBox.information(self, "Saved", f"Purchase Order created (ID: {pid})")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create purchase order:\n{e}")


# ---------------------------------------------------------
# 3. MAIN PURCHASE PAGE (History View)
# ---------------------------------------------------------
class PurchasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # TOP ACTIONS
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        actions = ["ORDER STOCKS", "SUPPLIERS", "TRACK ORDERS", "REPORT DAMAGES"]
        
        for text in actions:
            btn = QPushButton(text)
            btn.setFixedHeight(45)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white; border: 1px solid #d1d5db;
                    border-radius: 2px; font-weight: 700; font-size: 10px;
                    color: #374151; letter-spacing: 1px;
                }
                QPushButton:hover { background-color: #f9fafb; border-color: #0056b3; color: #0056b3; }
            """)
            if text == "ORDER STOCKS":
                btn.clicked.connect(self.open_order_stocks)
            actions_layout.addWidget(btn)
        self.layout.addLayout(actions_layout)

        # TRANSACTION TABLE
        table_container = QFrame()
        table_container.setStyleSheet("background-color: white; border: 1px solid #d1d5db; border-radius: 2px;")
        container_layout = QVBoxLayout(table_container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        table_header = QLabel("PURCHASE TRANSACTION HISTORY")
        table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_header.setFixedHeight(50)
        table_header.setStyleSheet("""
            font-weight: 800; font-size: 11px; color: #4b5563; 
            background-color: #f9fafb; border-bottom: 1px solid #d1d5db;
            letter-spacing: 1.5px;
        """)
        container_layout.addWidget(table_header)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "DATE", "SUPPLIER", "TOTAL AMOUNT", "STATUS"])
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setShowGrid(False)
        self.history_table.setStyleSheet("""
            QTableWidget { background-color: white; border: none; font-size: 13px; alternate-background-color: #fcfcfd; }
            QHeaderView::section { background-color: white; padding: 15px; border: none; border-bottom: 2px solid #f3f4f6; font-weight: bold; font-size: 10px; color: #6b7280; text-transform: uppercase;}
            QTableWidget::item { border-bottom: 1px solid #f3f4f6; padding: 10px; }
        """)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        
        container_layout.addWidget(self.history_table)
        self.layout.addWidget(table_container)

        self.load_history()

    def open_order_stocks(self):
        dlg = OrderStocksDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_history()

    def load_history(self):
        try:
            data = purchase_model.PurchaseModel.list_purchases()
        except Exception:
            data = []

        self.history_table.setRowCount(len(data))
        for r_idx, row in enumerate(data):
            if isinstance(row, dict):
                order_id = str(row.get('id', ''))
                date = str(row.get('created_at', ''))[:10]
                supplier_name = ''
                try:
                    sup = purchase_model.SupplierModel.get_supplier(row.get('supplier_id'))
                    supplier_name = sup.get('name') if sup else ''
                except Exception:
                    supplier_name = str(row.get('supplier_id', ''))
                total = f"₱ {float(row.get('total_amount', 0)):.2f}"
                status = str(row.get('status', ''))
                values = [order_id, date, supplier_name, total, status]
            else:
                values = list(row)

            for c_idx, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                try:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                except Exception:
                    item.setTextAlignment(int(Qt.AlignmentFlag.AlignCenter))
                self.history_table.setItem(r_idx, c_idx, item)