"""Controller for Requests page."""

from PyQt6.QtWidgets import QMessageBox, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from views.requests import SendRequestDialog
from models.request import RequestModel
from models.purchase import ItemModel

STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


class RequestsController:
    """Controller for managing stock requests."""
    
    def __init__(self, view):
        self.view = view
        
        # Connect buttons
        self.view.btn_send_request.clicked.connect(self.handle_send_request)
        self.view.btn_archive.clicked.connect(self.handle_toggle_archive)
        self.view.btn_sort.clicked.connect(self.handle_sort)
        
        # Create table if doesn't exist
        RequestModel.create_table()
    
    def set_user_info(self, user_name, user_role, department):
        """Set current user information."""
        self.view.current_user = user_name
        self.view.current_role = user_role
        self.view.current_department = department
        
        # Store role for conditional logic
        self.user_role = user_role
        self.user_department = department
        
        # Hide Send Request button for Purchase Admin/Owner
        if user_role in ["Purchase Admin", "Owner"]:
            self.view.btn_send_request.hide()
        else:
            self.view.btn_send_request.show()
        
        # Load requests
        self.refresh_requests()
    
    def handle_send_request(self):
        """Handle sending a new request."""
        dialog = SendRequestDialog(
            self.view,
            department=self.view.current_department,
            user_name=self.view.current_user
        )
        dialog.send_btn.clicked.connect(lambda: self.save_request(dialog))
        dialog.exec()
    
    def save_request(self, dialog):
        """Save a new request to database."""
        data = dialog.get_data()
        
        # Validate
        if not data['item_name']:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter an item name.")
            msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #111827; font-size: 13px; }
                QPushButton { 
                    background-color: #0056b3; 
                    color: white; 
                    border: none; 
                    padding: 8px 20px; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #003d82; }
            """)
            msg.exec()
            return
        
        if not data['unit']:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter a unit.")
            msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #111827; font-size: 13px; }
                QPushButton { 
                    background-color: #0056b3; 
                    color: white; 
                    border: none; 
                    padding: 8px 20px; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #003d82; }
            """)
            msg.exec()
            return
        
        try:
            RequestModel.create_request(
                department=self.view.current_department,
                requested_by=self.view.current_user,
                item_name=data['item_name'],
                quantity=data['quantity'],
                unit=data['unit'],
                reason=data['reason']
            )
            
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText("Request sent successfully!")
            msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #111827; font-size: 13px; }
                QPushButton { 
                    background-color: #10b981; 
                    color: white; 
                    border: none; 
                    padding: 8px 20px; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #059669; }
            """)
            msg.exec()
            dialog.accept()
            self.refresh_requests()
            
        except Exception as e:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to send request:\n{e}")
            msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #111827; font-size: 13px; }
                QPushButton { 
                    background-color: #ef4444; 
                    color: white; 
                    border: none; 
                    padding: 8px 20px; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #dc2626; }
            """)
            msg.exec()
    
    def handle_toggle_archive(self):
        """Toggle between showing active and archived requests."""
        self.view.show_archived = not self.view.show_archived
        
        if self.view.show_archived:
            self.view.btn_archive.setText("ACTIVE")
        else:
            self.view.btn_archive.setText("ARCHIVE")
        
        self.refresh_requests()
    
    def handle_sort(self):
        """Handle sorting requests."""
        # TODO: Implement sorting options
        msg = QMessageBox(self.view)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Sort")
        msg.setText("Sorting options coming soon!")
        msg.setStyleSheet("""
            QMessageBox { background-color: white; }
            QLabel { color: #111827; font-size: 13px; }
            QPushButton { 
                background-color: #0056b3; 
                color: white; 
                border: none; 
                padding: 8px 20px; 
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #003d82; }
        """)
        msg.exec()
    
    def refresh_requests(self):
        """Reload and display requests."""
        try:
            # Clear existing requests
            while self.view.requests_layout.count() > 1:  # Keep the stretch
                item = self.view.requests_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Get requests based on role
            if self.view.current_role == "Department":
                requests = RequestModel.get_requests_by_department(
                    self.view.current_department,
                    include_archived=self.view.show_archived
                )
            else:
                # Purchase Admin or Owner sees all requests
                requests = RequestModel.get_all_requests(
                    include_archived=self.view.show_archived
                )
            
            # Display requests
            if not requests:
                no_requests_label = QLabel("No requests found.")
                no_requests_label.setStyleSheet("color: #6b7280; font-size: 14px; border: none;")
                no_requests_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.requests_layout.insertWidget(0, no_requests_label)
            else:
                for request in requests:
                    request_card = self.create_request_card(request)
                    self.view.requests_layout.insertWidget(
                        self.view.requests_layout.count() - 1,  # Before stretch
                        request_card
                    )
        
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load requests:\n{e}")
            msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #111827; font-size: 13px; }
                QPushButton { 
                    background-color: #ef4444; 
                    color: white; 
                    border: none; 
                    padding: 8px 20px; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #dc2626; }
            """)
            msg.exec()
    
    def create_request_card(self, request):
        """Create a card widget for a request."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                border-radius: 6px;
            }}
            QFrame:hover {{
                border-color: {STYLE_BLUE};
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
        """)
        card.setMinimumHeight(85)
        card.setMaximumHeight(85)
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(16, 12, 16, 12)
        card_layout.setSpacing(16)
        
        # Request info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # Item name and quantity
        item_label = QLabel(f"{request['item_name']} - {request['quantity']} {request['unit']}")
        item_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        item_label.setStyleSheet(f"color: {STYLE_NAVY}; border: none;")
        info_layout.addWidget(item_label)
        
        # Department and requester
        details_label = QLabel(f"{request['department']} • Requested by {request['requested_by']}")
        details_label.setStyleSheet("color: #6b7280; font-size: 12px; border: none;")
        info_layout.addWidget(details_label)
        
        # Status and date
        status_text = request['status']
        status_color = "#10b981" if status_text == "Approved" else "#f59e0b" if status_text == "Pending" else "#6b7280"
        
        created_at = request['created_at'].strftime("%b %d, %Y") if hasattr(request['created_at'], 'strftime') else str(request['created_at'])
        status_label = QLabel(f"Status: <span style='color: {status_color}; font-weight: bold;'>{status_text}</span> • {created_at}")
        status_label.setStyleSheet("color: #6b7280; font-size: 11px; border: none;")
        info_layout.addWidget(status_label)
        
        card_layout.addLayout(info_layout)
        card_layout.addStretch()
        
        # Show different buttons based on role and status
        if self.user_role in ["Purchase Admin", "Owner"] and request['status'] == 'Pending':
            # Approve button for Purchase Admin/Owner
            approve_btn = QPushButton("✓ APPROVE")
            approve_btn.setFixedSize(100, 42)
            approve_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            approve_btn.setToolTip("Approve and distribute stock")
            approve_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #10b981;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ 
                    background-color: #059669;
                }}
            """)
            approve_btn.clicked.connect(lambda: self.handle_approve_request(request))
            card_layout.addWidget(approve_btn)
            
            # Reject button
            reject_btn = QPushButton("✗ REJECT")
            reject_btn.setFixedSize(90, 42)
            reject_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            reject_btn.setToolTip("Reject request")
            reject_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #ef4444;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ 
                    background-color: #dc2626;
                }}
            """)
            reject_btn.clicked.connect(lambda: self.handle_reject_request(request['id']))
            card_layout.addWidget(reject_btn)
        else:
            # Delete button (trash icon) - for department users or completed requests
            delete_btn = QPushButton("🗑")
            delete_btn.setFixedSize(42, 42)
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.setToolTip("Delete request")
            delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #ef4444;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 18px;
                }}
                QPushButton:hover {{ 
                    background-color: #dc2626;
                }}
            """)
            delete_btn.clicked.connect(lambda: self.handle_delete_request(request['id']))
            card_layout.addWidget(delete_btn)
        
        return card
    
    def handle_delete_request(self, request_id):
        """Handle deleting a request."""
        msg = QMessageBox(self.view)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Delete")
        msg.setText("Are you sure you want to delete this request?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("""
            QMessageBox { background-color: white; }
            QLabel { color: #111827; font-size: 13px; }
            QPushButton { 
                background-color: #0056b3; 
                color: white; 
                border: none; 
                padding: 8px 20px; 
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover { background-color: #003d82; }
        """)
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                RequestModel.delete_request(request_id)
                
                success_msg = QMessageBox(self.view)
                success_msg.setIcon(QMessageBox.Icon.Information)
                success_msg.setWindowTitle("Success")
                success_msg.setText("Request deleted successfully!")
                success_msg.setStyleSheet("""
                    QMessageBox { background-color: white; }
                    QLabel { color: #111827; font-size: 13px; }
                    QPushButton { 
                        background-color: #10b981; 
                        color: white; 
                        border: none; 
                        padding: 8px 20px; 
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #059669; }
                """)
                success_msg.exec()
                
                self.refresh_requests()
            except Exception as e:
                error_msg = QMessageBox(self.view)
                error_msg.setIcon(QMessageBox.Icon.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText(f"Failed to delete request:\n{e}")
                error_msg.setStyleSheet("""
                    QMessageBox { background-color: white; }
                    QLabel { color: #111827; font-size: 13px; }
                    QPushButton { 
                        background-color: #ef4444; 
                        color: white; 
                        border: none; 
                        padding: 8px 20px; 
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #dc2626; }
                """)
                error_msg.exec()
    
    def handle_approve_request(self, request):
        """Handle approving a request."""
        from views.requests import DistributeStockDialog
        
        # Show distribute dialog
        dialog = DistributeStockDialog(self.view, request=request)
        dialog.approve_btn.clicked.connect(lambda: self.process_approval(dialog, request))
        dialog.exec()
    
    def process_approval(self, dialog, request):
        """Process the approval and deduct stock."""
        data = dialog.get_data()
        distributed_qty = data['quantity']
        notes = data['notes']
        
        # Check if item exists in inventory
        try:
            items = ItemModel.list_items()
            matching_item = None
            for item in items:
                if item['name'].lower() == request['item_name'].lower():
                    matching_item = item
                    break
            
            if not matching_item:
                error_msg = QMessageBox(dialog)
                error_msg.setIcon(QMessageBox.Icon.Warning)
                error_msg.setWindowTitle("Item Not Found")
                error_msg.setText(f"Item '{request['item_name']}' not found in inventory. Cannot distribute stock.")
                error_msg.setStyleSheet("""
                    QMessageBox { background-color: white; }
                    QLabel { color: #111827; font-size: 13px; }
                    QPushButton { 
                        background-color: #ef4444; 
                        color: white; 
                        border: none; 
                        padding: 8px 20px; 
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #dc2626; }
                """)
                error_msg.exec()
                return
            
            # Check if enough stock
            current_stock = matching_item.get('stock_qty', 0)
            if current_stock < distributed_qty:
                error_msg = QMessageBox(dialog)
                error_msg.setIcon(QMessageBox.Icon.Warning)
                error_msg.setWindowTitle("Insufficient Stock")
                error_msg.setText(f"Insufficient stock. Available: {current_stock} {matching_item['unit']}, Requested: {distributed_qty} {request['unit']}")
                error_msg.setStyleSheet("""
                    QMessageBox { background-color: white; }
                    QLabel { color: #111827; font-size: 13px; }
                    QPushButton { 
                        background-color: #ef4444; 
                        color: white; 
                        border: none; 
                        padding: 8px 20px; 
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #dc2626; }
                """)
                error_msg.exec()
                return
            
            # Deduct stock
            ItemModel.adjust_stock(matching_item['id'], -distributed_qty)
            
            # Update request status
            RequestModel.approve_request(request['id'], distributed_qty, notes)
            
            # Close dialog
            dialog.accept()
            
            # Show success message
            success_msg = QMessageBox(self.view)
            success_msg.setIcon(QMessageBox.Icon.Information)
            success_msg.setWindowTitle("Success")
            success_msg.setText(f"Request approved! {distributed_qty} {request['unit']} distributed to {request['department']}.")
            success_msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #111827; font-size: 13px; }
                QPushButton { 
                    background-color: #10b981; 
                    color: white; 
                    border: none; 
                    padding: 8px 20px; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #059669; }
            """)
            success_msg.exec()
            
            # Refresh requests
            self.refresh_requests()
            
        except Exception as e:
            error_msg = QMessageBox(dialog)
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText(f"Failed to approve request:\n{e}")
            error_msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #111827; font-size: 13px; }
                QPushButton { 
                    background-color: #ef4444; 
                    color: white; 
                    border: none; 
                    padding: 8px 20px; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #dc2626; }
            """)
            error_msg.exec()
    
    def handle_reject_request(self, request_id):
        """Handle rejecting a request."""
        from PyQt6.QtWidgets import QInputDialog
        
        # Ask for rejection reason
        reason, ok = QInputDialog.getText(
            self.view,
            "Reject Request",
            "Reason for rejection (optional):",
        )
        
        if ok:
            try:
                RequestModel.reject_request(request_id, reason if reason else None)
                
                success_msg = QMessageBox(self.view)
                success_msg.setIcon(QMessageBox.Icon.Information)
                success_msg.setWindowTitle("Success")
                success_msg.setText("Request rejected successfully!")
                success_msg.setStyleSheet("""
                    QMessageBox { background-color: white; }
                    QLabel { color: #111827; font-size: 13px; }
                    QPushButton { 
                        background-color: #10b981; 
                        color: white; 
                        border: none; 
                        padding: 8px 20px; 
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #059669; }
                """)
                success_msg.exec()
                
                self.refresh_requests()
            except Exception as e:
                error_msg = QMessageBox(self.view)
                error_msg.setIcon(QMessageBox.Icon.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText(f"Failed to reject request:\n{e}")
                error_msg.setStyleSheet("""
                    QMessageBox { background-color: white; }
                    QLabel { color: #111827; font-size: 13px; }
                    QPushButton { 
                        background-color: #ef4444; 
                        color: white; 
                        border: none; 
                        padding: 8px 20px; 
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #dc2626; }
                """)
                error_msg.exec()
    
    def refresh(self):
        """Placeholder refresh method for compatibility."""
        if hasattr(self, 'refresh_requests'):
            self.refresh_requests()


