from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt
from views.suppliers import SuppliersDialog, AddSupplierDialog
from models.purchase import SupplierModel


class SuppliersController:
    def __init__(self, parent_view, model):
        self.parent_view = parent_view
        self.model = model
        self.suppliers_dialog = None
    
    def open_suppliers_management(self):
        """Open the suppliers management dialog."""
        self.suppliers_dialog = SuppliersDialog(self.parent_view)
        
        # Connect signals
        self.suppliers_dialog.add_btn.clicked.connect(self.handle_add_supplier)
        
        # Load initial data
        self.refresh_suppliers_list()
        
        self.suppliers_dialog.exec()
    
    def refresh_suppliers_list(self):
        """Reload suppliers from database and populate table."""
        if not self.suppliers_dialog:
            return
            
        try:
            suppliers = SupplierModel.list_suppliers()
            self.suppliers_dialog.populate_table(suppliers, self)
        except Exception as e:
            msg = QMessageBox(self.suppliers_dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load suppliers:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def handle_add_supplier(self):
        """Handle adding a new supplier."""
        dlg = AddSupplierDialog(self.suppliers_dialog)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            self.save_supplier(data)
    
    def handle_edit_supplier(self, supplier):
        """Handle editing an existing supplier."""
        dlg = AddSupplierDialog(self.suppliers_dialog, supplier)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            self.update_supplier(supplier.get('id'), data)
    
    def handle_delete_supplier(self, supplier):
        """Handle deleting a supplier with confirmation."""
        msg = QMessageBox(self.suppliers_dialog)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete supplier '{supplier.get('name')}'?\n\n"
                    f"This action cannot be undone.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        msg.setStyleSheet("QLabel { color: #000000; }")
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.delete_supplier(supplier.get('id'))
    
    def save_supplier(self, data):
        """Save new supplier to database."""
        try:
            SupplierModel.add_supplier(data)
            msg = QMessageBox(self.suppliers_dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText("Supplier added successfully!")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            self.refresh_suppliers_list()
        except Exception as e:
            msg = QMessageBox(self.suppliers_dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to add supplier:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def update_supplier(self, supplier_id, data):
        """Update existing supplier in database."""
        try:
            result = SupplierModel.update_supplier(supplier_id, data)
            if result:
                msg = QMessageBox(self.suppliers_dialog)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Supplier updated successfully!")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                self.refresh_suppliers_list()
            else:
                msg = QMessageBox(self.suppliers_dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Failed to update supplier.")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
        except Exception as e:
            msg = QMessageBox(self.suppliers_dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to update supplier:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def delete_supplier(self, supplier_id):
        """Delete supplier from database."""
        try:
            result = SupplierModel.delete_supplier(supplier_id)
            if result:
                msg = QMessageBox(self.suppliers_dialog)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Supplier deleted successfully!")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                self.refresh_suppliers_list()
            else:
                msg = QMessageBox(self.suppliers_dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Failed to delete supplier.")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
        except Exception as e:
            msg = QMessageBox(self.suppliers_dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to delete supplier:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
