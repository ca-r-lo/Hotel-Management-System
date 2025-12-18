from PyQt6.QtWidgets import QDialog, QMessageBox

class PurchaseController:
    def __init__(self, view, model):
        self.view = view  # This is your PurchasePage
        self.model = model  # This is your PurchaseModel
        
        # Connect the main buttons from the PurchasePage
        self.view.nav_btns["ORDER STOCKS"].clicked.connect(self.handle_open_order_dialog)
        
        # Initial data load
        self.refresh_table()

    def handle_open_order_dialog(self):
        from views.purchase_view import OrderStocksDialog
        dlg = OrderStocksDialog(self.view)
        
        # Connect the Save button logic inside the dialog to the controller
        dlg.save_btn.clicked.disconnect() # Remove internal view connection if exists
        dlg.save_btn.clicked.connect(lambda: self.handle_save_order(dlg))
        
        dlg.exec()

    def handle_save_order(self, dialog):
        # 1. Collect items from the dialog's table
        items = []
        for r in range(dialog.table.rowCount()):
            try:
                name = dialog.table.item(r, 0).text().strip()
                qty = int(dialog.table.item(r, 3).text())
                price_txt = dialog.table.item(r, 4).text().replace("₱", "").replace(",", "").strip()
                price = float(price_txt)
                items.append({'item_name': name, 'qty': qty, 'price': price})
            except Exception:
                continue

        if not items:
            QMessageBox.warning(dialog, "Validation", "Please add at least one item.")
            return

        # 2. Save to database via Model
        try:
            # We pass None for supplier/date if your UI doesn't have them yet
            purchase_id = self.model.create_purchase(None, items, None)
            QMessageBox.information(dialog, "Success", f"Order #{purchase_id} saved successfully.")
            dialog.accept() # Close dialog
            self.refresh_table() # Update main history table
        except Exception as e:
            QMessageBox.critical(dialog, "Database Error", f"Could not save order: {e}")

    def refresh_table(self):
        """Fetches latest data from DB and tells the View to display it."""
        try:
            data = self.model.list_purchases()
            self.view.load_history(data)
        except Exception as e:
            print(f"Error loading history: {e}")