from PyQt6.QtWidgets import QMessageBox
from views.report_damages import ReportDamagesDialog, AddDamageReportDialog
from models.purchase import PurchaseModel, DamageModel


class ReportDamagesController:
    def __init__(self, parent_view, model, dashboard=None):
        self.parent_view = parent_view
        self.model = model
        self.dashboard = dashboard
        self.damages_dialog = None
    
    def open_report_damages(self):
        """Open the report damages dialog."""
        self.damages_dialog = ReportDamagesDialog(self.parent_view)
        
        # Connect new report button
        self.damages_dialog.new_report_btn.clicked.connect(self.handle_add_report)
        
        # Load initial data
        self.refresh_damages_list()
        
        self.damages_dialog.exec()
    
    def refresh_damages_list(self):
        """Reload damages from database and populate table."""
        if not self.damages_dialog:
            return
            
        try:
            damages = DamageModel.list_damages()
            self.damages_dialog.populate_table(damages)
        except Exception as e:
            msg = QMessageBox(self.damages_dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load damage reports:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def handle_add_report(self):
        """Handle adding a new damage report."""
        dlg = AddDamageReportDialog(self.damages_dialog)
        
        # Populate order dropdown
        try:
            dlg.order_cb.addItem("-- Select Order --", None)
            orders = PurchaseModel.list_purchases()
            for order in orders:
                display_text = f"Order #{order.get('id')} - {order.get('supplier_name', 'Unknown')}"
                dlg.order_cb.addItem(display_text, order.get('id'))
        except Exception as e:
            print(f"Error loading orders: {e}")
        
        # Connect add button
        dlg.add_btn.clicked.connect(lambda: self.save_damage_report(dlg))
        
        dlg.exec()
    
    def save_damage_report(self, dialog):
        """Save a new damage report to database."""
        data = dialog.get_data()
        
        # Validate
        if not data['purchase_id']:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please select an order.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        if not data['description']:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please provide a description.")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            return
        
        try:
            # Get current user
            created_by = None
            if self.dashboard and hasattr(self.dashboard, 'current_user'):
                created_by = self.dashboard.current_user
            
            # Save to database
            result = DamageModel.add_damage_report(
                purchase_id=data['purchase_id'],
                category=data['category'],
                reason=data['description'],
                created_by=created_by
            )
            
            if result:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Damage report added successfully!")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                dialog.accept()
                self.refresh_damages_list()
            else:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Failed to add damage report.")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
        except Exception as e:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to add damage report:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
