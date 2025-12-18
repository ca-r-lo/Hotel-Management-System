"""KPI Detail Dialogs - Show detailed data when KPI cards are clicked."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

# Shared Style Constants
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


class InventoryValueDialog(QDialog):
    """Show all inventory items with their values."""
    
    def __init__(self, parent=None, department=None):
        super().__init__(parent)
        self.department = department
        self.setWindowTitle("Inventory Value Details")
        self.setMinimumSize(900, 600)
        self.resize(1000, 650)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.setStyleSheet("QDialog { background-color: white; }")
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("INVENTORY VALUE BREAKDOWN")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY};")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        if self.department:
            dept_label = QLabel(f"Department: {self.department}")
            dept_label.setStyleSheet(f"color: {STYLE_BLUE}; font-weight: bold; font-size: 14px;")
            header_layout.addWidget(dept_label)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Item Name", "Category", "Unit", "Stock Qty", "Unit Cost", "Total Value"
        ])
        
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                font-size: 13px;
                color: {STYLE_NAVY};
                alternate-background-color: #fcfcfd;
            }}
            QHeaderView::section {{
                background-color: {STYLE_BG_LIGHT};
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: bold;
                font-size: 10px;
                color: #4b5563;
                text-transform: uppercase;
            }}
            QTableWidget::item {{
                border-bottom: 1px solid #f3f4f6;
                padding: 8px;
            }}
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        # Total row
        total_frame = QFrame()
        total_frame.setStyleSheet(f"background-color: {STYLE_BG_LIGHT}; border-radius: 4px; padding: 15px;")
        total_layout = QHBoxLayout(total_frame)
        
        total_label = QLabel("GRAND TOTAL:")
        total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        total_label.setStyleSheet(f"color: {STYLE_NAVY};")
        total_layout.addWidget(total_label)
        
        total_layout.addStretch()
        
        self.total_value_label = QLabel("₱ 0.00")
        self.total_value_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.total_value_label.setStyleSheet(f"color: {STYLE_BLUE};")
        total_layout.addWidget(self.total_value_label)
        
        layout.addWidget(total_frame)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("CLOSE")
        close_btn.setFixedSize(120, 45)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY};
                color: white;
                font-weight: bold;
                border-radius: 4px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {STYLE_BLUE};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def populate_data(self, items):
        """Populate table with inventory items."""
        self.table.setRowCount(len(items))
        total_value = 0.0
        
        for row_idx, item in enumerate(items):
            self.table.setRowHeight(row_idx, 40)
            
            # Item Name
            name_item = QTableWidgetItem(item.get('name', ''))
            self.table.setItem(row_idx, 0, name_item)
            
            # Category
            category_item = QTableWidgetItem(item.get('category', 'General'))
            self.table.setItem(row_idx, 1, category_item)
            
            # Unit
            unit_item = QTableWidgetItem(item.get('unit', ''))
            self.table.setItem(row_idx, 2, unit_item)
            
            # Stock Qty
            stock_qty = int(item.get('stock_qty', 0))
            qty_item = QTableWidgetItem(str(stock_qty))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 3, qty_item)
            
            # Unit Cost
            unit_cost = float(item.get('unit_cost', 0))
            cost_item = QTableWidgetItem(f"₱ {unit_cost:,.2f}")
            cost_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 4, cost_item)
            
            # Total Value
            item_total = stock_qty * unit_cost
            total_value += item_total
            total_item = QTableWidgetItem(f"₱ {item_total:,.2f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            total_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            self.table.setItem(row_idx, 5, total_item)
        
        self.total_value_label.setText(f"₱ {total_value:,.2f}")


class WastagesDialog(QDialog):
    """Show all damage reports."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wastages Details")
        self.setMinimumSize(900, 600)
        self.resize(1000, 650)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.setStyleSheet("QDialog { background-color: white; }")
        
        # Header
        title = QLabel("WASTAGES / DAMAGE REPORTS")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY};")
        layout.addWidget(title)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Date", "Item", "Quantity", "Reason", "Reported By"
        ])
        
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                font-size: 13px;
                color: {STYLE_NAVY};
                alternate-background-color: #fcfcfd;
            }}
            QHeaderView::section {{
                background-color: {STYLE_BG_LIGHT};
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: bold;
                font-size: 10px;
                color: #4b5563;
                text-transform: uppercase;
            }}
            QTableWidget::item {{
                border-bottom: 1px solid #f3f4f6;
                padding: 8px;
            }}
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        # Total damages
        total_frame = QFrame()
        total_frame.setStyleSheet(f"background-color: {STYLE_BG_LIGHT}; border-radius: 4px; padding: 15px;")
        total_layout = QHBoxLayout(total_frame)
        
        total_label = QLabel("TOTAL WASTAGES:")
        total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        total_label.setStyleSheet(f"color: {STYLE_NAVY};")
        total_layout.addWidget(total_label)
        
        total_layout.addStretch()
        
        self.total_damages_label = QLabel("0")
        self.total_damages_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.total_damages_label.setStyleSheet(f"color: #ef4444;")
        total_layout.addWidget(self.total_damages_label)
        
        layout.addWidget(total_frame)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("CLOSE")
        close_btn.setFixedSize(120, 45)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY};
                color: white;
                font-weight: bold;
                border-radius: 4px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {STYLE_BLUE};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def populate_data(self, damages):
        """Populate table with damage reports."""
        self.table.setRowCount(len(damages))
        
        for row_idx, damage in enumerate(damages):
            self.table.setRowHeight(row_idx, 40)
            
            # Date
            date_item = QTableWidgetItem(str(damage.get('created_at', '')))
            self.table.setItem(row_idx, 0, date_item)
            
            # Item
            item_item = QTableWidgetItem(damage.get('item_name', 'Unknown'))
            self.table.setItem(row_idx, 1, item_item)
            
            # Quantity
            qty_item = QTableWidgetItem(str(damage.get('quantity', 0)))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 2, qty_item)
            
            # Reason
            reason_item = QTableWidgetItem(damage.get('reason', 'N/A'))
            self.table.setItem(row_idx, 3, reason_item)
            
            # Reported By
            reporter_item = QTableWidgetItem(damage.get('created_by', 'System'))
            self.table.setItem(row_idx, 4, reporter_item)
        
        self.total_damages_label.setText(str(len(damages)))


