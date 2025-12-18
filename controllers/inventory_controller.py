from PyQt6.QtWidgets import QMessageBox, QPushButton, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from views.inventory import AddStockDialog, create_edit_icon, create_more_icon
from models.purchase import ItemModel

STYLE_BLUE = "#0056b3"


class InventoryController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.current_category_filter = "All Categories"
        
        # Connect action buttons
        self.view.btn_add_stocks.clicked.connect(self.handle_add_stock)
        
        # Connect filters
        self.view.category_filter.currentTextChanged.connect(self.handle_category_filter_change)
        
        # Load initial data
        self.refresh_inventory()
    
    def handle_category_filter_change(self, filter_value):
        """Handle category filter change."""
        self.current_category_filter = filter_value
        self.refresh_inventory()
    
    def refresh_inventory(self):
        """Reload inventory items from database and populate table."""
        try:
            # Get all items
            all_items = ItemModel.list_items()
            
            # Filter by category if not "All Categories"
            if self.current_category_filter != "All Categories":
                filtered_items = [
                    item for item in all_items 
                    if item.get('category', '').lower() == self.current_category_filter.lower()
                ]
            else:
                filtered_items = all_items
            
            self.populate_table(filtered_items)
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load inventory:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def populate_table(self, items):
        """Populate inventory table with items."""
        self.view.table.setRowCount(len(items))
        
        for r_idx, item in enumerate(items):
            # Set row height
            self.view.table.setRowHeight(r_idx, 45)
            
            # Item Name
            from PyQt6.QtWidgets import QTableWidgetItem
            name_item = QTableWidgetItem(item.get('name', ''))
            name_item.setData(Qt.ItemDataRole.UserRole, item.get('id'))
            self.view.table.setItem(r_idx, 0, name_item)
            
            # Unit
            unit_item = QTableWidgetItem(item.get('unit', '-'))
            self.view.table.setItem(r_idx, 1, unit_item)
            
            # Stock Level
            stock_qty = int(item.get('stock_qty', 0))
            stock_item = QTableWidgetItem(str(stock_qty))
            self.view.table.setItem(r_idx, 2, stock_item)
            
            # Status (based on stock level vs minimum stock)
            min_stock = int(item.get('min_stock', 0))
            if stock_qty == 0:
                status_text = "OUT OF STOCK"
                status_color = QColor("#ef4444")  # Red
            elif stock_qty <= min_stock:
                status_text = "LOW STOCK"
                status_color = QColor("#f59e0b")  # Orange
            else:
                status_text = "IN STOCK"
                status_color = QColor("#10b981")  # Green
            
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(QBrush(status_color))
            status_item.setData(Qt.ItemDataRole.UserRole, {'stock_qty': stock_qty, 'min_stock': min_stock})
            self.view.table.setItem(r_idx, 3, status_item)
            
            # Action Buttons
            action_widget = QFrame()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            action_layout.setSpacing(6)
            
            # Edit button with icon
            edit_btn = QPushButton()
            edit_btn.setIcon(create_edit_icon(16))
            edit_btn.setFixedSize(32, 32)
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.setToolTip("Edit Item")
            edit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {STYLE_BLUE};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px;
                }}
                QPushButton:hover {{ 
                    background-color: #003d82;
                    border: 2px solid #ffffff;
                }}
            """)
            edit_btn.clicked.connect(lambda checked, i=item: self.handle_edit_item(i))
            
            # More button with icon
            more_btn = QPushButton()
            more_btn.setIcon(create_more_icon(16))
            more_btn.setFixedSize(32, 32)
            more_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            more_btn.setToolTip("More Options")
            more_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #6b7280;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px;
                }}
                QPushButton:hover {{ 
                    background-color: #4b5563;
                    border: 2px solid #ffffff;
                }}
            """)
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(more_btn)
            action_layout.addStretch()
            
            self.view.table.setCellWidget(r_idx, 4, action_widget)
    
    def handle_add_stock(self):
        """Handle adding a new inventory item."""
        dlg = AddStockDialog(self.view)
        dlg.save_btn.clicked.connect(lambda: self.save_item(dlg))
        dlg.exec()
    
    def handle_edit_item(self, item):
        """Handle editing an existing inventory item."""
        dlg = AddStockDialog(self.view, item)
        dlg.save_btn.clicked.connect(lambda: self.update_item(item.get('id'), dlg))
        dlg.exec()
    
    def save_item(self, dialog):
        """Save a new inventory item to database."""
        data = dialog.get_data()
        
        # Validate
        if not data['name']:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter an item name.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        if not data['unit']:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter a unit.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        try:
            result = ItemModel.add_item(
                name=data['name'],
                category=data['category'],
                unit=data['unit'],
                stock_qty=data['stock_qty'],
                min_stock=data['min_stock']
            )
            
            if result:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Item added successfully!")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                dialog.accept()
                self.refresh_inventory()
            else:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Failed to add item.")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
        except Exception as e:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to add item:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def update_item(self, item_id, dialog):
        """Update an existing inventory item in database."""
        data = dialog.get_data()
        
        # Validate
        if not data['name']:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter an item name.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        if not data['unit']:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter a unit.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        try:
            result = ItemModel.update_item(
                item_id=item_id,
                name=data['name'],
                category=data['category'],
                unit=data['unit'],
                stock_qty=data['stock_qty'],
                min_stock=data['min_stock']
            )
            
            if result:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Item updated successfully!")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                dialog.accept()
                self.refresh_inventory()
            else:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Failed to update item.")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
        except Exception as e:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to update item:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
