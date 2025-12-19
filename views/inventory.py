from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QDialog,
    QLineEdit, QMessageBox, QSpinBox, QMainWindow, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QBrush

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
    
    def __init__(self, parent=None, item_data=None, is_department_user=False):
        super().__init__(parent)
        self.item_data = item_data
        self.is_edit_mode = item_data is not None
        self.is_department_user = is_department_user
        
        # Department users can only update stock quantity
        if self.is_department_user:
            self.setWindowTitle("UPDATE STOCK")
        else:
            self.setWindowTitle("EDIT ITEM" if self.is_edit_mode else "ADD STOCKS")
        
        # Make dialog resizable with minimum and initial size
        self.setMinimumSize(480, 500)
        self.resize(550, 550)
        # Allow dialog to be resizable
        self.setSizeGripEnabled(True)
        self.init_ui()
        
        if self.is_edit_mode:
            self.populate_fields()

    def init_ui(self):
        # Main layout for the dialog
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Set dialog background
        self.setStyleSheet(f"""
            QDialog {{ background-color: white; }}
            QScrollArea {{
                border: none;
                background-color: white;
            }}
            QScrollArea > QWidget {{
                background-color: white;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: white;
            }}
        """)

        # Create scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Content widget inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        if self.is_department_user:
            title_text = "UPDATE STOCK"
        else:
            title_text = "EDIT ITEM" if self.is_edit_mode else "ADD STOCKS"
        
        title = QLabel(title_text)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {STYLE_NAVY}; padding-bottom: 10px; border-bottom: 2px solid {STYLE_BORDER};")
        title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(title)

        # Form fields
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        if self.is_edit_mode:
            # Edit mode: Show existing item name (read-only) and allow editing other fields
            name_label = QLabel("ITEM NAME:")
            name_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
            form_layout.addWidget(name_label)
            
            self.name_edit = QLineEdit()
            self.name_edit.setMinimumHeight(35)
            self.name_edit.setReadOnly(True)
            self.name_edit.setStyleSheet(f"""
                QLineEdit {{
                    border: 2px solid {STYLE_BORDER};
                    border-radius: 4px;
                    padding: 5px 10px;
                    background-color: #f9fafb;
                    color: #6b7280;
                }}
            """)
            self.name_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            form_layout.addWidget(self.name_edit)
        else:
            # Add mode: Select from delivered purchase order items
            item_label = QLabel("SELECT ITEM FROM DELIVERED ORDERS:")
            item_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
            form_layout.addWidget(item_label)
            
            self.item_selector = QComboBox()
            self.item_selector.setMinimumHeight(35)
            self.item_selector.setStyleSheet(f"""
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
            self.item_selector.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            # Will be populated by controller with delivered items
            self.item_selector.currentIndexChanged.connect(self.on_item_selected)
            form_layout.addWidget(self.item_selector)

        # Category (read-only, auto-filled)
        category_label = QLabel("DEPARTMENT:")
        category_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(category_label)
        
        self.category_display = QLineEdit()
        self.category_display.setMinimumHeight(35)
        self.category_display.setReadOnly(True)
        self.category_display.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: #f9fafb;
                color: #6b7280;
            }}
        """)
        self.category_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form_layout.addWidget(self.category_display)

        # Hidden category combo (for edit mode backward compatibility)
        self.category_cb = QComboBox()
        self.category_cb.addItems(["Housekeeping", "Kitchen", "Front Desk", "Maintenance", "General"])
        self.category_cb.setVisible(self.is_edit_mode and not self.is_department_user)
        if self.is_edit_mode and not self.is_department_user:
            self.category_cb.setMinimumHeight(35)
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
            self.category_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            # Replace the read-only display with editable combo in edit mode (but not for department users)
            self.category_display.setVisible(False)
            form_layout.addWidget(self.category_cb)

        # Unit (read-only in add mode or for department users, editable in edit mode for admins)
        unit_label = QLabel("UNIT:")
        unit_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(unit_label)
        
        self.unit_edit = QLineEdit()
        self.unit_edit.setMinimumHeight(35)
        self.unit_edit.setPlaceholderText("e.g., pcs, boxes, kg")
        if not self.is_edit_mode or self.is_department_user:
            self.unit_edit.setReadOnly(True)
            self.unit_edit.setStyleSheet(f"""
                QLineEdit {{
                    border: 2px solid {STYLE_BORDER};
                    border-radius: 4px;
                    padding: 5px 10px;
                    background-color: #f9fafb;
                    color: #6b7280;
                }}
            """)
        else:
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
        self.unit_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form_layout.addWidget(self.unit_edit)

        # Unit Cost (read-only in add mode or for department users)
        unit_cost_label = QLabel("UNIT COST (₱):")
        unit_cost_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(unit_cost_label)
        
        self.unit_cost_spin = QSpinBox()
        self.unit_cost_spin.setRange(0, 999999)
        self.unit_cost_spin.setMinimumHeight(35)
        self.unit_cost_spin.setPrefix("₱ ")
        if not self.is_edit_mode or self.is_department_user:
            self.unit_cost_spin.setReadOnly(True)
            self.unit_cost_spin.setStyleSheet(f"""
                QSpinBox {{
                    border: 2px solid {STYLE_BORDER};
                    border-radius: 4px;
                    padding: 5px 10px;
                    background-color: #f9fafb;
                    color: #6b7280;
                }}
            """)
        else:
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
        self.unit_cost_spin.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form_layout.addWidget(self.unit_cost_spin)

        if not self.is_edit_mode:
            # Add "Available to Add" info label in add mode
            available_label = QLabel("AVAILABLE TO ADD:")
            available_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
            form_layout.addWidget(available_label)
            
            self.available_info = QLabel("Select an item to see available quantity")
            self.available_info.setMinimumHeight(35)
            self.available_info.setStyleSheet(f"""
                QLabel {{
                    border: 2px solid {STYLE_BORDER};
                    border-radius: 4px;
                    padding: 5px 10px;
                    background-color: #fef3c7;
                    color: #92400e;
                    font-weight: bold;
                }}
            """)
            form_layout.addWidget(self.available_info)

        # Stock Quantity
        stock_label = QLabel("STOCK QUANTITY:")
        stock_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(stock_label)
        
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 999999)
        self.stock_spin.setMinimumHeight(35)
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
        self.stock_spin.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form_layout.addWidget(self.stock_spin)

        # Minimum Stock Level (read-only for department users)
        min_label = QLabel("MINIMUM STOCK LEVEL:")
        min_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(min_label)
        
        self.min_spin = QSpinBox()
        self.min_spin.setRange(0, 999999)
        self.min_spin.setMinimumHeight(35)
        if self.is_department_user:
            self.min_spin.setReadOnly(True)
            self.min_spin.setStyleSheet(f"""
                QSpinBox {{
                    border: 2px solid {STYLE_BORDER};
                    border-radius: 4px;
                    padding: 5px 10px;
                    background-color: #f9fafb;
                    color: #6b7280;
                }}
            """)
        else:
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
        self.min_spin.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form_layout.addWidget(self.min_spin)

        layout.addLayout(form_layout)
        
        # Add stretch to push content to top when scrolling not needed
        layout.addStretch()

        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)

        # Button container (fixed at bottom, not in scroll area)
        button_container = QWidget()
        button_container.setStyleSheet("background-color: white; border-top: 1px solid #e5e7eb;")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(30, 15, 30, 15)
        button_layout.addStretch()
        
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
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        main_layout.addWidget(button_container)

    def on_item_selected(self, index):
        """Handle item selection from delivered orders."""
        if index < 0 or not hasattr(self, 'item_selector'):
            return
        
        # Get the selected item data from the combo box
        item_data = self.item_selector.itemData(index)
        if item_data:
            # Auto-fill the fields with selected item data
            self.category_display.setText(item_data.get('category', 'General'))
            self.unit_edit.setText(item_data.get('unit', ''))
            self.unit_cost_spin.setValue(int(item_data.get('unit_price', 0)))
            
            # Update available quantity info and set max for stock spinbox
            qty_available = item_data.get('qty_available', item_data.get('qty', 0))
            ordered_qty = item_data.get('ordered_qty', item_data.get('qty', 0))
            
            if hasattr(self, 'available_info'):
                self.available_info.setText(f"Ordered: {ordered_qty} | Available to Add: {qty_available}")
            
            # Set the maximum for stock spinbox to available quantity
            self.stock_spin.setMaximum(qty_available)
            self.stock_spin.setValue(min(qty_available, self.stock_spin.value()))
            
            # Pre-fill minimum stock if item already exists in inventory
            item_id = item_data.get('item_id')
            if item_id:
                try:
                    from models.purchase import ItemModel
                    existing_item = ItemModel.get_item_by_id(item_id)
                    if existing_item:
                        self.min_spin.setValue(int(existing_item.get('min_stock', 10)))
                    else:
                        self.min_spin.setValue(10)  # Default value
                except:
                    self.min_spin.setValue(10)  # Default value if error
            else:
                self.min_spin.setValue(10)  # Default value for new items

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
        if self.is_edit_mode:
            return {
                'name': self.name_edit.text(),
                'category': self.category_cb.currentText(),
                'unit': self.unit_edit.text(),
                'unit_cost': self.unit_cost_spin.value(),
                'stock_qty': self.stock_spin.value(),
                'min_stock': self.min_spin.value()
            }
        else:
            # Add mode: return selected item info
            selected_index = self.item_selector.currentIndex()
            item_data = self.item_selector.itemData(selected_index) if selected_index >= 0 else {}
            
            return {
                'purchase_item_id': item_data.get('purchase_item_id') if item_data else None,
                'item_id': item_data.get('item_id') if item_data else None,
                'name': self.item_selector.currentText().split(' - ')[0] if self.item_selector.currentText() else '',
                'category': self.category_display.text(),
                'unit': self.unit_edit.text(),
                'unit_cost': self.unit_cost_spin.value(),
                'stock_qty': self.stock_spin.value(),
                'min_stock': self.min_spin.value()
            }


