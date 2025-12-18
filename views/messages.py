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
        self.setWindowTitle("COMPOSE MESSAGE")
        self.setMinimumSize(600, 550)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.setStyleSheet("QDialog { background-color: white; }")

        # Title
        title = QLabel("COMPOSE NEW MESSAGE")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {STYLE_NAVY}; padding-bottom: 10px; border-bottom: 2px solid {STYLE_BORDER};")
        layout.addWidget(title)

        # Recipient
        to_label = QLabel("TO:")
        to_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        layout.addWidget(to_label)
        
        self.to_input = QComboBox()
        self.to_input.setPlaceholderText("Select recipient...")
        self.to_input.setFixedHeight(40)
        self.to_input.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QComboBox:focus {{ border-color: {STYLE_BLUE}; }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        layout.addWidget(self.to_input)
        
        # Category
        category_label = QLabel("CATEGORY:")
        category_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        layout.addWidget(category_label)
        
        self.category_input = QComboBox()
        self.category_input.addItems([
            "General",
            "Purchase Order",
            "Inventory Alert",
            "Stock Request",
            "Damage Report",
            "Urgent"
        ])
        self.category_input.setFixedHeight(40)
        self.category_input.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QComboBox:focus {{ border-color: {STYLE_BLUE}; }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        layout.addWidget(self.category_input)

        # Subject
        subject_label = QLabel("SUBJECT:")
        subject_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        layout.addWidget(subject_label)
        
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Enter message subject...")
        self.subject_input.setFixedHeight(40)
        self.subject_input.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QLineEdit:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        layout.addWidget(self.subject_input)

        # Message Body
        body_label = QLabel("MESSAGE:")
        body_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        layout.addWidget(body_label)
        
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Enter your message here...")
        self.body_input.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 10px;
                background-color: white;
                color: {STYLE_NAVY};
                font-size: 13px;
            }}
            QTextEdit:focus {{ border-color: {STYLE_BLUE}; }}
        """)
        layout.addWidget(self.body_input)

        # Buttons
        button_row = QHBoxLayout()
        button_row.addStretch()
        
        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.setFixedSize(100, 40)
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {STYLE_BORDER};
                color: #6b7280;
                font-weight: bold;
                border-radius: 4px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BG_LIGHT}; }}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.send_btn = QPushButton("SEND")
        self.send_btn.setFixedSize(120, 40)
        self.send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_BLUE};
                color: white;
                border: none;
                font-weight: bold;
                border-radius: 4px;
            }}
            QPushButton:hover {{ background-color: #004494; }}
        """)
        self.send_btn.clicked.connect(self.accept)
        
        button_row.addWidget(self.cancel_btn)
        button_row.addWidget(self.send_btn)
        layout.addLayout(button_row)

    def get_data(self):
        """Return the message data."""
        return {
            'subject': self.subject_input.text(),
            'body': self.body_input.toPlainText()
        }


