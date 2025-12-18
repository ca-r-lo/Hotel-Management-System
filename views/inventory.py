from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QDialog,
    QLineEdit, QMessageBox, QSpinBox, QMainWindow
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor

# --- Shared Style Constants ---
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


def create_edit_icon(size=16):
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


def create_more_icon(size=16):
    """Create a three-dot more icon."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen_color = QColor("#FFFFFF")
    painter.setBrush(pen_color)
    painter.setPen(pen_color)
    
    # Draw three dots vertically
    dot_size = size // 5
    center_x = size // 2
    
    painter.drawEllipse(center_x - dot_size // 2, size // 4 - dot_size // 2, dot_size, dot_size)
    painter.drawEllipse(center_x - dot_size // 2, size // 2 - dot_size // 2, dot_size, dot_size)
    painter.drawEllipse(center_x - dot_size // 2, 3 * size // 4 - dot_size // 2, dot_size, dot_size)
    
    painter.end()
    return QIcon(pixmap)


class AddStockDialog(QDialog):
    """Dialog for adding new inventory items."""
    
    def __init__(self, parent=None, item_data=None):
        super().__init__(parent)
        self.item_data = item_data
        self.is_edit_mode = item_data is not None
        self.setWindowTitle("EDIT ITEM" if self.is_edit_mode else "ADD STOCKS")
        self.setFixedSize(550, 550)
        self.init_ui()
        
        if self.is_edit_mode:
            self.populate_fields()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Set dialog background
        self.setStyleSheet("QDialog { background-color: white; }")

        # Title
        title = QLabel("EDIT ITEM" if self.is_edit_mode else "ADD STOCKS")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {STYLE_NAVY}; padding-bottom: 10px; border-bottom: 2px solid {STYLE_BORDER};")
        layout.addWidget(title)

        # Form fields
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Item Name
        name_label = QLabel("ITEM NAME:")
        name_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(name_label)
        
        self.name_edit = QLineEdit()
        self.name_edit.setFixedHeight(35)
        self.name_edit.setPlaceholderText("Enter item name")
        self.name_edit.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QLineEdit:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.name_edit)

        # Category
        category_label = QLabel("CATEGORY:")
        category_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(category_label)
        
        self.category_cb = QComboBox()
        self.category_cb.addItems(["General", "Room Supplies", "Kitchen", "Cleaning", "Toiletries", "Other"])
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
        form_layout.addWidget(self.category_cb)

        # Unit
        unit_label = QLabel("UNIT:")
        unit_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(unit_label)
        
        self.unit_edit = QLineEdit()
        self.unit_edit.setFixedHeight(35)
        self.unit_edit.setPlaceholderText("e.g., pcs, boxes, kg")
        self.unit_edit.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QLineEdit:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.unit_edit)

        # Unit Cost
        unit_cost_label = QLabel("UNIT COST (₱):")
        unit_cost_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(unit_cost_label)
        
        self.unit_cost_spin = QSpinBox()
        self.unit_cost_spin.setRange(0, 999999)
        self.unit_cost_spin.setFixedHeight(35)
        self.unit_cost_spin.setPrefix("₱ ")
        self.unit_cost_spin.setStyleSheet(f"""
            QSpinBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QSpinBox:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.unit_cost_spin)

        # Stock Quantity
        stock_label = QLabel("STOCK QUANTITY:")
        stock_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(stock_label)
        
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 999999)
        self.stock_spin.setFixedHeight(35)
        self.stock_spin.setStyleSheet(f"""
            QSpinBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QSpinBox:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.stock_spin)

        # Minimum Stock Level
        min_label = QLabel("MINIMUM STOCK LEVEL:")
        min_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(min_label)
        
        self.min_spin = QSpinBox()
        self.min_spin.setRange(0, 999999)
        self.min_spin.setFixedHeight(35)
        self.min_spin.setStyleSheet(f"""
            QSpinBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QSpinBox:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        form_layout.addWidget(self.min_spin)

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
        
        self.save_btn = QPushButton("SAVE" if self.is_edit_mode else "ADD")
        self.save_btn.setFixedSize(100, 40)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY};
                color: white;
                border: none;
                font-weight: bold;
                border-radius: 4px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BLUE}; }}
        """)
        
        button_row.addWidget(self.cancel_btn)
        button_row.addWidget(self.save_btn)
        layout.addLayout(button_row)

    def populate_fields(self):
        """Populate fields when editing."""
        if self.item_data:
            self.name_edit.setText(self.item_data.get('name', ''))
            
            category = self.item_data.get('category', 'General')
            index = self.category_cb.findText(category)
            if index >= 0:
                self.category_cb.setCurrentIndex(index)
            
            self.unit_edit.setText(self.item_data.get('unit', ''))
            self.unit_cost_spin.setValue(int(self.item_data.get('unit_cost', 0)))
            self.stock_spin.setValue(int(self.item_data.get('stock_qty', 0)))
            self.min_spin.setValue(int(self.item_data.get('min_stock', 0)))

    def get_data(self):
        """Return the form data."""
        return {
            'name': self.name_edit.text(),
            'category': self.category_cb.currentText(),
            'unit': self.unit_edit.text(),
            'unit_cost': self.unit_cost_spin.value(),
            'stock_qty': self.stock_spin.value(),
            'min_stock': self.min_spin.value()
        }


class InventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_role = None
        self.current_department = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # Header with Title
        # header_layout = QHBoxLayout()
        
        # title = QLabel("INVENTORY")
        # title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        # title.setStyleSheet(f"color: {STYLE_NAVY};")
        # header_layout.addWidget(title)
        # header_layout.addStretch()
        
        # self.layout.addLayout(header_layout)

        # Action Buttons Row (will be hidden for Department role)
        self.actions_layout = QHBoxLayout()
        self.actions_layout.setSpacing(12)
        
        self.btn_add_stocks = QPushButton("ADD STOCKS")
        self.btn_distribute_stocks = QPushButton("DISTRIBUTE STOCKS")
        self.btn_stock_request = QPushButton("STOCK REQUEST")
        self.btn_history = QPushButton("HISTORY")

        self.actions = [self.btn_add_stocks, self.btn_distribute_stocks, self.btn_stock_request, self.btn_history]
        for btn in self.actions:
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
                }}
                QPushButton:hover {{ 
                    background-color: {STYLE_BG_LIGHT}; 
                    border-color: {STYLE_BLUE}; 
                    color: {STYLE_BLUE}; 
                }}
            """)
            self.actions_layout.addWidget(btn)
        
        # Create a container widget for actions so we can hide it
        self.actions_container = QWidget()
        self.actions_container.setLayout(self.actions_layout)
        self.layout.addWidget(self.actions_container)

        # Filters Row
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(12)
        
        # Department Filter (hidden for Department role)
        self.dept_label = QLabel("DEPARTMENT:")
        self.dept_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 11px;")
        filters_layout.addWidget(self.dept_label)
        
        self.dept_filter = QComboBox()
        self.dept_filter.addItems(["All Departments", "Housekeeping", "Kitchen", "Front Desk", "Maintenance"])
        self.dept_filter.setFixedWidth(180)
        self.dept_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: white;
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                color: {STYLE_NAVY};
                font-size: 11px;
                font-weight: bold;
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        filters_layout.addWidget(self.dept_filter)
        
        filters_layout.addSpacing(20)
        
        # Category Filter (shown for Department role, hidden for others)
        self.cat_label = QLabel("CATEGORY:")
        self.cat_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 11px;")
        filters_layout.addWidget(self.cat_label)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All Categories", "General", "Room Supplies", "Kitchen", "Housekeeping", "Cleaning", "Toiletries"])
        self.category_filter.setFixedWidth(180)
        self.category_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: white;
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                color: {STYLE_NAVY};
                font-size: 11px;
                font-weight: bold;
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        filters_layout.addWidget(self.category_filter)
        
        filters_layout.addStretch()
        self.layout.addLayout(filters_layout)

        # Inventory Table
        table_container = QFrame()
        table_container.setStyleSheet(f"background-color: white; border: 1px solid {STYLE_BORDER}; border-radius: 2px;")
        container_layout = QVBoxLayout(table_container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ITEM NAME", "UNIT", "STOCK LEVEL", "STATUS", "ACTIONS"
        ])
        
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: none;
                font-size: 13px;
                color: {STYLE_NAVY};
                alternate-background-color: #fcfcfd;
                gridline-color: #f3f4f6;
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
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # ITEM NAME
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # UNIT
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # STOCK LEVEL
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # STATUS
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # ACTIONS
        self.table.verticalHeader().setVisible(False)
        
        container_layout.addWidget(self.table)
        self.layout.addWidget(table_container)

    def update_ui_for_role(self, role, department=None):
        """Update UI based on user role."""
        self.current_role = role
        self.current_department = department
        
        if role == "Department":
            # Hide action buttons for Department role
            self.actions_container.setVisible(False)
            
            # Hide department filter, show only category
            self.dept_label.setVisible(False)
            self.dept_filter.setVisible(False)
            
            # Set category filter to department's category if provided
            if department:
                index = self.category_filter.findText(department)
                if index >= 0:
                    self.category_filter.setCurrentIndex(index)
                # Disable the dropdown so department users can only see their department
                self.category_filter.setEnabled(False)
        else:
            # Show all controls for other roles (Purchase Admin, Owner)
            self.actions_container.setVisible(True)
            self.dept_label.setVisible(True)
            self.dept_filter.setVisible(True)
            self.category_filter.setEnabled(True)


class InventoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory - Department")
        self.init_ui()

    def init_ui(self):
        # Main layout setup
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        # Category dropdown for department-specific stocks
        self.category_label = QLabel("CATEGORY:")
        self.category_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Housekeeping", "Maintenance", "Kitchen"])

        # Table for inventory items
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(4)
        self.inventory_table.setHorizontalHeaderLabels(["Item Name", "Unit", "Stock Level", "Status"])

        # Add widgets to layout
        self.main_layout.addWidget(self.category_label)
        self.main_layout.addWidget(self.category_dropdown)
        self.main_layout.addWidget(self.inventory_table)

        # Remove top row buttons (not included in this layout)

    def load_department_inventory(self, department):
        # Logic to load inventory for the selected department
        pass