class StockRequestsDialog(QDialog):
    """Dialog for viewing and managing stock requests."""
    
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Stock Requests")
        self.setFixedSize(950, 650)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.setStyleSheet(f"""
            QDialog {{ 
                background-color: {STYLE_BG_LIGHT}; 
            }}
        """)
        
        # Header with gradient background
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_NAVY};
                border: none;
            }}
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        title = QLabel("Pending Stock Requests")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white; border: none;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("↻ Refresh")
        self.refresh_btn.setFixedSize(100, 36)
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
            }}
            QPushButton:hover {{ 
                background-color: rgba(255, 255, 255, 0.25);
                border-color: rgba(255, 255, 255, 0.5);
            }}
        """)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(header_frame)
        
        # Content area with padding
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)
        
        # Scroll area for requests
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: #f3f4f6;
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: #d1d5db;
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #9ca3af;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """)
        
        # Container for request cards
        self.requests_container = QWidget()
        self.requests_layout = QVBoxLayout(self.requests_container)
        self.requests_layout.setSpacing(12)
        self.requests_layout.setContentsMargins(0, 0, 0, 0)
        self.requests_layout.addStretch()
        
        scroll.setWidget(self.requests_container)
        content_layout.addWidget(scroll)
        
        layout.addWidget(content_widget)
        
        # Footer with close button
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(24, 0, 24, 24)
        footer_layout.addStretch()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedSize(100, 40)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                color: #6b7280;
                font-weight: 600;
                font-size: 13px;
                border-radius: 6px;
            }}
            QPushButton:hover {{ 
                background-color: {STYLE_BG_LIGHT};
                border-color: {STYLE_NAVY};
                color: {STYLE_NAVY};
            }}
        """)
        self.close_btn.clicked.connect(self.accept)
        footer_layout.addWidget(self.close_btn)
        
        layout.addLayout(footer_layout)
    
    def load_requests(self, requests):
        """Load and display requests."""
        # Clear existing widgets
        while self.requests_layout.count() > 1:  # Keep the stretch
            item = self.requests_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not requests:
            # Show empty state with icon
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.setSpacing(12)
            
            empty_icon = QLabel("📭")
            empty_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_icon.setStyleSheet("font-size: 48px; border: none;")
            empty_layout.addWidget(empty_icon)
            
            empty_label = QLabel("No Pending Requests")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("color: #9ca3af; font-size: 16px; font-weight: 600; border: none;")
            empty_layout.addWidget(empty_label)
            
            empty_sublabel = QLabel("All requests have been processed")
            empty_sublabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_sublabel.setStyleSheet("color: #d1d5db; font-size: 13px; border: none;")
            empty_layout.addWidget(empty_sublabel)
            
            self.requests_layout.insertWidget(0, empty_widget)
        else:
            # Add request cards
            for request in requests:
                card = self.create_request_card(request)
                self.requests_layout.insertWidget(self.requests_layout.count() - 1, card)
    
    def create_request_card(self, request):
        """Create a card widget for a request."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                border-radius: 8px;
            }}
            QFrame:hover {{
                border-color: {STYLE_BLUE};
            }}
        """)
        card.setMinimumHeight(110)
        card.setMaximumHeight(110)
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(20)
        
        # Left side - Item info with colored indicator
        left_layout = QHBoxLayout()
        left_layout.setSpacing(16)
        
        # Colored indicator bar
        indicator = QFrame()
        indicator.setFixedSize(4, 78)
        indicator.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_BLUE};
                border-radius: 2px;
                border: none;
            }}
        """)
        left_layout.addWidget(indicator)
        
        # Request info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        # Item name and quantity - larger and bolder
        item_label = QLabel(f"{request['item_name']}")
        item_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        item_label.setStyleSheet(f"color: {STYLE_NAVY}; border: none;")
        info_layout.addWidget(item_label)
        
        # Quantity with badge style
        qty_label = QLabel(f"Quantity: {request['quantity']} {request['unit']}")
        qty_label.setStyleSheet(f"""
            color: {STYLE_BLUE}; 
            font-size: 13px; 
            font-weight: 600;
            border: none;
        """)
        info_layout.addWidget(qty_label)
        
        # Department and requester - cleaner icons
        details_label = QLabel(f"🏢 {request['department']}  •  👤 {request['requested_by']}")
        details_label.setStyleSheet("color: #6b7280; font-size: 12px; border: none;")
        info_layout.addWidget(details_label)
        
        # Date - smaller and subtle
        created_at = request['created_at'].strftime("%b %d, %Y at %I:%M %p") if hasattr(request['created_at'], 'strftime') else str(request['created_at'])
        date_label = QLabel(f"� {created_at}")
        date_label.setStyleSheet("color: #d1d5db; font-size: 11px; border: none;")
        info_layout.addWidget(date_label)
        
        left_layout.addLayout(info_layout)
        card_layout.addLayout(left_layout)
        
        # Right side - Reason (if provided) and Actions
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        
        # Reason in a subtle box
        if request.get('reason'):
            reason_frame = QFrame()
            reason_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {STYLE_BG_LIGHT};
                    border: 1px solid {STYLE_BORDER};
                    border-radius: 6px;
                    padding: 8px;
                }}
            """)
            reason_layout = QVBoxLayout(reason_frame)
            reason_layout.setContentsMargins(8, 8, 8, 8)
            reason_layout.setSpacing(4)
            
            reason_title = QLabel("Reason:")
            reason_title.setStyleSheet("color: #9ca3af; font-size: 10px; font-weight: 600; border: none;")
            reason_layout.addWidget(reason_title)
            
            reason_text = QLabel(request['reason'])
            reason_text.setStyleSheet("color: #6b7280; font-size: 11px; border: none;")
            reason_text.setWordWrap(True)
            reason_text.setMaximumWidth(250)
            reason_layout.addWidget(reason_text)
            
            right_layout.addWidget(reason_frame)
        
        right_layout.addStretch()
        
        # Action buttons container
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        # Approve button - modern green
        approve_btn = QPushButton("✓ Approve")
        approve_btn.setFixedSize(95, 38)
        approve_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        approve_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{ 
                background-color: #059669;
            }}
            QPushButton:pressed {{
                background-color: #047857;
            }}
        """)
        approve_btn.clicked.connect(lambda: self.controller.handle_approve_from_dialog(request, self))
        actions_layout.addWidget(approve_btn)
        
        # Reject button - modern red
        reject_btn = QPushButton("✗ Reject")
        reject_btn.setFixedSize(85, 38)
        reject_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reject_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{ 
                background-color: #dc2626;
            }}
            QPushButton:pressed {{
                background-color: #b91c1c;
            }}
        """)
        reject_btn.clicked.connect(lambda: self.controller.handle_reject_from_dialog(request['id'], self))
        actions_layout.addWidget(reject_btn)
        
        right_layout.addLayout(actions_layout)
        card_layout.addLayout(right_layout)
        
        return card


class StockHistoryDialog(QDialog):
    """Dialog for viewing stock movement history."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stock History")
        self.setFixedSize(1000, 650)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.setStyleSheet(f"""
            QDialog {{ 
                background-color: {STYLE_BG_LIGHT}; 
            }}
        """)
        
        # Header
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_NAVY};
                border: none;
            }}
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        title = QLabel("Stock Movement History")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white; border: none;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Movements", "Stock In", "Stock Out", "Adjustments"])
        self.filter_combo.setFixedSize(150, 36)
        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 600;
                font-size: 12px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: #111827;
                selection-background-color: {STYLE_BLUE};
                border: 1px solid {STYLE_BORDER};
            }}
        """)
        header_layout.addWidget(self.filter_combo)
        
        layout.addWidget(header_frame)
        
        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)
        
        # Table for history
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["Date & Time", "Item", "Type", "Quantity", "By User", "Notes"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setColumnWidth(0, 180)
        self.history_table.setColumnWidth(1, 200)
        self.history_table.setColumnWidth(2, 120)
        self.history_table.setColumnWidth(3, 100)
        self.history_table.setColumnWidth(4, 150)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        
        self.history_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                border-radius: 8px;
                gridline-color: {STYLE_BORDER};
                color: #111827;
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                border: none;
                color: #111827;
            }}
            QTableWidget::item:selected {{
                background-color: {STYLE_BLUE};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {STYLE_BG_LIGHT};
                color: {STYLE_NAVY};
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid {STYLE_BORDER};
                font-weight: 700;
                font-size: 12px;
                text-align: left;
            }}
            QTableWidget::item:alternate {{
                background-color: #fafafa;
            }}
        """)
        
        content_layout.addWidget(self.history_table)
        
        layout.addWidget(content_widget)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(24, 0, 24, 24)
        
        # Export button
        export_btn = QPushButton("📥 Export")
        export_btn.setFixedSize(100, 40)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_BLUE};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #003d82;
            }}
        """)
        footer_layout.addWidget(export_btn)
        
        footer_layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(100, 40)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                color: #6b7280;
                font-weight: 600;
                font-size: 13px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {STYLE_BG_LIGHT};
                border-color: {STYLE_NAVY};
                color: {STYLE_NAVY};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
    
    def load_history(self, history_data):
        """Load history data into the table."""
        self.history_table.setRowCount(len(history_data))
        
        for row_idx, record in enumerate(history_data):
            # Set row height for better readability
            self.history_table.setRowHeight(row_idx, 45)
            
            # Date & Time
            date_item = QTableWidgetItem(record.get('timestamp', ''))
            date_item.setForeground(QBrush(QColor("#111827")))
            self.history_table.setItem(row_idx, 0, date_item)
            
            # Item
            item_item = QTableWidgetItem(record.get('item_name', ''))
            item_item.setForeground(QBrush(QColor("#111827")))
            item_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            self.history_table.setItem(row_idx, 1, item_item)
            
            # Type (with color coding and badge style)
            type_text = record.get('type', 'Unknown')
            type_item = QTableWidgetItem(type_text)
            type_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            if type_text == "Stock In":
                type_item.setForeground(QBrush(QColor("#10b981")))
            elif type_text == "Stock Out":
                type_item.setForeground(QBrush(QColor("#ef4444")))
            else:
                type_item.setForeground(QBrush(QColor("#f59e0b")))
            self.history_table.setItem(row_idx, 2, type_item)
            
            # Quantity
            qty_item = QTableWidgetItem(str(record.get('quantity', 0)))
            qty_item.setForeground(QBrush(QColor("#111827")))
            qty_item.setFont(QFont("Arial", 11))
            self.history_table.setItem(row_idx, 3, qty_item)
            
            # By User
            user_item = QTableWidgetItem(record.get('user', 'System'))
            user_item.setForeground(QBrush(QColor("#6b7280")))
            self.history_table.setItem(row_idx, 4, user_item)
            
            # Notes
            notes_item = QTableWidgetItem(record.get('notes', '-'))
            notes_item.setForeground(QBrush(QColor("#6b7280")))
            self.history_table.setItem(row_idx, 5, notes_item)
            # Notes
            notes_item = QTableWidgetItem(record.get('notes', '-'))
            self.history_table.setItem(row_idx, 5, notes_item)


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
