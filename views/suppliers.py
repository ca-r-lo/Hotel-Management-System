from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QTextEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor

# --- Shared Style Constants ---
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


def create_edit_icon(size=20):
    """Create a simple edit/pencil icon."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Draw pencil shape
    pen_color = QColor("#FFFFFF")
    painter.setPen(pen_color)
    painter.setBrush(pen_color)
    
    # Pencil body
    points = [
        (size * 0.7, size * 0.2),
        (size * 0.8, size * 0.3),
        (size * 0.4, size * 0.7),
        (size * 0.3, size * 0.6)
    ]
    from PyQt6.QtCore import QPointF
    from PyQt6.QtGui import QPolygonF
    polygon = QPolygonF([QPointF(x, y) for x, y in points])
    painter.drawPolygon(polygon)
    
    # Pencil tip
    tip_points = [
        (size * 0.3, size * 0.6),
        (size * 0.4, size * 0.7),
        (size * 0.2, size * 0.8)
    ]
    tip_polygon = QPolygonF([QPointF(x, y) for x, y in tip_points])
    painter.setBrush(QColor("#FFD700"))
    painter.drawPolygon(tip_polygon)
    
    painter.end()
    return QIcon(pixmap)


def create_delete_icon(size=20):
    """Create a simple trash/delete icon."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen_color = QColor("#FFFFFF")
    painter.setPen(pen_color)
    painter.setBrush(pen_color)
    
    # Trash can body
    body_width = size * 0.5
    body_height = size * 0.5
    body_x = (size - body_width) / 2
    body_y = size * 0.35
    painter.drawRect(int(body_x), int(body_y), int(body_width), int(body_height))
    
    # Trash can lid
    lid_width = size * 0.6
    lid_x = (size - lid_width) / 2
    lid_y = size * 0.25
    painter.drawRect(int(lid_x), int(lid_y), int(lid_width), int(size * 0.1))
    
    # Handle on lid
    handle_width = size * 0.3
    handle_x = (size - handle_width) / 2
    handle_y = size * 0.15
    painter.drawRect(int(handle_x), int(handle_y), int(handle_width), int(size * 0.1))
    
    painter.end()
    return QIcon(pixmap)


class AddSupplierDialog(QDialog):
    def __init__(self, parent=None, supplier_data=None):
        super().__init__(parent)
        self.supplier_data = supplier_data
        self.is_edit_mode = supplier_data is not None
        self.setWindowTitle("EDIT SUPPLIER" if self.is_edit_mode else "ADD SUPPLIER")
        self.setFixedSize(550, 600)
        self.init_ui()
        
        if self.is_edit_mode:
            self.populate_fields()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.setStyleSheet(f"""
            QDialog {{ background-color: #ffffff; }}
            QLabel {{ 
                font-size: 10px; font-weight: 800; color: #6b7280; 
                letter-spacing: 1px; margin-bottom: 5px;
            }}
            QLineEdit, QTextEdit {{
                border: 1px solid {STYLE_BORDER}; border-radius: 2px; 
                padding: 12px; color: {STYLE_NAVY}; background-color: #ffffff;
                font-size: 13px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 2px solid {STYLE_BLUE};
            }}
        """)

        # Title
        title = QLabel("EDIT SUPPLIER" if self.is_edit_mode else "ADD SUPPLIER")
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY}; font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(title)

        # Supplier Name
        layout.addWidget(QLabel("SUPPLIER NAME"))
        self.name_le = QLineEdit()
        self.name_le.setPlaceholderText("e.g., ABC Supplies Inc.")
        layout.addWidget(self.name_le)

        # Contact Name
        layout.addWidget(QLabel("CONTACT PERSON"))
        self.contact_name_le = QLineEdit()
        self.contact_name_le.setPlaceholderText("e.g., John Doe")
        layout.addWidget(self.contact_name_le)

        # Email
        layout.addWidget(QLabel("E-MAIL"))
        self.email_le = QLineEdit()
        self.email_le.setPlaceholderText("e.g., supplier@example.com")
        layout.addWidget(self.email_le)

        # Phone
        layout.addWidget(QLabel("CONTACT #"))
        self.phone_le = QLineEdit()
        self.phone_le.setPlaceholderText("e.g., +1 234 567 8900")
        layout.addWidget(self.phone_le)

        # Address
        layout.addWidget(QLabel("ADDRESS"))
        self.address_te = QTextEdit()
        self.address_te.setPlaceholderText("Enter complete address...")
        self.address_te.setMaximumHeight(100)
        layout.addWidget(self.address_te)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        
        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.setFixedHeight(45)
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; 
                border: 2px solid {STYLE_BORDER}; 
                color: #6b7280; 
                font-weight: bold; 
                border-radius: 2px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BG_LIGHT}; }}
        """)
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("UPDATE" if self.is_edit_mode else "ADD")
        self.save_btn.setFixedHeight(45)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY}; 
                color: white; 
                font-weight: bold; 
                border-radius: 2px;
                padding: 0 30px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BLUE}; }}
        """)
        self.save_btn.clicked.connect(self.on_save)

        btn_row.addStretch()
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        layout.addLayout(btn_row)

    def populate_fields(self):
        """Fill form fields with existing supplier data."""
        if self.supplier_data:
            self.name_le.setText(self.supplier_data.get('name', ''))
            self.contact_name_le.setText(self.supplier_data.get('contact_name', ''))
            self.email_le.setText(self.supplier_data.get('email', ''))
            self.phone_le.setText(self.supplier_data.get('phone', ''))
            self.address_te.setPlainText(self.supplier_data.get('address', ''))

    def on_save(self):
        # Validation
        if not self.name_le.text().strip():
            QMessageBox.warning(self, "Validation", "Supplier name is required.")
            return
        
        self.accept()

    def get_data(self):
        return {
            'name': self.name_le.text().strip(),
            'contact_name': self.contact_name_le.text().strip(),
            'email': self.email_le.text().strip(),
            'phone': self.phone_le.text().strip(),
            'address': self.address_te.toPlainText().strip()
        }


class SuppliersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SUPPLIERS MANAGEMENT")
        self.resize(1100, 700)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(20)
        self.setStyleSheet("QDialog { background-color: #f4f7f9; }")

        # Header
        header_row = QHBoxLayout()
        title = QLabel("SUPPLIERS")
        title.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY}; border: none;")
        header_row.addWidget(title)
        header_row.addStretch()

        # Add Supplier Button
        self.add_btn = QPushButton("+ ADD SUPPLIER")
        self.add_btn.setFixedHeight(45)
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY}; 
                color: white; 
                font-weight: bold; 
                padding: 0 25px;
                border-radius: 2px;
                font-size: 11px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BLUE}; }}
        """)
        # Controller will connect this button
        header_row.addWidget(self.add_btn)
        root.addLayout(header_row)

        # Suppliers Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "SUPPLIER NAME", "CONTACT PERSON", "E-MAIL", "CONTACT #", "ADDRESS", "ACTIONS"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
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
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # SUPPLIER NAME
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # CONTACT PERSON
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # E-MAIL
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # CONTACT #
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # ADDRESS
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # ACTIONS
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

    def populate_table(self, suppliers, controller):
        """Populate table with suppliers data using controller for actions."""
        self.table.setRowCount(len(suppliers))
        
        for r_idx, supplier in enumerate(suppliers):
            # Set row height to accommodate icon buttons
            self.table.setRowHeight(r_idx, 45)
            
            # Supplier Name
            name_item = QTableWidgetItem(supplier.get('name', ''))
            name_item.setData(Qt.ItemDataRole.UserRole, supplier.get('id'))
            self.table.setItem(r_idx, 0, name_item)
            
            # Contact Person
            contact_item = QTableWidgetItem(supplier.get('contact_name', '-'))
            self.table.setItem(r_idx, 1, contact_item)
            
            # Email
            email_item = QTableWidgetItem(supplier.get('email', '-'))
            self.table.setItem(r_idx, 2, email_item)
            
            # Phone
            phone_item = QTableWidgetItem(supplier.get('phone', '-'))
            self.table.setItem(r_idx, 3, phone_item)
            
            # Address (truncated if too long)
            address = supplier.get('address', '-')
            if len(address) > 50:
                address = address[:50] + '...'
            address_item = QTableWidgetItem(address)
            address_item.setToolTip(supplier.get('address', '-'))  # Show full address on hover
            self.table.setItem(r_idx, 4, address_item)
            
            # Action Buttons
            action_widget = QFrame()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            action_layout.setSpacing(6)
            
            # Edit button with icon
            edit_btn = QPushButton()
            edit_btn.setIcon(create_edit_icon(18))
            edit_btn.setFixedSize(35, 35)
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.setToolTip("Edit Supplier")
            edit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {STYLE_BLUE};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }}
                QPushButton:hover {{ 
                    background-color: #003d82;
                    border: 2px solid #ffffff;
                }}
            """)
            edit_btn.clicked.connect(lambda checked, s=supplier: controller.handle_edit_supplier(s))
            
            # Delete button with icon
            delete_btn = QPushButton()
            delete_btn.setIcon(create_delete_icon(18))
            delete_btn.setFixedSize(35, 35)
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.setToolTip("Delete Supplier")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }
                QPushButton:hover { 
                    background-color: #c82333;
                    border: 2px solid #ffffff;
                }
            """)
            delete_btn.clicked.connect(lambda checked, s=supplier: controller.handle_delete_supplier(s))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()
            
            self.table.setCellWidget(r_idx, 5, action_widget)
