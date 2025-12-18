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
        self.view.btn_distribute_stocks.clicked.connect(self.handle_stock_requests)
        self.view.btn_stock_request.clicked.connect(self.handle_stock_requests)
        self.view.btn_history.clicked.connect(self.handle_history)
        
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
            
            # Action Buttons (only show for non-Department roles)
            if self.view.current_role != "Department":
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
                more_btn.setToolTip("Delete Item")
                more_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #ef4444;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 4px;
                    }}
                    QPushButton:hover {{ 
                        background-color: #dc2626;
                        border: 2px solid #ffffff;
                    }}
                """)
                more_btn.clicked.connect(lambda checked, i=item: self.handle_delete_item(i))
            
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(more_btn)
                action_layout.addStretch()
                
                self.view.table.setCellWidget(r_idx, 4, action_widget)
            else:
                # For Department role, leave the actions column empty
                empty_widget = QFrame()
                self.view.table.setCellWidget(r_idx, 4, empty_widget)
    
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
                unit_cost=data['unit_cost'],
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
                unit_cost=data['unit_cost'],
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
    
    def handle_delete_item(self, item):
        """Handle deleting an inventory item."""
        # Confirm deletion
        msg = QMessageBox(self.view)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete '{item.get('name', 'this item')}'?")
        msg.setInformativeText("This action cannot be undone.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("QLabel { color: #000000; }")
        
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = ItemModel.delete_item(item.get('id'))
                
                if result:
                    success_msg = QMessageBox(self.view)
                    success_msg.setIcon(QMessageBox.Icon.Information)
                    success_msg.setWindowTitle("Success")
                    success_msg.setText("Item deleted successfully!")
                    success_msg.setStyleSheet("QLabel { color: #000000; }")
                    success_msg.exec()
                    self.refresh_inventory()
                else:
                    error_msg = QMessageBox(self.view)
                    error_msg.setIcon(QMessageBox.Icon.Warning)
                    error_msg.setWindowTitle("Error")
                    error_msg.setText("Failed to delete item.")
                    error_msg.setStyleSheet("QLabel { color: #000000; }")
                    error_msg.exec()
            except Exception as e:
                error_msg = QMessageBox(self.view)
                error_msg.setIcon(QMessageBox.Icon.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText(f"Failed to delete item:\n{e}")
                error_msg.setStyleSheet("QLabel { color: #000000; }")
                error_msg.exec()
    
    def handle_stock_requests(self):
        """Handle showing stock requests dialog."""
        from views.inventory import StockRequestsDialog
        from models.request import RequestModel
        
        # Get all pending requests
        try:
            requests = RequestModel.get_all_requests(include_archived=False)
            # Filter only pending requests
            pending_requests = [r for r in requests if r['status'] == 'Pending']
            
            dialog = StockRequestsDialog(self.view, controller=self)
            dialog.load_requests(pending_requests)
            dialog.refresh_btn.clicked.connect(lambda: self.refresh_requests_dialog(dialog))
            dialog.exec()
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load requests:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def refresh_requests_dialog(self, dialog):
        """Refresh the requests in the dialog."""
        from models.request import RequestModel
        
        try:
            requests = RequestModel.get_all_requests(include_archived=False)
            pending_requests = [r for r in requests if r['status'] == 'Pending']
            dialog.load_requests(pending_requests)
        except Exception as e:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to refresh requests:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def handle_approve_from_dialog(self, request, dialog):
        """Handle approving a request from the stock requests dialog."""
        from views.requests import DistributeStockDialog
        from models.request import RequestModel
        
        # Show distribute dialog
        distribute_dialog = DistributeStockDialog(dialog, request=request)
        distribute_dialog.approve_btn.clicked.connect(
            lambda: self.process_approval_from_dialog(distribute_dialog, request, dialog)
        )
        distribute_dialog.exec()
    
    def process_approval_from_dialog(self, distribute_dialog, request, parent_dialog):
        """Process the approval and deduct stock."""
        data = distribute_dialog.get_data()
        distributed_qty = data['quantity']
        notes = data['notes']
        
        try:
            # Check if item exists in inventory
            items = ItemModel.list_items()
            matching_item = None
            for item in items:
                if item['name'].lower() == request['item_name'].lower():
                    matching_item = item
                    break
            
            if not matching_item:
                msg = QMessageBox(distribute_dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Item Not Found")
                msg.setText(f"Item '{request['item_name']}' not found in inventory. Cannot distribute stock.")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                return
            
            # Check if enough stock
            current_stock = matching_item.get('stock_qty', 0)
            if current_stock < distributed_qty:
                msg = QMessageBox(distribute_dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Insufficient Stock")
                msg.setText(f"Insufficient stock. Available: {current_stock} {matching_item['unit']}, Requested: {distributed_qty} {request['unit']}")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                return
            
            # Deduct stock
            from models.request import RequestModel
            ItemModel.adjust_stock(matching_item['id'], -distributed_qty)
            
            # Update request status
            RequestModel.approve_request(request['id'], distributed_qty, notes)
            
            # Close distribute dialog
            distribute_dialog.accept()
            
            # Show success message
            msg = QMessageBox(parent_dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText(f"Request approved! {distributed_qty} {request['unit']} distributed to {request['department']}.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            
            # Refresh the requests dialog
            self.refresh_requests_dialog(parent_dialog)
            
            # Refresh inventory table
            self.refresh_inventory()
            
        except Exception as e:
            msg = QMessageBox(distribute_dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to approve request:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def handle_reject_from_dialog(self, request_id, dialog):
        """Handle rejecting a request from the stock requests dialog."""
        from PyQt6.QtWidgets import QInputDialog
        from models.request import RequestModel
        
        # Ask for rejection reason
        reason, ok = QInputDialog.getText(
            dialog,
            "Reject Request",
            "Reason for rejection (optional):",
        )
        
        if ok:
            try:
                RequestModel.reject_request(request_id, reason if reason else None)
                
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Request rejected successfully!")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                
                # Refresh the dialog
                self.refresh_requests_dialog(dialog)
                
            except Exception as e:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Error")
                msg.setText(f"Failed to reject request:\n{e}")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
    
    def handle_history(self):
        """Handle showing stock history dialog."""
        from views.inventory import StockHistoryDialog
        from datetime import datetime
        
        # Create sample history data (you can replace this with actual database queries)
        # This is mock data - replace with actual history from your database
        history_data = [
            {
                'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p'),
                'item_name': 'Toilet Paper',
                'type': 'Stock In',
                'quantity': 100,
                'user': 'Purchase Admin',
                'notes': 'New stock delivery'
            },
            {
                'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p'),
                'item_name': 'Soap',
                'type': 'Stock Out',
                'quantity': -20,
                'user': 'Housekeeping Manager',
                'notes': 'Distributed to Housekeeping'
            },
            {
                'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p'),
                'item_name': 'Towels',
                'type': 'Adjustment',
                'quantity': -5,
                'user': 'System',
                'notes': 'Damaged items removed'
            },
        ]
        
        try:
            dialog = StockHistoryDialog(self.view)
            dialog.load_history(history_data)
            dialog.exec()
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load history:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()


