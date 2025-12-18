from PyQt6.QtWidgets import QMessageBox
from views.messages import ComposeMessageDialog
from models.purchase import MessageModel
from models.user import UserModel
from configs.config import DB_CONFIG
from datetime import datetime


class MessagesController:
    def __init__(self, view, model, dashboard):
        self.view = view
        self.model = model
        self.dashboard = dashboard
        
        # Initialize user model with database config
        self.user_model = UserModel(DB_CONFIG)
        
        # Get current user ID
        self.current_user_id = self.get_current_user_id()
        
        # Connect action buttons
        self.view.btn_compose.clicked.connect(self.handle_compose)
        
        # Set delete callback
        self.view.delete_message = self.handle_delete_message
        
        # Don't load messages here - they will be loaded when the user switches to the messages page
    
    def get_current_user_id(self):
        """Get the current logged-in user's ID."""
        try:
            current_user_name = self.dashboard.current_user
            if current_user_name:
                user = self.user_model.get_user_by_name(current_user_name)
                if user:
                    return user['id']
            # Default to user ID 1 if not found
            return 1
        except Exception as e:
            print(f"Error getting current user ID: {e}")
            return 1
    
    def refresh_messages(self):
        """Refresh the messages list from database."""
        try:
            messages = self.model.list_messages(self.current_user_id)
            # Add current_user_id to each message for display logic
            for msg in messages:
                msg['current_user_id'] = self.current_user_id
            self.view.populate_messages(messages)
        except Exception as e:
            print(f"Error loading messages: {e}")
            import traceback
            traceback.print_exc()
    
    def handle_compose(self):
        """Handle composing a new message."""
        try:
            # Get all users for recipient selection
            users = self.user_model.get_all_users()
            
            dlg = ComposeMessageDialog(self.view)
            
            # Populate recipient dropdown with users
            dlg.to_input.clear()
            for user in users:
                if user['id'] != self.current_user_id:  # Don't include current user
                    dlg.to_input.addItem(f"{user['full_name']} ({user['role']})", user['id'])
            
            if dlg.exec():
                data = dlg.get_data()
                recipient_id = dlg.to_input.currentData()
                category = data['category']
                subject = data['subject']
                body = data['body']
                
                if not subject or not body:
                    msg = QMessageBox(self.view)
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setWindowTitle("Validation Error")
                    msg.setText("Please fill in both subject and message body.")
                    msg.setStyleSheet("QLabel { color: #000000; }")
                    msg.exec()
                    return
                
                if not recipient_id:
                    msg = QMessageBox(self.view)
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setWindowTitle("Validation Error")
                    msg.setText("Please select a recipient.")
                    msg.setStyleSheet("QLabel { color: #000000; }")
                    msg.exec()
                    return
                
                # Save message to database
                self.model.add_message(self.current_user_id, recipient_id, category, subject, body)
                
                # Refresh the messages list
                self.refresh_messages()
                
                # Show success message
                msg = QMessageBox(self.view)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Message sent successfully!")
                msg.setStyleSheet("QLabel { color: #000000; }")
                msg.exec()
                
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to send message:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            import traceback
            traceback.print_exc()
    
    def handle_delete_message(self, message_id):
        """Handle deleting a message."""
        try:
            # Confirm deletion
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("Confirm Delete")
            msg.setText("Are you sure you want to delete this message?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setStyleSheet("QLabel { color: #000000; }")
            
            if msg.exec() == QMessageBox.StandardButton.Yes:
                # Delete from database
                self.model.delete_message(message_id)
                
                # Refresh messages list
                self.refresh_messages()
                
                # Show success message
                success_msg = QMessageBox(self.view)
                success_msg.setIcon(QMessageBox.Icon.Information)
                success_msg.setWindowTitle("Success")
                success_msg.setText("Message deleted successfully!")
                success_msg.setStyleSheet("QLabel { color: #000000; }")
                success_msg.exec()
                
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to delete message:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