class LowStocksDialog(QDialog):
    """Show all items with stock below minimum level."""
    
    def __init__(self, parent=None, department=None):
        super().__init__(parent)
        self.department = department
        self.setWindowTitle("Low Stock Items")
        self.setMinimumSize(900, 600)
        self.resize(1000, 650)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.setStyleSheet("QDialog { background-color: white; }")
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("LOW STOCK ITEMS")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY};")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        if self.department:
            dept_label = QLabel(f"Department: {self.department}")
            dept_label.setStyleSheet(f"color: {STYLE_BLUE}; font-weight: bold; font-size: 14px;")
            header_layout.addWidget(dept_label)
        
        layout.addLayout(header_layout)
        
        # Info label
        info_label = QLabel("Items below minimum stock level require immediate attention")
        info_label.setStyleSheet("color: #ef4444; font-size: 12px; font-style: italic;")
        layout.addWidget(info_label)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Item Name", "Category", "Current Stock", "Min Stock", "Shortage", "Status"
        ])
        
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                font-size: 13px;
                color: {STYLE_NAVY};
                alternate-background-color: #fcfcfd;
            }}
            QHeaderView::section {{
                background-color: {STYLE_BG_LIGHT};
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: bold;
                font-size: 10px;
                color: #4b5563;
                text-transform: uppercase;
            }}
            QTableWidget::item {{
                border-bottom: 1px solid #f3f4f6;
                padding: 8px;
            }}
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("CLOSE")
        close_btn.setFixedSize(120, 45)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY};
                color: white;
                font-weight: bold;
                border-radius: 4px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {STYLE_BLUE};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def populate_data(self, items):
        """Populate table with low stock items."""
        self.table.setRowCount(len(items))
        
        for row_idx, item in enumerate(items):
            self.table.setRowHeight(row_idx, 40)
            
            # Item Name
            name_item = QTableWidgetItem(item.get('name', ''))
            self.table.setItem(row_idx, 0, name_item)
            
            # Category
            category_item = QTableWidgetItem(item.get('category', 'General'))
            self.table.setItem(row_idx, 1, category_item)
            
            # Current Stock
            current_stock = int(item.get('stock_qty', 0))
            current_item = QTableWidgetItem(str(current_stock))
            current_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if current_stock == 0:
                current_item.setForeground(QColor("#ef4444"))  # Red for out of stock
            self.table.setItem(row_idx, 2, current_item)
            
            # Min Stock
            min_stock = int(item.get('min_stock', 0))
            min_item = QTableWidgetItem(str(min_stock))
            min_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 3, min_item)
            
            # Shortage
            shortage = max(0, min_stock - current_stock)
            shortage_item = QTableWidgetItem(str(shortage))
            shortage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            shortage_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            self.table.setItem(row_idx, 4, shortage_item)
            
            # Status
            if current_stock == 0:
                status = "OUT OF STOCK"
                color = QColor("#ef4444")
            elif current_stock <= min_stock * 0.5:
                status = "CRITICAL"
                color = QColor("#f97316")
            else:
                status = "LOW"
                color = QColor("#eab308")
            
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            status_item.setForeground(color)
            self.table.setItem(row_idx, 5, status_item)