class MessageItem(QFrame):
    """Individual message item widget."""
    
    def __init__(self, message_id, sender_name, sender_role, category, subject, body, is_read, created_at, on_delete, parent=None):
        super().__init__(parent)
        self.message_id = message_id
        self.on_delete = on_delete
        self.is_read = is_read
        self.init_ui(sender_name, sender_role, category, subject, body, created_at)
    
    def init_ui(self, sender_name, sender_role, category, subject, body, created_at):
        self.setFixedHeight(100)
        
        # Different background for read/unread
        bg_color = "white" if self.is_read else STYLE_BG_LIGHT
        border_color = STYLE_BORDER if self.is_read else STYLE_BLUE
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-left: 4px solid {border_color};
                border-top: 1px solid {STYLE_BORDER};
                border-right: 1px solid {STYLE_BORDER};
                border-bottom: 1px solid {STYLE_BORDER};
                border-radius: 4px;
            }}
            QFrame:hover {{
                background-color: {STYLE_BG_LIGHT};
                border-left-color: {STYLE_BLUE};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)
        
        # Message content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)
        
        # Header row: Sender + Category
        header_layout = QHBoxLayout()
        
        # Sender name and role
        sender_label = QLabel(f"{sender_name or 'Unknown'} • {sender_role or 'User'}")
        sender_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        sender_label.setStyleSheet(f"color: {STYLE_BLUE}; border: none;")
        header_layout.addWidget(sender_label)
        
        # Category badge
        category_badge = QLabel(category or "General")
        category_badge.setStyleSheet(f"""
            background-color: #e0e7ff;
            color: #4338ca;
            border: none;
            border-radius: 10px;
            padding: 2px 10px;
            font-size: 9px;
            font-weight: bold;
        """)
        category_badge.setFixedHeight(20)
        header_layout.addWidget(category_badge)
        header_layout.addStretch()
        
        content_layout.addLayout(header_layout)
        
        # Subject
        subject_label = QLabel(subject or "No Subject")
        subject_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        subject_label.setStyleSheet(f"color: {STYLE_NAVY}; border: none;")
        content_layout.addWidget(subject_label)
        
        # Body preview (truncated)
        body_preview = body[:100] + "..." if len(body) > 100 else body
        body_label = QLabel(body_preview)
        body_label.setStyleSheet(f"color: #6b7280; font-size: 11px; border: none;")
        content_layout.addWidget(body_label)
        
        # Date - convert to string if datetime object
        if created_at:
            if isinstance(created_at, str):
                date_str = created_at
            else:
                # It's a datetime object
                date_str = created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_str = "Unknown date"
        
        date_label = QLabel(date_str)
        date_label.setStyleSheet(f"color: #9ca3af; font-size: 10px; border: none;")
        content_layout.addWidget(date_label)
        
        layout.addLayout(content_layout, 1)
        
        # Delete button
        delete_btn = QPushButton()
        delete_btn.setFixedSize(35, 35)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {STYLE_BORDER};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #fee2e2;
                border-color: #ef4444;
            }}
        """)
        
        # Create trash icon
        icon = self.create_delete_icon()
        delete_btn.setIcon(icon)
        delete_btn.setIconSize(delete_btn.size() * 0.6)
        delete_btn.clicked.connect(lambda: self.on_delete(self.message_id))
        
        layout.addWidget(delete_btn)
    
    def create_delete_icon(self):
        """Create a trash can icon."""
        from PyQt6.QtGui import QIcon, QPixmap
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw trash can
        painter.setPen(QColor("#ef4444"))
        painter.setBrush(QColor("#ef4444"))
        
        # Lid
        painter.drawRect(8, 8, 16, 2)
        # Body
        painter.drawRect(10, 10, 12, 14)
        # Lines
        painter.setPen(QColor("#ffffff"))
        painter.drawLine(14, 12, 14, 22)
        painter.drawLine(18, 12, 18, 22)
        
        painter.end()
        return QIcon(pixmap)


class MessagesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # Header with Title
        header_layout = QHBoxLayout()
        
        title = QLabel("MESSAGES")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY};")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.layout.addLayout(header_layout)

        # Action Buttons Row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        self.btn_compose = QPushButton("COMPOSE")
        self.btn_sort = QPushButton("SORT")
        self.btn_archive = QPushButton("ARCHIVE")

        self.actions = [self.btn_compose, self.btn_sort, self.btn_archive]
        for btn in self.actions:
            btn.setFixedHeight(45)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: white; 
                    border: 1px solid {STYLE_BORDER};
                    border-radius: 2px; 
                    font-weight: 700; 
                    font-size: 10px;
                    color: #374151; 
                    letter-spacing: 1px;
                }}
                QPushButton:hover {{ 
                    background-color: {STYLE_BG_LIGHT}; 
                    border-color: {STYLE_BLUE}; 
                    color: {STYLE_BLUE}; 
                }}
            """)
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        self.layout.addLayout(actions_layout)

        # Messages List Container
        messages_container = QFrame()
        messages_container.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {STYLE_BORDER};
                border-radius: 4px;
            }}
        """)
        messages_layout = QVBoxLayout(messages_container)
        messages_layout.setContentsMargins(15, 15, 15, 15)
        messages_layout.setSpacing(10)

        # Scroll Area for Messages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f2f5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9ca3af;
            }
        """)
        
        # Widget to hold message items
        self.messages_widget = QWidget()
        self.messages_list_layout = QVBoxLayout(self.messages_widget)
        self.messages_list_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_list_layout.setSpacing(10)
        self.messages_list_layout.addStretch()
        
        scroll.setWidget(self.messages_widget)
        messages_layout.addWidget(scroll)
        
        self.layout.addWidget(messages_container)

    def add_message(self, message_id, sender_name, sender_role, category, subject, body, is_read, created_at):
        """Add a new message to the list."""
        message_item = MessageItem(message_id, sender_name, sender_role, category, subject, body, is_read, created_at, self.delete_message)
        # Insert before the stretch
        self.messages_list_layout.insertWidget(self.messages_list_layout.count() - 1, message_item)
        self.messages.append(message_item)
    
    def clear_messages(self):
        """Clear all messages from the list."""
        for message in self.messages:
            message.deleteLater()
        self.messages.clear()
    
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
                msg.get('sender_name'),
                msg.get('sender_role'),
                msg.get('category'),
                msg.get('title'),
                msg.get('body'),
                msg.get('is_read'),
                msg.get('created_at')
            )
