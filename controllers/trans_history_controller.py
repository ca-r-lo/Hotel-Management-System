"""
Transaction History Controller for Owner/Director role.
Displays all purchase transactions with filtering capabilities.
"""

from PyQt6.QtWidgets import QMessageBox


class TransactionHistoryController:
    """Controller for managing transaction history view."""
    
    def __init__(self, view, model):
        self.view = view
        self.model = model
        
        # Connect filter change events
        self.view.year_filter.currentTextChanged.connect(self.refresh_transactions)
        self.view.month_filter.currentTextChanged.connect(self.refresh_transactions)
        
        # Load initial data
        self.refresh_transactions()
    
    def refresh_transactions(self):
        """Refresh the transaction history table with filters applied."""
        try:
            # Get filter values
            selected_year = self.view.year_filter.currentText()
            selected_month = self.view.month_filter.currentText()
            
            # Get all purchases from model
            purchases = self.model.list_purchases()
            
            # Apply filters
            filtered_purchases = self.apply_filters(purchases, selected_year, selected_month)
            
            # Populate the table
            self.view.populate_table(filtered_purchases)
            
        except Exception as e:
            print(f"Error refreshing transactions: {e}")
            import traceback
            traceback.print_exc()
    
    def apply_filters(self, purchases, year, month):
        """Apply year and month filters to purchase data."""
        filtered = []
        
        for purchase in purchases:
            # Get purchase date
            created_at = purchase.get('created_at')
            if not created_at:
                continue
            
            # Parse date
            try:
                if isinstance(created_at, str):
                    # Format: "YYYY-MM-DD HH:MM:SS" or "YYYY-MM-DD"
                    date_parts = created_at.split(' ')[0].split('-')
                    purchase_year = date_parts[0]
                    purchase_month = int(date_parts[1])
                else:
                    # datetime object
                    purchase_year = str(created_at.year)
                    purchase_month = created_at.month
            except Exception as e:
                print(f"Error parsing date: {e}")
                continue
            
            # Apply year filter
            if purchase_year != year:
                continue
            
            # Apply month filter
            if month != "All Months":
                month_map = {
                    "January": 1, "February": 2, "March": 3, "April": 4,
                    "May": 5, "June": 6, "July": 7, "August": 8,
                    "September": 9, "October": 10, "November": 11, "December": 12
                }
                selected_month_num = month_map.get(month)
                if selected_month_num and purchase_month != selected_month_num:
                    continue
            
            filtered.append(purchase)
        
        return filtered
