from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class TransactionHistoryPage(QWidget):
    """Transaction History page for Directors/Owners to view all transactions."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # Filters Row
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(15)
        
        # Year Filter
        year_label = QLabel("YEAR:")
        year_label.setStyleSheet("font-weight: 700; font-size: 11px; color: #374151;")
        filters_layout.addWidget(year_label)
        
        self.year_filter = QComboBox()
        self.year_filter.setFixedHeight(40)
        self.year_filter.setFixedWidth(150)
        self.year_filter.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                color: #111827;
            }
            QComboBox:hover {
                border-color: #0056b3;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6b7280;
                margin-right: 8px;
            }
        """)
        # Populate with years (current year and previous 5 years)
        from datetime import datetime
        current_year = datetime.now().year
        for year in range(current_year, current_year - 6, -1):
            self.year_filter.addItem(str(year))
        filters_layout.addWidget(self.year_filter)
        
        filters_layout.addSpacing(20)
        
        # Month Filter
        month_label = QLabel("MONTH:")
        month_label.setStyleSheet("font-weight: 700; font-size: 11px; color: #374151;")
        filters_layout.addWidget(month_label)
        
        self.month_filter = QComboBox()
        self.month_filter.setFixedHeight(40)
        self.month_filter.setFixedWidth(150)
        self.month_filter.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                color: #111827;
            }
            QComboBox:hover {
                border-color: #0056b3;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6b7280;
                margin-right: 8px;
            }
        """)
        # Populate with months
        months = [
            "All Months",
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]
        self.month_filter.addItems(months)
        filters_layout.addWidget(self.month_filter)
        
        filters_layout.addStretch()
        
        self.layout.addLayout(filters_layout)

        # Transaction Table Container
        table_container = QFrame()
        table_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
            }
        """)
        container_layout = QVBoxLayout(table_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Table Header
        table_header = QFrame()
        table_header.setFixedHeight(60)
        table_header.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-bottom: 2px solid #e5e7eb;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)
        header_layout = QHBoxLayout(table_header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        header_label = QLabel("TRANSACTION HISTORY")
        header_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #111827; border: none;")
        header_layout.addWidget(header_label)
        
        container_layout.addWidget(table_header)

        # Transaction Table
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
                alternate-background-color: #f9fafb;
                color: #111827;
                gridline-color: transparent;
            }
            QHeaderView::section { 
                background-color: #f3f4f6; 
                padding: 12px 15px; 
                border: none; 
                border-bottom: 2px solid #e5e7eb;
                border-right: 1px solid #e5e7eb;
                font-weight: 700; 
                font-size: 11px; 
                color: #6b7280; 
                text-transform: uppercase;
            }
            QHeaderView::section:last {
                border-right: none;
            }
            QTableWidget::item { 
                border-bottom: 1px solid #f3f4f6; 
                padding: 12px 15px;
                color: #111827;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #111827;
            }
        """)
        
        # Make table responsive
        header = self.history_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ORDER ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # DATE
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)          # SUPPLIER
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # CONTACT
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # EXPECTED DATE
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # ITEMS
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # TOTAL AMOUNT
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # STATUS
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)          # CREATED BY
        
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        container_layout.addWidget(self.history_table)
        self.layout.addWidget(table_container)

    def populate_table(self, data):
        """Populate the table with transaction data."""
        self.history_table.setRowCount(0)
        
        for row_data in data:
            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            
            # ORDER ID
            order_id = QTableWidgetItem(str(row_data.get('id', '')))
            order_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row_position, 0, order_id)
            
            # DATE
            created_at = row_data.get('created_at', '')
            if created_at:
                if isinstance(created_at, str):
                    date_str = created_at[:10] if len(created_at) >= 10 else created_at
                else:
                    # datetime object
                    date_str = created_at.strftime('%Y-%m-%d')
            else:
                date_str = ''
            date = QTableWidgetItem(date_str)
            date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row_position, 1, date)
            
            # SUPPLIER
            supplier = QTableWidgetItem(str(row_data.get('supplier_name', 'N/A')))
            self.history_table.setItem(row_position, 2, supplier)
            
            # CONTACT (contact person name)
            contact = QTableWidgetItem(str(row_data.get('supplier_contact', 'N/A')))
            contact.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row_position, 3, contact)
            
            # EXPECTED DATE
            expected_date = QTableWidgetItem(str(row_data.get('expected_date', 'N/A')))
            expected_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row_position, 4, expected_date)
            
            # ITEMS
            items_count = row_data.get('items_count', 0)
            items = QTableWidgetItem(str(items_count))
            items.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row_position, 5, items)
            
            # TOTAL AMOUNT
            total = row_data.get('total_amount', 0)
            amount = QTableWidgetItem(f"₱ {total:,.2f}")
            amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.history_table.setItem(row_position, 6, amount)
            
            # STATUS
            status = row_data.get('status', 'pending')
            status_item = QTableWidgetItem(status.upper())
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Color code status
            if status.lower() == 'completed':
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif status.lower() == 'pending':
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            elif status.lower() == 'cancelled':
                status_item.setForeground(Qt.GlobalColor.red)
            
            self.history_table.setItem(row_position, 7, status_item)
            
            # CREATED BY
            created_by = QTableWidgetItem(str(row_data.get('created_by', 'N/A')))
            self.history_table.setItem(row_position, 8, created_by)

    def clear_table(self):
        """Clear all rows from the table."""
        self.history_table.setRowCount(0)
