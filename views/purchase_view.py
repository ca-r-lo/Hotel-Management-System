from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, 
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt

class PurchasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # Action Buttons Row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        self.btn_order_stocks = QPushButton("ORDER STOCKS")
        self.btn_suppliers = QPushButton("SUPPLIERS")
        self.btn_track_orders = QPushButton("TRACK ORDERS")
        self.btn_report_damages = QPushButton("REPORT DAMAGES")

        self.actions = [self.btn_order_stocks, self.btn_suppliers, self.btn_track_orders, self.btn_report_damages]
        for btn in self.actions:
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
            actions_layout.addWidget(btn)
        self.layout.addLayout(actions_layout)

        # Transaction Table
        table_container = QFrame()
        table_container.setStyleSheet("background-color: white; border: 1px solid #d1d5db; border-radius: 2px;")
        container_layout = QVBoxLayout(table_container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        table_header = QLabel("PURCHASE TRANSACTION HISTORY")
        table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_header.setFixedHeight(50)
        table_header.setStyleSheet("font-weight: 800; font-size: 11px; color: #4b5563; background-color: #f9fafb; border-bottom: 1px solid #d1d5db;")
        container_layout.addWidget(table_header)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(9)
        self.history_table.setHorizontalHeaderLabels([
            "ORDER ID", 
            "DATE", 
            "SUPPLIER", 
            "CONTACT", 
            "EXPECTED DATE",
            "ITEMS",
            "TOTAL AMOUNT", 
            "STATUS",
            "CREATED BY"
        ])
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setShowGrid(False)
        self.history_table.setStyleSheet("""
            QTableWidget { 
                background-color: white; 
                border: none; 
                font-size: 13px; 
                alternate-background-color: #fcfcfd;
                color: #111827;
            }
            QHeaderView::section { 
                background-color: white; 
                padding: 15px; 
                border: none; 
                border-bottom: 2px solid #f3f4f6; 
                font-weight: bold; 
                font-size: 10px; 
                color: #6b7280; 
                text-transform: uppercase;
            }
            QTableWidget::item { 
                border-bottom: 1px solid #f3f4f6; 
                padding: 10px;
                color: #111827;
            }
        """)
        # Make table responsive - use Stretch for most columns with minimum widths
        header = self.history_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ORDER ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # DATE
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # SUPPLIER
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # CONTACT
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # EXPECTED DATE
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # ITEMS
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # TOTAL AMOUNT
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # STATUS
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)  # CREATED BY
        self.history_table.verticalHeader().setVisible(False)
        container_layout.addWidget(self.history_table)
        self.layout.addWidget(table_container)

    def load_history(self, data):
        self.history_table.setRowCount(len(data))
        for r_idx, row in enumerate(data):
            order_id = f"#{row.get('id', 0):0>4}"
            created_date = str(row.get('created_at', ''))[:10] if row.get('created_at') else 'N/A'
            supplier_name = row.get('supplier_name', 'N/A') if row.get('supplier_name') else 'N/A'
            supplier_contact = row.get('supplier_contact', '-') if row.get('supplier_contact') else '-'
            expected_date = str(row.get('expected_date', ''))[:10] if row.get('expected_date') else 'N/A'
            item_count = str(row.get('item_count', 0)) + ' items'
            total = f"₱ {float(row.get('total_amount', 0)):,.2f}"
            status = str(row.get('status', 'PENDING')).upper()
            created_by = row.get('created_by', 'N/A') if row.get('created_by') else 'N/A'
            
            vals = [order_id, created_date, supplier_name, supplier_contact, expected_date, item_count, total, status, created_by]
            for c_idx, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(r_idx, c_idx, item)