from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QScrollArea, QDialog, QTextEdit, QLineEdit, QMessageBox, QSplitter,
    QComboBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPainter, QColor, QIcon, QPixmap

# --- Shared Style Constants ---
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


class ComposeMessageDialog(QDialog):
    """Dialog for composing a new message."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Compose Message")
        self.setMinimumSize(650, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_BLUE};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 20px;
            }}
        """)
        header_layout = QVBoxLayout(header)
        
        title = QLabel("✉️  COMPOSE NEW MESSAGE")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; border: none;")
        header_layout.addWidget(title)
        
        subtitle = QLabel("Send a message to your team members")
        subtitle.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 12px; border: none;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
        # Form content
        content = QWidget()
        content.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        content_layout.setSpacing(20)

        # Recipient
        to_label = QLabel("RECIPIENT:")
        to_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: 700; font-size: 11px; border: none;")
        content_layout.addWidget(to_label)
        
        self.to_input = QComboBox()
        self.to_input.setPlaceholderText("Select recipient...")
        self.to_input.setFixedHeight(45)
        self.to_input.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 10px 15px;
                background-color: #f9fafb;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QComboBox:focus {{ 
                border-color: {STYLE_BLUE}; 
                background-color: white;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
        """)
        content_layout.addWidget(self.to_input)
        
        # Category
        category_label = QLabel("CATEGORY:")
        category_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: 700; font-size: 11px; border: none;")
        content_layout.addWidget(category_label)
        
        self.category_input = QComboBox()
        self.category_input.addItems([
            "General",
            "Purchase Order",
            "Inventory Alert",
            "Stock Request",
            "Damage Report",
            "Urgent"
        ])
        self.category_input.setFixedHeight(45)
        self.category_input.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 10px 15px;
                background-color: #f9fafb;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QComboBox:focus {{ 
                border-color: {STYLE_BLUE}; 
                background-color: white;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
        """)
        content_layout.addWidget(self.category_input)

        # Subject
        subject_label = QLabel("SUBJECT:")
        subject_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: 700; font-size: 11px; border: none;")
        content_layout.addWidget(subject_label)
        
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Enter message subject...")
        self.subject_input.setFixedHeight(45)
        self.subject_input.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 10px 15px;
                background-color: #f9fafb;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QLineEdit:focus {{ 
                border-color: {STYLE_BLUE}; 
                background-color: white;
            }}
        """)
        content_layout.addWidget(self.subject_input)

        # Message Body
        body_label = QLabel("MESSAGE:")
        body_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: 700; font-size: 11px; border: none;")
        content_layout.addWidget(body_label)
        
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Type your message here...")
        self.body_input.setMinimumHeight(150)
        self.body_input.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px 15px;
                background-color: #f9fafb;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QTextEdit:focus {{ 
                border-color: {STYLE_BLUE}; 
                background-color: white;
            }}
        """)
        content_layout.addWidget(self.body_input)

        content_layout.addWidget(self.body_input)

        # Buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        button_row.addStretch()
        
        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.setFixedSize(120, 45)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 2px solid #e5e7eb;
                color: #6b7280;
                font-weight: 700;
                font-size: 12px;
                border-radius: 8px;
            }}
            QPushButton:hover {{ 
                background-color: #f9fafb; 
                border-color: #d1d5db;
            }}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.send_btn = QPushButton("✉️  SEND MESSAGE")
        self.send_btn.setFixedSize(160, 45)
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_BLUE};
                color: white;
                border: none;
                font-weight: 700;
                font-size: 12px;
                border-radius: 8px;
            }}
            QPushButton:hover {{ background-color: #004494; }}
        """)
        self.send_btn.clicked.connect(self.accept)
        
        button_row.addWidget(self.cancel_btn)
        button_row.addWidget(self.send_btn)
        content_layout.addLayout(button_row)
        
        layout.addWidget(content)

    def get_data(self):
        """Return the message data."""
        return {
            'category': self.category_input.currentText(),
            'subject': self.subject_input.text(),
            'body': self.body_input.toPlainText()
        }


class MessageItem(QFrame):
    """Gmail-style message item - simple one-line preview."""
    
    def __init__(self, message_id, sender_id, recipient_id, current_user_id, sender_name, sender_role, recipient_name, recipient_role, category, subject, body, is_read, created_at, on_delete, parent=None):
        super().__init__(parent)
        self.message_id = message_id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.current_user_id = current_user_id
        self.on_delete = on_delete
        self.is_read = is_read
        self.is_sent = (sender_id == current_user_id)
        
        # Store full message data for details dialog
        self.message_data = {
            'sender_name': sender_name,
            'sender_role': sender_role,
            'recipient_name': recipient_name,
            'recipient_role': recipient_role,
            'category': category,
            'subject': subject,
            'body': body,
            'created_at': created_at
        }
        
        self.init_ui(sender_name, recipient_name, category, subject, body, created_at)
    
    def init_ui(self, sender_name, recipient_name, category, subject, body, created_at):
        self.setFixedHeight(70)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Different styling for sent vs received
        if self.is_sent:
            bg_color = "#f0fdf4" if self.is_read else "#f0fdf4"
            indicator_color = "#10b981"
        else:
            bg_color = "#ffffff" if self.is_read else "#eff6ff"
            indicator_color = STYLE_BLUE if not self.is_read else "#d1d5db"
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: none;
                border-bottom: 1px solid #f3f4f6;
            }}
            QFrame:hover {{
                background-color: #f9fafb;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(15)
        
        # Unread/Sent indicator
        indicator = QLabel("●" if not self.is_read and not self.is_sent else "")
        indicator.setStyleSheet(f"color: {indicator_color}; font-size: 16px; border: none;")
        indicator.setFixedWidth(20)
        layout.addWidget(indicator)
        
        # From/To label
        contact_name = recipient_name if self.is_sent else sender_name
        contact_prefix = "To: " if self.is_sent else ""
        contact_label = QLabel(contact_prefix + (contact_name or "Unknown"))
        contact_label.setFont(QFont("Arial", 12, QFont.Weight.Bold if not self.is_read else QFont.Weight.Normal))
        contact_label.setStyleSheet(f"color: {STYLE_NAVY}; border: none;")
        contact_label.setFixedWidth(200)
        layout.addWidget(contact_label)
        
        # Category badge (small)
        category_badge = QLabel(category or "General")
        category_colors = {
            'General': ('#dbeafe', '#1e40af'),
            'Purchase Order': ('#dbeafe', '#1e40af'),
            'Inventory Alert': ('#fef3c7', '#92400e'),
            'Stock Request': ('#d1fae5', '#065f46'),
            'Damage Report': ('#fee2e2', '#991b1b'),
            'Urgent': ('#fecaca', '#7f1d1d')
        }
        bg, text_color = category_colors.get(category or 'General', ('#dbeafe', '#1e40af'))
        category_badge.setStyleSheet(f"""
            background-color: {bg};
            color: {text_color};
            border: none;
            border-radius: 8px;
            padding: 2px 8px;
            font-size: 9px;
            font-weight: bold;
        """)
        category_badge.setFixedHeight(18)
        layout.addWidget(category_badge)
        
        # Subject and body preview
        preview_text = f"{subject or 'No Subject'} - {body[:50] if body else ''}..."
        preview_label = QLabel(preview_text)
        preview_label.setFont(QFont("Arial", 11))
        preview_label.setStyleSheet("color: #6b7280; border: none;")
        preview_label.setWordWrap(False)
        layout.addWidget(preview_label, 1)
        
        # Date
        if created_at:
            if isinstance(created_at, str):
                date_str = created_at.split(' ')[0]  # Just show date
            else:
                date_str = created_at.strftime('%m/%d/%y')
        else:
            date_str = ""
        
        date_label = QLabel(date_str)
        date_label.setStyleSheet("color: #9ca3af; font-size: 11px; border: none;")
        date_label.setFixedWidth(80)
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(date_label)
        
        # Delete button (small)
        delete_btn = QPushButton("🗑")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #9ca3af;
            }
            QPushButton:hover {
                color: #ef4444;
            }
        """)
        delete_btn.clicked.connect(lambda: self.on_delete(self.message_id))
        layout.addWidget(delete_btn)
    
    def mousePressEvent(self, event):
        """Open message details when clicked."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.show_message_details()
        super().mousePressEvent(event)
    
    def show_message_details(self):
        """Show full message details in a dialog."""
        dialog = MessageDetailsDialog(
            self.message_data,
            self.is_sent,
            self
        )
        dialog.exec()


class MessageDetailsDialog(QDialog):
    """Modern, clean message details dialog."""
    
    def __init__(self, message_data, is_sent, parent=None):
        super().__init__(parent)
        self.message_data = message_data
        self.is_sent = is_sent
        self.setWindowTitle("Message Details")
        self.setMinimumSize(600, 550)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Clean white background
        self.setStyleSheet("QDialog { background-color: white; }")
        
        # Subject header
        subject_label = QLabel(self.message_data.get('subject', 'No Subject'))
        subject_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        subject_label.setStyleSheet(f"color: {STYLE_NAVY}; border: none;")
        subject_label.setWordWrap(True)
        layout.addWidget(subject_label)
        
        # Category badge
        category = self.message_data.get('category', 'General')
        category_container = QHBoxLayout()
        category_badge = QLabel(category)
        category_colors = {
            'General': ('#dbeafe', '#1e40af'),
            'Purchase Order': ('#e0e7ff', '#4338ca'),
            'Inventory Alert': ('#fef3c7', '#92400e'),
            'Stock Request': ('#d1fae5', '#065f46'),
            'Damage Report': ('#fee2e2', '#991b1b'),
            'Urgent': ('#fecaca', '#7f1d1d')
        }
        bg, text_color = category_colors.get(category, ('#dbeafe', '#1e40af'))
        category_badge.setStyleSheet(f"""
            background-color: {bg};
            color: {text_color};
            border: none;
            border-radius: 12px;
            padding: 6px 14px;
            font-size: 11px;
            font-weight: bold;
        """)
        category_badge.setFixedWidth(category_badge.sizeHint().width() + 10)
        category_container.addWidget(category_badge)
        category_container.addStretch()
        layout.addLayout(category_container)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {STYLE_BORDER}; max-height: 1px; border: none;")
        layout.addWidget(separator)
        
        # From/To and Date info in a clean row
        info_layout = QHBoxLayout()
        info_layout.setSpacing(20)
        
        # Left side - From/To
        if self.is_sent:
            contact_text = f"<b>To:</b> {self.message_data.get('recipient_name', 'Unknown')}"
            role_text = self.message_data.get('recipient_role', 'User')
        else:
            contact_text = f"<b>From:</b> {self.message_data.get('sender_name', 'Unknown')}"
            role_text = self.message_data.get('sender_role', 'User')
        
        contact_info = QVBoxLayout()
        contact_label = QLabel(contact_text)
        contact_label.setStyleSheet(f"color: {STYLE_NAVY}; font-size: 13px; border: none;")
        contact_info.addWidget(contact_label)
        
        role_label = QLabel(role_text)
        role_label.setStyleSheet("color: #9ca3af; font-size: 12px; border: none;")
        contact_info.addWidget(role_label)
        
        info_layout.addLayout(contact_info)
        info_layout.addStretch()
        
        # Right side - Date
        created_at = self.message_data.get('created_at')
        if created_at:
            if isinstance(created_at, str):
                date_str = created_at
            else:
                date_str = created_at.strftime('%B %d, %Y at %I:%M %p')
        else:
            date_str = "Unknown date"
        
        date_label = QLabel(date_str)
        date_label.setStyleSheet("color: #6b7280; font-size: 12px; border: none;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        info_layout.addWidget(date_label)
        
        layout.addLayout(info_layout)
        
        # Message body in a clean container
        body_container = QFrame()
        body_container.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_BG_LIGHT};
                border-radius: 12px;
                padding: 20px;
                border: 1px solid {STYLE_BORDER};
            }}
        """)
        body_layout = QVBoxLayout(body_container)
        
        body_text = QTextEdit()
        body_text.setPlainText(self.message_data.get('body', 'No message content'))
        body_text.setReadOnly(True)
        body_text.setStyleSheet(f"""
            QTextEdit {{
                border: none;
                background-color: transparent;
                color: {STYLE_NAVY};
                font-size: 14px;
                line-height: 1.6;
            }}
        """)
        body_layout.addWidget(body_text)
        
        layout.addWidget(body_container, 1)
        
        # Close button at bottom
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(120, 45)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_BLUE};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #004494;
            }}
        """)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)


class MessagesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # Action Buttons Row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        self.btn_compose = QPushButton("✉️  COMPOSE")

        # Style for Compose button
        self.btn_compose.setFixedHeight(50)
        self.btn_compose.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_compose.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_BLUE}; 
                border: none;
                border-radius: 8px; 
                font-weight: 700; 
                font-size: 13px;
                color: white; 
                padding: 0 30px;
            }}
            QPushButton:hover {{ 
                background-color: #004494; 
            }}
        """)
        
        actions_layout.addWidget(self.btn_compose)
        actions_layout.addStretch()
        self.layout.addLayout(actions_layout)

        # Messages List Container
        messages_container = QFrame()
        messages_container.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                border-radius: 8px;
            }}
        """)
        messages_layout = QVBoxLayout(messages_container)
        messages_layout.setContentsMargins(0, 0, 0, 0)
        messages_layout.setSpacing(0)

        # Scroll Area for Messages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: white;
            }}
            QScrollBar:vertical {{
                border: none;
                background: #f9fafb;
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background: #d1d5db;
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #9ca3af;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Widget to hold message items
        self.messages_widget = QWidget()
        self.messages_widget.setStyleSheet("QWidget { background-color: white; }")
        self.messages_list_layout = QVBoxLayout(self.messages_widget)
        self.messages_list_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_list_layout.setSpacing(0)
        
        # Empty state message
        # self.empty_state = QLabel("📭\n\nNo messages yet\n\nClick 'COMPOSE' to send your first message")
        # self.empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.empty_state.setStyleSheet(f"""
        #     QLabel {{
        #         color: #9ca3af;
        #         font-size: 14px;
        #         padding: 60px;
        #         background-color: transparent;
        #         border: none;
        #     }}
        # """)
        # self.messages_list_layout.addWidget(self.empty_state)
        
        self.messages_list_layout.addStretch()
        
        scroll.setWidget(self.messages_widget)
        messages_layout.addWidget(scroll)
        
        self.layout.addWidget(messages_container)

    def add_message(self, message_id, sender_id, recipient_id, current_user_id, sender_name, sender_role, recipient_name, recipient_role, category, subject, body, is_read, created_at):
        """Add a new message to the list."""
        # Hide empty state when messages exist
        # if self.empty_state.isVisible():
        #     self.empty_state.setVisible(False)
        
        message_item = MessageItem(message_id, sender_id, recipient_id, current_user_id, sender_name, sender_role, recipient_name, recipient_role, category, subject, body, is_read, created_at, self.delete_message)
        # Insert before the stretch
        self.messages_list_layout.insertWidget(self.messages_list_layout.count() - 1, message_item)
        self.messages.append(message_item)
    
    def clear_messages(self):
        """Clear all messages from the list."""
        for message in self.messages:
            message.deleteLater()
        self.messages.clear()
        # Show empty state when no messages
        # self.empty_state.setVisible(True)
    
    def delete_message(self, message_id):
        """Remove a message from the list."""
        # This will be connected to controller
        pass
    
    def populate_messages(self, messages_data):
        """Populate the messages list with data."""
        self.clear_messages()
        for msg in messages_data:
            self.add_message(
                msg.get('id'),
                msg.get('sender_id'),
                msg.get('recipient_id'),
                msg.get('current_user_id'),
                msg.get('sender_name'),
                msg.get('sender_role'),
                msg.get('recipient_name'),
                msg.get('recipient_role'),
                msg.get('category'),
                msg.get('title'),
                msg.get('body'),
                msg.get('is_read'),
                msg.get('created_at')
            )
