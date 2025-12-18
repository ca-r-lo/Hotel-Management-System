from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QComboBox, QFrame, QMessageBox, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit,
    QAbstractItemView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

# --- Shared Style Constants ---
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


class AddDamageReportDialog(QDialog):
    """Dialog for adding a new damage report."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADD REPORT")
        self.setFixedSize(550, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Set dialog background
        self.setStyleSheet("QDialog { background-color: white; }")

        # Title
        title = QLabel("ADD REPORT")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {STYLE_NAVY}; padding-bottom: 10px; border-bottom: 2px solid {STYLE_BORDER};")
        layout.addWidget(title)

        # Form fields
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Order ID (ComboBox)
        order_row = QHBoxLayout()
        order_label = QLabel("ORDER ID:")
        order_label.setFixedWidth(120)
        order_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        self.order_cb = QComboBox()
        self.order_cb.setFixedHeight(35)
        self.order_cb.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        order_row.addWidget(order_label)
        order_row.addWidget(self.order_cb)
        form_layout.addLayout(order_row)

        # Report Date
        date_row = QHBoxLayout()
        date_label = QLabel("REPORT DATE:")
        date_label.setFixedWidth(120)
        date_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setFixedHeight(35)
        self.date_edit.setStyleSheet(f"""
            QDateEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QDateEdit:hover {{ border-color: {STYLE_BLUE}; }}
        """)
        date_row.addWidget(date_label)
        date_row.addWidget(self.date_edit)
        form_layout.addLayout(date_row)

        # Category
        category_row = QHBoxLayout()
        category_label = QLabel("CATEGORY:")
        category_label.setFixedWidth(120)
        category_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        self.category_cb = QComboBox()
        self.category_cb.addItems(["Broken", "Expired", "Lost", "Defective", "Other"])
        self.category_cb.setFixedHeight(35)
        self.category_cb.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        category_row.addWidget(category_label)
        category_row.addWidget(self.category_cb)
        form_layout.addLayout(category_row)

        # Description
        desc_label = QLabel("DESCRIPTION:")
        desc_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(desc_label)
        
        self.description_edit = QTextEdit()
        self.description_edit.setFixedHeight(120)
        self.description_edit.setPlaceholderText("Describe the damage...")
        self.description_edit.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QTextEdit:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.description_edit)

        layout.addLayout(form_layout)

        # Buttons
        button_row = QHBoxLayout()
        button_row.addStretch()
        
        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.setFixedSize(100, 40)
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {STYLE_BORDER};
                color: #6b7280;
                font-weight: bold;
                border-radius: 4px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BG_LIGHT}; }}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.add_btn = QPushButton("ADD")
        self.add_btn.setFixedSize(100, 40)
        self.add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY};
                color: white;
                border: none;
                font-weight: bold;
                border-radius: 4px;
            }}
            QPushButton:hover {{ background-color: #0056b3; }}
        """)
        
        button_row.addWidget(self.cancel_btn)
        button_row.addWidget(self.add_btn)
        layout.addLayout(button_row)

    def get_data(self):
        """Return the form data."""
        return {
            'purchase_id': self.order_cb.currentData(),
            'order_display': self.order_cb.currentText(),
            'report_date': self.date_edit.date().toString("yyyy-MM-dd"),
            'category': self.category_cb.currentText(),
            'description': self.description_edit.toPlainText()
        }


class ReportDamagesDialog(QDialog):
    """Main dialog for viewing and managing damage reports."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("REPORT DAMAGES")
        self.setMinimumSize(1200, 700)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(20)
        
        # Set dialog background to white
        self.setStyleSheet("QDialog { background-color: white; }")

        # Header with Add Button
        header_layout = QHBoxLayout()
        
        title = QLabel("REPORT DAMAGES")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY};")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # New Report Button
        self.new_report_btn = QPushButton("+ New Report...")
        self.new_report_btn.setFixedHeight(40)
        self.new_report_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_report_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BLUE}; }}
        """)
        header_layout.addWidget(self.new_report_btn)
        
        root.addLayout(header_layout)

        # Damages Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "REPORT ID", "REPORT DATE", "ORDER ID", "CATEGORY", "DESCRIPTION", "STATUS"
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
                padding: 5px;
                color: {STYLE_NAVY};
            }}
        """)
        
        # Make table responsive
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # REPORT ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # REPORT DATE
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # ORDER ID
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # CATEGORY
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # DESCRIPTION
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # STATUS
        self.table.verticalHeader().setVisible(False)
        
        root.addWidget(self.table)

        # Close Button
        close_row = QHBoxLayout()
        close_row.addStretch()
        self.close_btn = QPushButton("CLOSE")
        self.close_btn.setFixedSize(120, 45)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {STYLE_BORDER};
                color: #6b7280;
                font-weight: bold;
                border-radius: 2px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BG_LIGHT}; }}
        """)
        self.close_btn.clicked.connect(self.accept)
        close_row.addWidget(self.close_btn)
        root.addLayout(close_row)

    def populate_table(self, damages):
        """Populate table with damage reports."""
        self.table.setRowCount(len(damages))
        
        for r_idx, damage in enumerate(damages):
            # Set row height
            self.table.setRowHeight(r_idx, 45)
            
            # Report ID
            id_item = QTableWidgetItem(str(damage.get('id', '')))
            self.table.setItem(r_idx, 0, id_item)
            
            # Report Date
            date_item = QTableWidgetItem(str(damage.get('created_at', '')))
            self.table.setItem(r_idx, 1, date_item)
            
            # Order ID
            order_item = QTableWidgetItem(str(damage.get('purchase_id', '-')))
            self.table.setItem(r_idx, 2, order_item)
            
            # Category
            category_item = QTableWidgetItem(damage.get('category', '-'))
            self.table.setItem(r_idx, 3, category_item)
            
            # Description (truncated)
            description = damage.get('reason', '-')
            if len(description) > 80:
                description = description[:80] + '...'
            desc_item = QTableWidgetItem(description)
            desc_item.setToolTip(damage.get('reason', '-'))  # Show full description on hover
            self.table.setItem(r_idx, 4, desc_item)
            
            # Status with badge
            status = damage.get('status', 'Reported')
            status_item = QTableWidgetItem(status.upper())
            
            # Color code status
            from PyQt6.QtGui import QBrush, QColor
            if status.lower() == 'reported':
                status_item.setForeground(QBrush(QColor("#f59e0b")))  # Orange
            elif status.lower() == 'resolved':
                status_item.setForeground(QBrush(QColor("#10b981")))  # Green
            
            self.table.setItem(r_idx, 5, status_item)

