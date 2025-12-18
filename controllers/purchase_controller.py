from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from views.order_stocks import OrderStocksDialog, AddItemDialog

class PurchaseController:
    def __init__(self, view, model, dashboard=None):
        self.view = view
        self.model = model
        self.dashboard = dashboard  # Reference to dashboard for current_user
        # Connect main dashboard button to open procurement
        self.view.btn_order_stocks.clicked.connect(self.handle_open_order_stocks)
        self.refresh_table()

    def handle_open_order_stocks(self):
        """Opens the main Procurement Dialog."""
        dlg = OrderStocksDialog(self.view)
        # Connect the '+ ADD NEW LINE' button inside the dialog
        dlg.add_item_btn.clicked.connect(lambda: self.handle_open_add_item(dlg))
        # Connect the 'CONFIRM' button
        dlg.save_btn.clicked.connect(lambda: self.handle_save_procurement(dlg))
        dlg.exec()

    def handle_open_add_item(self, parent_dlg):
        """Opens the Add Item modal and handles data return."""
        add_dlg = AddItemDialog(parent_dlg)
        
        # Populate Suppliers via Controller/Model with contact info
        from models.purchase import SupplierModel
        try:
            add_dlg.supplier_cb.addItem("-- Select Supplier --", None)
            suppliers = SupplierModel.list_suppliers()
            for s in suppliers:
                supplier_name = s.get('name', 'Unknown')
                supplier_id = s.get('id')
                contact_name = s.get('contact_name', '')
                # Store supplier_id as main data, contact_name as UserRole+1
                add_dlg.supplier_cb.addItem(supplier_name, supplier_id)
                # Store contact in the item data
                idx = add_dlg.supplier_cb.count() - 1
                add_dlg.supplier_cb.setItemData(idx, contact_name, Qt.ItemDataRole.UserRole + 1)
        except Exception as e:
            print(f"Error loading suppliers: {e}")

        # If user clicks 'ADD TO LIST'
        if add_dlg.exec() == QDialog.DialogCode.Accepted:
            data = add_dlg.get_data()
            self.add_row_to_procurement_table(parent_dlg, data)

    def add_row_to_procurement_table(self, dlg, data):
        """Logic to insert a new row into the procurement grid."""
        r = dlg.table.rowCount()
        dlg.table.insertRow(r)
        
        # Mapping data to table columns
        cols = [
            data['item_name'], data['category'], data['unit'], 
            str(data['qty']), f"₱{data['price']:,.2f}", f"₱{data['total']:,.2f}"
        ]
        
        for i, val in enumerate(cols):
            item = QTableWidgetItem(val)
            # store supplier id and expected_date on the item for later retrieval when saving
            if i == 0:
                try:
                    item.setData(Qt.ItemDataRole.UserRole, data.get('supplier_id'))
                    item.setData(Qt.ItemDataRole.UserRole + 2, data.get('expected_date'))
                except Exception:
                    pass
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            dlg.table.setItem(r, i, item)
        
        # Add the Remove button logic
        rm_btn = QPushButton("REMOVE")
        rm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        rm_btn.setStyleSheet("color: #dc3545; border: none; font-size: 9px; font-weight: bold; background: transparent;")
        rm_btn.clicked.connect(lambda: self.remove_procurement_row(dlg, rm_btn))
        dlg.table.setCellWidget(r, 6, rm_btn)
        
        self.recalc_dlg_total(dlg)

    def remove_procurement_row(self, dlg, btn):
        """Identifies and removes the specific row containing the clicked button."""
        for r in range(dlg.table.rowCount()):
            if dlg.table.cellWidget(r, 6) == btn:
                dlg.table.removeRow(r)
                break
        self.recalc_dlg_total(dlg)

    def recalc_dlg_total(self, dlg):
        """Calculates the Grand Total of all lines in the procurement table."""
        total = 0.0
        for r in range(dlg.table.rowCount()):
            try:
                val = dlg.table.item(r, 5).text().replace("₱", "").replace(",", "").strip()
                total += float(val)
            except:
                continue
        dlg.total_lbl.setText(f"TOTAL AMOUNT: ₱ {total:,.2f}")

    def handle_save_procurement(self, dlg):
        """Final save logic to push the order to the database."""
        # Validate
        if dlg.table.rowCount() == 0:
            QMessageBox.warning(dlg, "Validation", "Please add at least one item before saving.")
            return

        # Determine supplier_id and expected_date (try to read from first row item's stored data)
        supplier_id = None
        expected_date = None
        try:
            first_item = dlg.table.item(0, 0)
            if first_item is not None:
                supplier_id = first_item.data(Qt.ItemDataRole.UserRole)
                expected_date = first_item.data(Qt.ItemDataRole.UserRole + 2)  # stored expected date
        except Exception:
            supplier_id = None
            expected_date = None

        # Collect items and ensure they exist in the items table
        from models.purchase import ItemModel
        items = []
        for r in range(dlg.table.rowCount()):
            try:
                name = dlg.table.item(r, 0).text().strip()
                category = dlg.table.item(r, 1).text().strip() if dlg.table.item(r, 1) else 'General'
                unit = dlg.table.item(r, 2).text().strip() if dlg.table.item(r, 2) else ''
                quantity = int(dlg.table.item(r, 3).text())
                price_txt = dlg.table.item(r, 4).text().replace("₱", "").replace(",", "").strip()
                unit_price = float(price_txt) if price_txt else 0.0
                
                # Create or find item in items table
                item_id = self.get_or_create_item(name, unit, unit_price, category)
                
                items.append({ 
                    'item_id': item_id, 
                    'quantity': quantity, 
                    'unit_price': unit_price 
                })
            except Exception as e:
                # skip invalid rows but log the error
                print(f"[CONTROLLER ERROR] Skipping row {r}: {e}")
                continue

        # Call model to create purchase with expected_date and created_by
        try:
            # Get current user from dashboard
            created_by = None
            if self.dashboard and hasattr(self.dashboard, 'current_user'):
                created_by = self.dashboard.current_user
            
            pid = self.model.create_purchase(supplier_id, items, expected_date, created_by)
            msg = QMessageBox(dlg)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Saved")
            msg.setText(f"Purchase Order created (ID: {pid})")
            msg.setStyleSheet("QLabel { color: black; }")
            msg.exec()
            dlg.accept()
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(dlg, "Error", f"Failed to create purchase order:\n{e}")

    def get_or_create_item(self, name, unit, unit_cost, category='General'):
        """Check if item exists by name, if not create it. Return item_id."""
        from models.purchase import ItemModel
        from models.database import get_conn, DB_DRIVER
        
        conn = get_conn()
        try:
            cur = conn.cursor()
            param = "%s" if DB_DRIVER == 'mariadb' else "?"
            
            # Check if item exists
            cur.execute(f"SELECT id FROM items WHERE name = {param}", (name,))
            row = cur.fetchone()
            
            if row:
                return row[0]
            
            # Create new item
            cur.execute(
                f"INSERT INTO items (name, unit, unit_cost, category, stock_qty) VALUES ({param}, {param}, {param}, {param}, 0)",
                (name, unit, unit_cost, category)
            )
            conn.commit()
            
            # Get the newly created item_id
            if DB_DRIVER == 'mariadb':
                return cur.lastrowid
            else:
                return conn.execute('SELECT last_insert_rowid()').fetchone()[0]
                
        finally:
            conn.close()

    def refresh_table(self):
        """Updates the main Purchase Page history list."""
        data = self.model.list_purchases()
        self.view.load_history(data)