from PyQt6.QtWidgets import QMessageBox
from views.track_orders import TrackOrdersDialog
from models.purchase import PurchaseModel


class TrackOrdersController:
    def __init__(self, parent_view, model):
        self.parent_view = parent_view
        self.model = model
        self.track_orders_dialog = None
        self.current_filter = "All"
    
    def open_track_orders(self):
        """Open the track orders dialog."""
        self.track_orders_dialog = TrackOrdersDialog(self.parent_view)
        
        # Connect filter dropdown
        self.track_orders_dialog.status_filter.currentTextChanged.connect(self.handle_filter_change)
        
        # Load initial data
        self.refresh_orders_list()
        
        self.track_orders_dialog.exec()
    
    def handle_filter_change(self, filter_value):
        """Handle status filter change."""
        self.current_filter = filter_value
        self.refresh_orders_list()
    
    def refresh_orders_list(self):
        """Reload orders from database and populate table."""
        if not self.track_orders_dialog:
            return
            
        try:
            # Get all orders
            all_orders = PurchaseModel.list_purchases()
            
            # Filter by status if not "All"
            if self.current_filter != "All":
                filtered_orders = [
                    order for order in all_orders 
                    if order.get('status', '').lower() == self.current_filter.lower()
                ]
            else:
                filtered_orders = all_orders
            
            self.track_orders_dialog.populate_table(filtered_orders, self)
        except Exception as e:
            msg = QMessageBox(self.track_orders_dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load orders:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def handle_update_status(self, order_id, new_status):
        """Handle updating order status."""
        try:
            result = PurchaseModel.update_order_status(order_id, new_status.lower())
            if result:
                msg = QMessageBox(self.track_orders_dialog)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText(f"Order #{order_id} status updated to {new_status}!")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                self.refresh_orders_list()
            else:
                msg = QMessageBox(self.track_orders_dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Failed to update order status.")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
        except Exception as e:
            msg = QMessageBox(self.track_orders_dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to update order status:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
