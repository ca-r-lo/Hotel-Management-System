from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor

# --- Shared Style Constants ---
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


def create_status_badge_icon(status, size=16):
    """Create a colored badge icon based on status."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Color based on status
    if status.lower() == 'pending':
        color = QColor("#fbbf24")  # Yellow
    elif status.lower() == 'delivered':
        color = QColor("#10b981")  # Green
    elif status.lower() == 'cancelled':
        color = QColor("#ef4444")  # Red
    else:  # draft or other
        color = QColor("#6b7280")  # Gray
    
    painter.setBrush(color)
    painter.setPen(color)
    painter.drawEllipse(2, 2, size - 4, size - 4)
    
    painter.end()
    return QIcon(pixmap)


class TrackOrdersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TRACK ORDERS")
        self.setMinimumSize(1200, 700)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(20)
        
        # Set dialog background to white
        self.setStyleSheet("QDialog { background-color: white; }")

        # Header with Filter
        header_layout = QHBoxLayout()
        
        title = QLabel("TRACK ORDERS")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY};")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Status Filter
        filter_label = QLabel("Filter by Status:")
        filter_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 12px;")
        header_layout.addWidget(filter_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Draft", "Pending", "Delivered", "Cancelled"])
        self.status_filter.setFixedWidth(150)
        self.status_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: white;
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                color: {STYLE_NAVY};
                font-size: 12px;
                font-weight: bold;
            }}
            QComboBox:hover {{
                border-color: {STYLE_BLUE};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        header_layout.addWidget(self.status_filter)
        
        root.addLayout(header_layout)

        # Orders Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ORDER ID", "DATE", "SUPPLIER", "ITEMS", 
            "TOTAL AMOUNT", "EXPECTED DATE", "STATUS", "ACTIONS"
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
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ORDER ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # DATE
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # SUPPLIER
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # ITEMS
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # TOTAL AMOUNT
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # EXPECTED DATE
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # STATUS
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # ACTIONS
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

    def populate_table(self, orders, controller):
        """Populate table with orders data using controller for actions."""
        self.table.setRowCount(len(orders))
        
        for r_idx, order in enumerate(orders):
            # Set row height
            self.table.setRowHeight(r_idx, 45)
            
            # Order ID
            id_item = QTableWidgetItem(str(order.get('id', '')))
            id_item.setData(Qt.ItemDataRole.UserRole, order.get('id'))
            self.table.setItem(r_idx, 0, id_item)
            
            # Date
            date_item = QTableWidgetItem(str(order.get('created_at', '')))
            self.table.setItem(r_idx, 1, date_item)
            
            # Supplier
            supplier_item = QTableWidgetItem(order.get('supplier_name', '-'))
            self.table.setItem(r_idx, 2, supplier_item)
            
            # Items Count
            items_item = QTableWidgetItem(str(order.get('items_count', 0)))
            self.table.setItem(r_idx, 3, items_item)
            
            # Total Amount
            total = float(order.get('total_amount', 0))
            amount_item = QTableWidgetItem(f"₱{total:,.2f}")
            self.table.setItem(r_idx, 4, amount_item)
            
            # Expected Date
            expected_item = QTableWidgetItem(str(order.get('expected_date', '-')))
            self.table.setItem(r_idx, 5, expected_item)
            
            # Status with colored badge
            status = order.get('status', 'draft')
            status_widget = QFrame()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(5, 0, 5, 0)
            
            status_label = QLabel(status.upper())
            status_label.setStyleSheet(f"""
                color: {STYLE_NAVY};
                font-weight: bold;
                font-size: 11px;
            """)
            
            # Add status icon
            icon_label = QLabel()
            icon_label.setPixmap(create_status_badge_icon(status, 12).pixmap(12, 12))
            
            status_layout.addWidget(icon_label)
            status_layout.addWidget(status_label)
            status_layout.addStretch()
            
            self.table.setCellWidget(r_idx, 6, status_widget)
            
            # Action Button - Status Dropdown
            action_widget = QFrame()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            
            
            status_dropdown = QComboBox()
            status_dropdown.addItems(["Draft", "Pending", "Delivered", "Cancelled"])
            status_dropdown.setCurrentText(status.capitalize())
            status_dropdown.setFixedHeight(32)
            
            
            # Style based on current status
            if status.lower() == 'pending':
                bg_color = "#fbbf24"  # Yellow
                hover_color = "#f59e0b"
            elif status.lower() == 'delivered':
                bg_color = "#10b981"  # Green
                hover_color = "#059669"
            elif status.lower() == 'cancelled':
                bg_color = "#ef4444"  # Red
                hover_color = "#dc2626"
            else:  # draft
                bg_color = "#6b7280"  # Gray
                hover_color = "#4b5563"
            
            status_dropdown.setStyleSheet(f"""
                QComboBox {{
                    background-color: {bg_color};
                    color: black;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QComboBox:hover {{
                    background-color: {hover_color};
                }}
                QComboBox::drop-down {{
                    border: none;
                    padding-right: 5px;
                }}
                QComboBox QAbstractItemView {{
                    background-color: white !important;
                    border: 1px solid {STYLE_BORDER};
                }}
                QComboBox QAbstractItemView::item {{
                    color: #000000 !important;
                    background-color: white;
                    padding: 8px 12px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QComboBox QAbstractItemView::item:selected {{
                    background-color: {STYLE_BG_LIGHT} !important;
                    color: #000000 !important;
                }}
            """)
            status_dropdown.currentTextChanged.connect(
                lambda new_status, o=order: controller.handle_update_status(o.get('id'), new_status)
            )
            
            action_layout.addWidget(status_dropdown)
            
            self.table.setCellWidget(r_idx, 7, action_widget)
