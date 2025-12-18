from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPixmap

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STASH - Hotel Management System")
        # Make window maximized (windowed fullscreen)
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        # 1. Main Background - Simple Light Theme
        self.setObjectName("MainPage")
        self.setStyleSheet("""
            #MainPage {
                background-color: #f4f7f9;
            }
        """)

        # 2. Layout to center the login card
        main_layout = QHBoxLayout(self)
        main_layout.addStretch(1)

        v_center_layout = QVBoxLayout()
        v_center_layout.addStretch(1)

        # 3. The Login Card
        login_card = QFrame()
        login_card.setObjectName("LoginCard")
        login_card.setFixedSize(400, 520) 
        login_card.setStyleSheet("""
            #LoginCard {
                background-color: white;
                border: 1px solid #e1e4e8;
                border-radius: 8px;
            }
            QLabel { 
                color: #2c3e50; 
                font-family: 'Segoe UI', Arial; 
            }
            QLineEdit {
                border: 1px solid #dcdfe6;
                border-radius: 4px;
                padding: 12px;
                font-size: 14px;
                background: #ffffff;
                color: #000000;
            }
            QLineEdit:focus {
                border: 1.5px solid #0056b3;
                color: #000000;
            }
            QPushButton#LoginBtn {
                background-color: #0056b3;
                color: white;
                border-radius: 4px;
                padding: 12px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton#LoginBtn:hover {
                background-color: #004494;
            }
            QPushButton#ForgotBtn {
                border: none;
                color: #5a6268;
                font-size: 12px;
                background: transparent;
            }
            QPushButton#ForgotBtn:hover {
                color: #0056b3;
                text-decoration: underline;
            }
        """)

        # Soft Shadow for a modern look
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        login_card.setGraphicsEffect(shadow)

        # 4. Elements inside the Card
        card_content = QVBoxLayout(login_card)
        card_content.setContentsMargins(40, 40, 40, 40)
        card_content.setSpacing(12)

        # Logo Section
        logo_label = QLabel()
        # Ensure your high-def logo is saved as assets/logo.png
        pixmap = QPixmap("assets/logo_taskbar.png")
        scaled_pixmap = pixmap.scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio, 
                                     Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        # logo_label.setFixedSize(180, 180)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_label = QLabel("Welcome!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        welcome_label.setStyleSheet("margin-top: 10px; margin-bottom: 20px;")

        # Input Fields
        email_label = QLabel("Company E-mail")
        email_label.setFont(QFont("Segoe UI", 10))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")

        pass_label = QLabel("Password")
        pass_label.setFont(QFont("Segoe UI", 10))
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Buttons
        login_btn = QPushButton("Login")
        login_btn.setObjectName("LoginBtn")
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.setObjectName("ForgotBtn")
        forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Add widgets to layout
        card_content.addWidget(logo_label)
        card_content.addWidget(welcome_label)
        card_content.addWidget(email_label)
        card_content.addWidget(self.email_input)
        card_content.addWidget(pass_label)
        card_content.addWidget(self.pass_input)
        card_content.addSpacing(10)
        card_content.addWidget(login_btn)
        card_content.addWidget(forgot_btn)
        card_content.addStretch()

        # Final assembly
        v_center_layout.addWidget(login_card)
        v_center_layout.addStretch(1)
        main_layout.addLayout(v_center_layout)
        main_layout.addStretch(1)

    # Added a method for the controller to connect to
    def get_login_data(self):
        return self.email_input.text(), self.pass_input.text()