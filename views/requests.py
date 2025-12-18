from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QScrollArea, QDialog, QLineEdit, QTextEdit, QSpinBox, QComboBox, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Style constants
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


class SendRequestDialog(QDialog):
    """Dialog for creating a new stock request."""
    
    def __init__(self, parent=None, department=None, user_name=None):
        super().__init__(parent)
        self.department = department
        self.user_name = user_name
        self.setWindowTitle("SEND REQUEST")
        self.setFixedSize(550, 520)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.setStyleSheet(f"""
            QDialog {{ 
                background-color: white; 
            }}
            QLabel {{
                color: {STYLE_NAVY};
            }}
        """)
        
        # Title
        title = QLabel("SEND REQUEST")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY}; border: none;")
        layout.addWidget(title)
        
        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)
        
        # Item Name
        item_label = QLabel("ITEM NAME:")
        item_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 11px; border: none;")
        form_layout.addWidget(item_label)
        
        self.item_edit = QLineEdit()
        self.item_edit.setPlaceholderText("Enter item name")
        self.item_edit.setFixedHeight(40)
        self.item_edit.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QLineEdit:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.item_edit)
        
        # Quantity
        qty_label = QLabel("QUANTITY:")
        qty_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 11px; border: none;")
        form_layout.addWidget(qty_label)
        
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 999999)
        self.qty_spin.setValue(1)
        self.qty_spin.setFixedHeight(40)
        self.qty_spin.setStyleSheet(f"""
            QSpinBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QSpinBox:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.qty_spin)
        
        # Unit
        unit_label = QLabel("UNIT:")
        unit_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 11px; border: none;")
        form_layout.addWidget(unit_label)
        
        self.unit_edit = QLineEdit()
        self.unit_edit.setPlaceholderText("e.g., pcs, boxes, liters")
        self.unit_edit.setFixedHeight(40)
        self.unit_edit.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QLineEdit:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.unit_edit)
        
        # Reason
        reason_label = QLabel("REASON:")
        reason_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 11px; border: none;")
        form_layout.addWidget(reason_label)
        
        self.reason_edit = QTextEdit()
        self.reason_edit.setPlaceholderText("Explain why you need this item")
        self.reason_edit.setFixedHeight(90)
        self.reason_edit.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QTextEdit:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.reason_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_row = QHBoxLayout()
        button_row.addStretch()
        
        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.setFixedSize(110, 42)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 2px solid {STYLE_BORDER};
                color: #6b7280;
                font-weight: bold;
                font-size: 11px;
                border-radius: 4px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{ 
                border-color: {STYLE_BLUE}; 
                color: {STYLE_BLUE}; 
            }}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        button_row.addWidget(self.cancel_btn)
        
        self.send_btn = QPushButton("SEND")
        self.send_btn.setFixedSize(110, 42)
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_BLUE};
                color: white;
                border: none;
                font-weight: bold;
                font-size: 11px;
                border-radius: 4px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{ background-color: #003d82; }}
        """)
        button_row.addWidget(self.send_btn)
        
        layout.addLayout(button_row)
    
    def get_data(self):
        """Return the form data."""
        return {
            'item_name': self.item_edit.text(),
            'quantity': self.qty_spin.value(),
            'unit': self.unit_edit.text(),
            'reason': self.reason_edit.toPlainText()
        }


class RequestsPage(QWidget):
    """Department Requests page for submitting and tracking stock requests."""
    
    def __init__(self):
        super().__init__()
        self.current_role = None
        self.current_department = None
        self.current_user = None
        self.show_archived = False
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)
        
        # Header
        # header_layout = QHBoxLayout()
        
        # title = QLabel("REQUESTS")
        # title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        # title.setStyleSheet(f"color: {STYLE_NAVY}; border: none;")
        # header_layout.addWidget(title)
        # header_layout.addStretch()
        
        # self.layout.addLayout(header_layout)
        
        # Action Buttons Row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        self.btn_send_request = QPushButton("SEND REQUEST")
        self.btn_archive = QPushButton("ARCHIVE")
        self.btn_sort = QPushButton("SORT")
        
        self.action_buttons = [self.btn_send_request, self.btn_archive, self.btn_sort]
        for btn in self.action_buttons:
            btn.setFixedHeight(45)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    border: 1px solid {STYLE_BORDER};
                    border-radius: 2px;
                    font-weight: 700;
                    font-size: 10px;
                    color: #374151;
                    letter-spacing: 1px;
                    padding: 0 15px;
                }}
                QPushButton:hover {{
                    background-color: {STYLE_BG_LIGHT};
                    border-color: {STYLE_BLUE};
                    color: {STYLE_BLUE};
                }}
            """)
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        self.layout.addLayout(actions_layout)
        
        # Requests List (Scroll Area)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: #f9fafb;
                border: 1px solid {STYLE_BORDER};
                border-radius: 2px;
            }}
            QScrollBar:vertical {{
                background-color: #f9fafb;
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {STYLE_BORDER};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #9ca3af;
            }}
        """)
        
        self.requests_container = QWidget()
        self.requests_container.setStyleSheet("background-color: #f9fafb;")
        self.requests_layout = QVBoxLayout(self.requests_container)
        self.requests_layout.setContentsMargins(20, 20, 20, 20)
        self.requests_layout.setSpacing(14)
        self.requests_layout.addStretch()
        
        scroll_area.setWidget(self.requests_container)
        self.layout.addWidget(scroll_area)
