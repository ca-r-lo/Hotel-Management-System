from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QDialog)
from PyQt6.QtCore import Qt
from views.order_stocks import OrderStocksDialog
from models import purchase as purchase_model

# import AddItemDialog, OrderStocksDialog

class PurchasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Using a layout that fills the widget
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # 1. ACTION BUTTONS ROW
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        actions = ["ORDER STOCKS", "SUPPLIERS", "TRACK ORDERS", "REPORT DAMAGES"]
        
        for text in actions:
            btn = QPushButton(text)
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white; border: 1px solid #d1d5db;
                    border-radius: 2px; font-weight: 700; font-size: 11px;
                    color: #374151; letter-spacing: 0.5px;
                }
                QPushButton:hover { background-color: #f3f4f6; border-color: #0056b3; color: #0056b3; }
            """)
            actions_layout.addWidget(btn)
            # wire button actions
            if text == "ORDER STOCKS":
                btn.clicked.connect(self.open_order_stocks)
            if text == "SUPPLIERS":
                pass
                # btn.clicked.connect(self.open_suppliers)
            if text == "TRACK ORDERS":
                pass
                # btn.clicked.connect(self.open_track_orders)
        self.layout.addLayout(actions_layout)

        table_container = QFrame()
        table_container.setStyleSheet("""
            QFrame {
                background-color: white; 
                border: 1px solid #d1d5db; 
                border-radius: 2px;
            }
        """)
        container_layout = QVBoxLayout(table_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Header Label with a solid background
        table_header = QLabel("PURCHASE TRANSACTION HISTORY")
        table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_header.setFixedHeight(50)
        table_header.setStyleSheet("""
            font-weight: 800; font-size: 11px; color: #4b5563; 
            background-color: #f9fafb; border-bottom: 1px solid #d1d5db;
            letter-spacing: 1px;
        """)
        container_layout.addWidget(table_header)

        # 3. TABLE STYLING
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "DATE", "SUPPLIER", "TOTAL AMOUNT", "STATUS"])
        
        # Professional Table Stylesheet
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setShowGrid(False) # Hide internal grid for a cleaner look
        self.history_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #fcfcfd;
                border: none;
                font-size: 13px;
                color: #111827;
                selection-background-color: #eff6ff;
                selection-color: #0056b3;
            }
            QHeaderView::section {
                background-color: white;
                padding-left: 15px;
                height: 45px;
                border: none;
                border-bottom: 2px solid #f3f4f6;
                font-weight: bold;
                font-size: 10px;
                color: #6b7280;
                text-transform: uppercase;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f3f4f6;
            }
        """)

        # Responsive column sizing
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.verticalHeader().setDefaultSectionSize(50) # Set row height

        container_layout.addWidget(self.history_table)
        self.layout.addWidget(table_container)

        try:
            self.load_history()
        except Exception:
            pass

    def open_order_stocks(self):
        dlg = OrderStocksDialog(self)
        res = dlg.exec()
        try:
            if res == QDialog.DialogCode.Accepted:
                self.load_history()
        except Exception:
            self.load_history()

    # def open_suppliers(self):
    #     try:
    #         from views.suppliers import SuppliersDialog
    #         dlg = SuppliersDialog(self)
    #         res = dlg.exec()
    #         try:
    #             if res == QDialog.DialogCode.Accepted:
    #                 self.load_history()
    #         except Exception:
    #             self.load_history()
    #     except Exception:
    #         pass

    # def open_track_orders(self):
    #     try:
    #         from views.track_orders import TrackOrdersDialog
    #         dlg = TrackOrdersDialog(self, supplier_id=None)
    #         res = dlg.exec()
    #         try:
    #             if res == QDialog.DialogCode.Accepted:
    #                 self.load_history()
    #         except Exception:
    #             self.load_history()
    #     except Exception:
    #         pass

    # Inside PurchasePage class
    def load_history(self, data):
        self.history_table.setRowCount(len(data))
        for r_idx, row in enumerate(data):
            # Format the data for the table cells
            order_id = f"#{row.get('id', 0):0>4}"
            date = str(row.get('created_at', ''))[:10]
            total = f"₱ {float(row.get('total_amount', 0)):,.2f}"
            status = str(row.get('status', 'PENDING')).upper()
            
            values = [order_id, date, "GENERAL VENDOR", total, status]
            
            for c_idx, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(r_idx, c_idx, item)