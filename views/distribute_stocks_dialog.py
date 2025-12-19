from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, 
    QFrame, QScrollArea, QWidget, QHeaderView, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QFont

# Shared Style Constants
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"

class DistributeStocksDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Distribute Stocks to Department")
        self.resize(1200, 750)
        self.setSizeGripEnabled(True)
        self.selected_items = []  # Store items to distribute
        self.setStyleSheet("QDialog { background-color: white; }")
        self.init_ui()
    
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)
        
        # Header
        header = QLabel("DISTRIBUTE STOCKS TO DEPARTMENT")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            color: {STYLE_NAVY};
            padding-bottom: 10px;
            border-bottom: 2px solid {STYLE_BORDER};
        """)
        main_layout.addWidget(header)
        
        # Department Selection
        dept_layout = QHBoxLayout()
        dept_layout.setSpacing(15)
        
        dept_label = QLabel("Department:")
        dept_label.setFixedWidth(120)
        dept_label.setStyleSheet(f"font-weight: bold; color: {STYLE_NAVY}; font-size: 14px;")
        
        self.dept_combo = QComboBox()
        self.dept_combo.setFixedHeight(45)
        self.dept_combo.addItems([
            "-- Select Department --",
            "Housekeeping",
            "Kitchen",
            "Front Desk",
            "Maintenance"
        ])
        self.dept_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 10px 15px;
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                background: white;
                font-size: 14px;
                color: {STYLE_NAVY};
            }}
            QComboBox:hover {{
                border-color: {STYLE_BLUE};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 15px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        self.dept_combo.currentTextChanged.connect(self.on_department_changed)
        
        dept_layout.addWidget(dept_label)
        dept_layout.addWidget(self.dept_combo)
        dept_layout.addStretch()
        
        main_layout.addLayout(dept_layout)
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.setSpacing(15)
        
        search_label = QLabel("Search Items:")
        search_label.setFixedWidth(120)
        search_label.setStyleSheet(f"font-weight: bold; color: {STYLE_NAVY}; font-size: 14px;")
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type to search by item name or category...")
        self.search_box.setFixedHeight(45)
        self.search_box.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 15px;
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                font-size: 14px;
                background: white;
                color: {STYLE_NAVY};
            }}
            QLineEdit:focus {{
                border-color: {STYLE_BLUE};
            }}
        """)
        self.search_box.textChanged.connect(self.filter_items)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        
        main_layout.addLayout(search_layout)
        
        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(6)
        self.items_table.setHorizontalHeaderLabels([
            "ITEM NAME", "CATEGORY", "AVAILABLE", "UNIT", "QUANTITY", "ACTION"
        ])
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.items_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.items_table.horizontalHeader().resizeSection(4, 100)
        self.items_table.horizontalHeader().resizeSection(5, 85)
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.verticalHeader().setDefaultSectionSize(50)  # Set row height
        self.items_table.setAlternatingRowColors(True)
        self.items_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                font-size: 13px;
                color: {STYLE_NAVY};
                gridline-color: {STYLE_BORDER};
                alternate-background-color: {STYLE_BG_LIGHT};
            }}
            QHeaderView::section {{
                background-color: {STYLE_NAVY};
                padding: 10px 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
                color: white;
                text-align: center;
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                border-bottom: 1px solid {STYLE_BORDER};
                color: {STYLE_NAVY};
            }}
        """)
        main_layout.addWidget(self.items_table)
        
        # Summary
        self.summary_label = QLabel("Select a department to view available items")
        self.summary_label.setStyleSheet(f"""
            font-size: 13px; 
            color: #6b7280; 
            padding: 12px;
            background-color: {STYLE_BG_LIGHT};
            border-radius: 4px;
            border: 1px solid {STYLE_BORDER};
        """)
        main_layout.addWidget(self.summary_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addStretch()
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setFixedSize(140, 45)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #e5e7eb;
                color: #374151;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {STYLE_BORDER};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        
        self.distribute_btn = QPushButton("DISTRIBUTE")
        self.distribute_btn.setFixedSize(140, 45)
        self.distribute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.distribute_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_BLUE};
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #004494;
            }}
            QPushButton:disabled {{
                background-color: {STYLE_BORDER};
                color: #9ca3af;
            }}
        """)
        self.distribute_btn.setEnabled(False)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.distribute_btn)
        main_layout.addLayout(button_layout)
    
    def on_department_changed(self, department):
        """Load available items when department is selected."""
        if department == "-- Select Department --":
            self.items_table.setRowCount(0)
            self.summary_label.setText("Select a department to view available items")
            self.distribute_btn.setEnabled(False)
            return
        
        self.load_available_items(department)
        self.summary_label.setText(f"Distributing to: {department}")
        self.distribute_btn.setEnabled(True)
    
    def load_available_items(self, department):
        """Load inventory items available for distribution."""
        from models.purchase import ItemModel
        
        try:
            # Get all items from inventory with stock > 0
            items = ItemModel.list_items()
            
            # Filter items by department category AND stock > 0
            filtered_items = [
                item for item in items 
                if item.get('stock_qty', 0) > 0 and item.get('category', '') == department
            ]
            
            self.all_items = filtered_items  # Store for filtering
            self.display_items(filtered_items)
            
        except Exception as e:
            print(f"Error loading items: {e}")
            import traceback
            traceback.print_exc()
    
    def display_items(self, items):
        """Display items in the table."""
        self.items_table.setRowCount(len(items))
        
        for r_idx, item in enumerate(items):
            # Item Name
            name_item = QTableWidgetItem(str(item.get('name', 'Unknown')))
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            name_item.setData(Qt.ItemDataRole.UserRole, item)  # Store full item data
            self.items_table.setItem(r_idx, 0, name_item)
            
            # Category
            category_item = QTableWidgetItem(str(item.get('category', 'General')))
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setItem(r_idx, 1, category_item)
            
            # Current Stock
            stock = item.get('stock_qty', 0)
            stock_item = QTableWidgetItem(str(stock))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Color code based on stock level
            if stock <= item.get('min_stock', 0):
                stock_item.setForeground(QBrush(QColor('#dc2626')))  # Red for low stock
            self.items_table.setItem(r_idx, 2, stock_item)
            
            # Unit
            unit_item = QTableWidgetItem(str(item.get('unit', 'pcs')))
            unit_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setItem(r_idx, 3, unit_item)
            
            # Quantity Spinbox
            qty_spin = QSpinBox()
            qty_spin.setMinimum(0)
            qty_spin.setMaximum(stock)
            qty_spin.setValue(0)
            qty_spin.setFixedHeight(32)
            qty_spin.setStyleSheet(f"""
                QSpinBox {{
                    padding: 4px 8px;
                    border: 1px solid {STYLE_BORDER};
                    border-radius: 4px;
                    background: white;
                    color: {STYLE_NAVY};
                    font-size: 13px;
                }}
                QSpinBox:focus {{
                    border-color: {STYLE_BLUE};
                }}
                QSpinBox::up-button, QSpinBox::down-button {{
                    width: 16px;
                    border: none;
                    background: transparent;
                }}
                QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                    background-color: {STYLE_BG_LIGHT};
                }}
            """)
            
            # Center the spinbox in the cell
            spinbox_widget = QWidget()
            spinbox_layout = QHBoxLayout(spinbox_widget)
            spinbox_layout.addWidget(qty_spin)
            spinbox_layout.setContentsMargins(5, 5, 5, 5)
            spinbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setCellWidget(r_idx, 4, spinbox_widget)
            
            # Add Button
            add_btn = QPushButton("ADD")
            add_btn.setFixedSize(65, 30)
            add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            add_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {STYLE_BLUE};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: #004494;
                }}
            """)
            add_btn.clicked.connect(lambda checked, row=r_idx: self.add_to_distribution(row))
            
            # Center the button in the cell
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.addWidget(add_btn)
            button_layout.setContentsMargins(5, 5, 5, 5)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setCellWidget(r_idx, 5, button_widget)
    
    def filter_items(self, text):
        """Filter items based on search text."""
        if not hasattr(self, 'all_items'):
            return
        
        if not text:
            self.display_items(self.all_items)
            return
        
        filtered = [
            item for item in self.all_items 
            if text.lower() in item.get('name', '').lower() or 
               text.lower() in item.get('category', '').lower()
        ]
        self.display_items(filtered)
    
    def add_to_distribution(self, row):
        """Add item to distribution list."""
        item_data = self.items_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # Get the spinbox from the wrapper widget
        spinbox_widget = self.items_table.cellWidget(row, 4)
        qty_spin = spinbox_widget.findChild(QSpinBox)
        qty = qty_spin.value()
        
        if qty <= 0:
            from PyQt6.QtWidgets import QMessageBox
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Invalid Quantity")
            msg.setText("Please enter a quantity greater than 0.")
            msg.setStyleSheet(f"QLabel {{ color: {STYLE_NAVY}; }}")
            msg.exec()
            return
        
        # Add to selected items
        self.selected_items.append({
            'item_id': item_data.get('id'),
            'item_name': item_data.get('name'),
            'category': item_data.get('category'),
            'unit': item_data.get('unit'),
            'quantity': qty,
            'current_stock': item_data.get('stock_qty')
        })
        
        # Reset quantity and show feedback
        qty_spin.setValue(0)
        
        # Update summary
        total_items = len(self.selected_items)
        self.summary_label.setText(f"Distributing to: {self.dept_combo.currentText()} | Items added: {total_items}")
    
    def get_data(self):
        """Return selected department and items to distribute."""
        return {
            'department': self.dept_combo.currentText(),
            'items': self.selected_items
        }
