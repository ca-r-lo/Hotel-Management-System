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
        self.current_dept_filter = "All Departments"
        
        # Connect action buttons
        self.view.btn_add_stocks.clicked.connect(self.handle_add_stock)
        self.view.btn_distribute_stocks.clicked.connect(self.handle_distribute_stocks)
        self.view.btn_stock_request.clicked.connect(self.handle_stock_requests)
        self.view.btn_history.clicked.connect(self.handle_history)
        
        # Connect filters
        self.view.category_filter.currentTextChanged.connect(self.handle_category_filter_change)
        self.view.dept_filter.currentTextChanged.connect(self.handle_dept_filter_change)
        
        # Load initial data
        self.refresh_inventory()
    
    def handle_category_filter_change(self, filter_value):
        """Handle category filter change."""
        self.current_category_filter = filter_value
        self.refresh_inventory()
    
    def handle_dept_filter_change(self, filter_value):
        """Handle department filter change."""
        self.current_dept_filter = filter_value
        # When department changes, reset category to "All Categories"
        # unless we're filtering by a specific department
        if filter_value != "All Departments":
            # Department filter takes precedence over category filter
            # Show items from this department regardless of category
            self.current_category_filter = "All Categories"
            if self.view.category_filter.currentText() != "All Categories":
                self.view.category_filter.blockSignals(True)
                self.view.category_filter.setCurrentText("All Categories")
                self.view.category_filter.blockSignals(False)
        self.refresh_inventory()
    
    def refresh_inventory(self):
        """Reload inventory items from database and populate table."""
        try:
            # Get all items
            all_items = ItemModel.list_items()
            
            # Apply filters
            filtered_items = all_items
            
            # First apply department filter if set
            if self.current_dept_filter != "All Departments":
                filtered_items = [
                    item for item in filtered_items 
                    if item.get('category', '').lower() == self.current_dept_filter.lower()
                ]
            
            # Then apply category filter if set (and dept filter is "All Departments")
            elif self.current_category_filter != "All Categories":
                filtered_items = [
                    item for item in filtered_items 
                    if item.get('category', '').lower() == self.current_category_filter.lower()
                ]
            
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
            
            # Edit button with icon (shown for all roles)
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
            action_layout.addWidget(edit_btn)
            
            # Delete button (only show for non-Department roles)
            if self.view.current_role != "Department":
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
                action_layout.addWidget(more_btn)
            
            action_layout.addStretch()
            self.view.table.setCellWidget(r_idx, 4, action_widget)
    
    def handle_distribute_stocks(self):
        """Handle distributing stocks to departments."""
        from views.distribute_stocks_dialog import DistributeStocksDialog
        
        dlg = DistributeStocksDialog(self.view)
        dlg.distribute_btn.clicked.connect(lambda: self.process_distribution(dlg))
        dlg.exec()
    
    def process_distribution(self, dialog):
        """Process the stock distribution."""
        data = dialog.get_data()
        department = data.get('department')
        items = data.get('items', [])
        
        if not items:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("No Items Selected")
            msg.setText("Please add at least one item to distribute.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        try:
            from models.purchase import ItemModel
            from models.database import get_conn, _paramstyle
            
            conn = get_conn()
            cur = conn.cursor()
            
            # Create a distribution record and update inventory
            user_name = self.view.current_user if hasattr(self.view, 'current_user') else 'System'
            
            for item in items:
                # Deduct from inventory
                ItemModel.adjust_stock(item['item_id'], -item['quantity'])
                
                # Log the distribution activity
                self.log_inventory_activity(
                    item_name=item['item_name'],
                    movement_type='distributed',
                    quantity=item['quantity'],
                    user_name=user_name,
                    notes=f"Distributed to {department}",
                    department=department
                )
                
            conn.commit()
            conn.close()
            
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText(f"Successfully distributed {len(items)} item(s) to {department}!")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            
            dialog.accept()
            self.refresh_inventory()
            
        except Exception as e:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to distribute stocks:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            import traceback
            traceback.print_exc()
    
    def handle_add_stock(self):
        """Handle adding a new inventory item from delivered purchase orders."""
        dlg = AddStockDialog(self.view)
        
        # Populate the item selector with delivered purchase order items
        self.populate_delivered_items(dlg)
        
        dlg.save_btn.clicked.connect(lambda: self.save_item(dlg))
        dlg.exec()
    
    def populate_delivered_items(self, dialog):
        """Populate the item selector with items from delivered purchase orders."""
        try:
            from models.purchase import PurchaseModel
            from models.database import get_conn, _paramstyle
            
            # Get delivered/received purchase orders and their items
            conn = get_conn()
            cur = conn.cursor()
            
            # Query to get items from delivered purchase orders with remaining quantity tracking
            sql = f"""
                SELECT 
                    pi.id as purchase_item_id,
                    pi.item_id,
                    COALESCE(pi.item_name, i.name) as item_name,
                    pi.quantity as ordered_qty,
                    COALESCE(pi.qty_added_to_inventory, 0) as qty_added,
                    (pi.quantity - COALESCE(pi.qty_added_to_inventory, 0)) as qty_available,
                    pi.unit_price,
                    p.id as purchase_id,
                    i.category,
                    i.unit
                FROM purchase_items pi
                JOIN purchases p ON pi.purchase_id = p.id
                LEFT JOIN items i ON pi.item_id = i.id
                WHERE p.status IN ('received', 'delivered', 'completed')
                AND (pi.quantity - COALESCE(pi.qty_added_to_inventory, 0)) > 0
                ORDER BY p.created_at DESC, COALESCE(pi.item_name, i.name)
            """
            cur.execute(sql)
            rows = cur.fetchall()
            
            dialog.item_selector.clear()
            dialog.item_selector.addItem("-- Select Item from Delivered Orders --", None)
            
            for row in rows:
                try:
                    row_dict = dict(row)
                except:
                    row_dict = {
                        'purchase_item_id': row[0],
                        'item_id': row[1],
                        'item_name': row[2],
                        'ordered_qty': row[3],
                        'qty_added': row[4],
                        'qty_available': row[5],
                        'unit_price': row[6],
                        'purchase_id': row[7],
                        'category': row[8] if len(row) > 8 else 'General',
                        'unit': row[9] if len(row) > 9 else 'pcs'
                    }
                
                # Create display text showing available quantity
                item_name = row_dict.get('item_name', 'Unknown')
                qty_available = row_dict.get('qty_available', 0)
                ordered_qty = row_dict.get('ordered_qty', 0)
                purchase_id = row_dict.get('purchase_id', 0)
                display_text = f"{item_name} - Order #{purchase_id:04d} (Available: {qty_available}/{ordered_qty})"
                
                # Add to combo box with data
                dialog.item_selector.addItem(display_text, row_dict)
            
            conn.close()
            
        except Exception as e:
            print(f"Error loading delivered items: {e}")
            import traceback
            traceback.print_exc()
            # Add a default message if query fails
            dialog.item_selector.addItem("No delivered items found", None)
    
    def handle_edit_item(self, item):
        """Handle editing an existing inventory item."""
        # Check if user is a department user
        is_dept_user = self.view.current_role == "Department"
        
        dlg = AddStockDialog(self.view, item, is_department_user=is_dept_user)
        dlg.save_btn.clicked.connect(lambda: self.update_item(item.get('id'), dlg))
        dlg.exec()
    
    def save_item(self, dialog):
        """Save a new inventory item to database from delivered purchase order."""
        data = dialog.get_data()
        
        # Validate - check if item was selected
        if not data.get('name') or data.get('name') == '-- Select Item from Delivered Orders --':
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please select an item from delivered orders.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        if data.get('stock_qty', 0) <= 0:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter a valid quantity.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        try:
            from models.database import get_conn, _paramstyle
            conn = get_conn()
            cur = conn.cursor()
            
            # Check if item_id already exists in inventory
            item_id = data.get('item_id')
            qty_to_add = data['stock_qty']
            
            if item_id:
                # Item exists - update the quantity
                if _paramstyle == 'qmark':
                    sql = """
                        UPDATE items 
                        SET stock_qty = stock_qty + ?
                        WHERE id = ?
                    """
                    cur.execute(sql, (qty_to_add, item_id))
                else:
                    sql = """
                        UPDATE items 
                        SET stock_qty = stock_qty + %s
                        WHERE id = %s
                    """
                    cur.execute(sql, (qty_to_add, item_id))
                
                conn.commit()
                success_msg = f"Added {qty_to_add} units to existing item!"
            else:
                # Item doesn't exist yet - create new entry
                result = ItemModel.add_item(
                    name=data['name'],
                    category=data['category'],
                    unit=data['unit'],
                    unit_cost=data['unit_cost'],
                    stock_qty=qty_to_add,
                    min_stock=data.get('min_stock', 10)
                )
                
                if not result:
                    raise Exception("Failed to create new inventory item")
                
                success_msg = "Item added to inventory successfully!"
            
            # Update the purchase_items table to track how much was added
            purchase_item_id = data.get('purchase_item_id')
            if purchase_item_id:
                if _paramstyle == 'qmark':
                    # Increment qty_added_to_inventory
                    sql = """
                        UPDATE purchase_items 
                        SET qty_added_to_inventory = COALESCE(qty_added_to_inventory, 0) + ?
                        WHERE id = ?
                    """
                    cur.execute(sql, (qty_to_add, purchase_item_id))
                    
                    # Check if fully added, if so mark in_inventory = 1
                    sql = """
                        UPDATE purchase_items 
                        SET in_inventory = 1
                        WHERE id = ? 
                        AND quantity <= COALESCE(qty_added_to_inventory, 0)
                    """
                    cur.execute(sql, (purchase_item_id,))
                else:
                    # Increment qty_added_to_inventory
                    sql = """
                        UPDATE purchase_items 
                        SET qty_added_to_inventory = COALESCE(qty_added_to_inventory, 0) + %s
                        WHERE id = %s
                    """
                    cur.execute(sql, (qty_to_add, purchase_item_id))
                    
                    # Check if fully added, if so mark in_inventory = 1
                    sql = """
                        UPDATE purchase_items 
                        SET in_inventory = 1
                        WHERE id = %s 
                        AND quantity <= COALESCE(qty_added_to_inventory, 0)
                    """
                    cur.execute(sql, (purchase_item_id,))
                    
                conn.commit()
            
            conn.close()
            
            # Log the activity
            user_name = self.view.current_user if hasattr(self.view, 'current_user') else 'Purchase Admin'
            self.log_inventory_activity(
                item_name=data['name'],
                movement_type='stock_in',
                quantity=qty_to_add,
                user_name=user_name,
                notes='Added from purchase order',
                department=data.get('category')
            )
            
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText(success_msg)
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            dialog.accept()
            self.refresh_inventory()
            
        except Exception as e:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to add item:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            import traceback
            traceback.print_exc()
    
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
        from models.database import get_conn
        
        try:
            # Fetch real inventory history from database
            history_data = self.get_inventory_history()
            
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
            import traceback
            traceback.print_exc()
    
    def get_inventory_history(self):
        """Fetch inventory history from database."""
        from models.database import get_conn
        from datetime import datetime
        
        try:
            conn = get_conn()
            cur = conn.cursor()
            
            # Query to get inventory movements
            # This includes: items added from purchases, distributions to departments, adjustments
            sql = """
                SELECT 
                    created_at,
                    item_name,
                    movement_type,
                    quantity,
                    user_name,
                    notes,
                    department
                FROM inventory_history
                ORDER BY created_at DESC
                LIMIT 100
            """
            
            cur.execute(sql)
            rows = cur.fetchall()
            conn.close()
            
            history_data = []
            for row in rows:
                try:
                    row_dict = dict(row)
                except:
                    row_dict = {
                        'created_at': row[0],
                        'item_name': row[1],
                        'movement_type': row[2],
                        'quantity': row[3],
                        'user_name': row[4],
                        'notes': row[5],
                        'department': row[6] if len(row) > 6 else None
                    }
                
                # Format the data for display
                timestamp = row_dict.get('created_at')
                if timestamp:
                    try:
                        if isinstance(timestamp, str):
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        else:
                            dt = timestamp
                        formatted_time = dt.strftime('%Y-%m-%d %I:%M %p')
                    except:
                        formatted_time = str(timestamp)
                else:
                    formatted_time = 'Unknown'
                
                movement_type = row_dict.get('movement_type', 'Unknown')
                # Map movement types to display names
                type_mapping = {
                    'stock_in': 'Stock In',
                    'stock_out': 'Stock Out',
                    'distributed': 'Stock Out',
                    'adjustment': 'Adjustment',
                    'damage': 'Adjustment',
                    'added': 'Stock In'
                }
                display_type = type_mapping.get(movement_type.lower(), movement_type)
                
                quantity = row_dict.get('quantity', 0)
                # Add + or - prefix
                if display_type == 'Stock In':
                    qty_display = f"+{quantity}"
                elif display_type == 'Stock Out':
                    qty_display = f"-{quantity}"
                else:
                    qty_display = str(quantity)
                
                notes = row_dict.get('notes', '-')
                department = row_dict.get('department')
                if department and 'department' not in notes.lower():
                    notes = f"{notes} ({department})" if notes != '-' else department
                
                history_data.append({
                    'timestamp': formatted_time,
                    'item_name': row_dict.get('item_name', 'Unknown'),
                    'type': display_type,
                    'quantity': qty_display,
                    'user': row_dict.get('user_name', 'System'),
                    'notes': notes
                })
            
            return history_data
            
        except Exception as e:
            print(f"Error fetching inventory history: {e}")
            import traceback
            traceback.print_exc()
            # Return empty list if table doesn't exist yet
            return []
    
    @staticmethod
    def log_inventory_activity(item_name, movement_type, quantity, user_name, notes='', department=None):
        """Log an inventory activity to the history table."""
        from models.database import get_conn, _paramstyle
        from datetime import datetime
        
        try:
            conn = get_conn()
            cur = conn.cursor()
            
            if _paramstyle == 'qmark':
                sql = """
                    INSERT INTO inventory_history 
                    (item_name, movement_type, quantity, user_name, notes, department, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cur.execute(sql, (item_name, movement_type, quantity, user_name, notes, department, datetime.now()))
            else:
                sql = """
                    INSERT INTO inventory_history 
                    (item_name, movement_type, quantity, user_name, notes, department, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (item_name, movement_type, quantity, user_name, notes, department, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error logging inventory activity: {e}")
            import traceback
            traceback.print_exc()
            return False


