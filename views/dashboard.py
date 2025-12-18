from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from views.purchase_view import PurchasePage
from views.inventory import InventoryPage
from views.reports import ReportsPage
from views.messages import MessagesPage
from controllers.purchase_controller import PurchaseController
from controllers.inventory_controller import InventoryController
from controllers.reports_controller import ReportsController
from controllers.messages_controller import MessagesController
from models import purchase as purchase_model

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STASH - Hotel Management System")
        self.setMinimumSize(1200, 800)
        self.current_user = None  # Store logged-in user name
        self.init_ui()

    def init_ui(self):
        # 1. Base Setup
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainDashboard")
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet("#MainDashboard { background-color: #f0f2f5; }")

        # 2. SIDEBAR Setup
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            QFrame { background-color: white; border-right: 1px solid #d1d5db; }
            QPushButton {
                background-color: transparent; border: none; color: #4b5563;
                padding: 12px 20px; text-align: left; font-size: 12px;
                font-weight: 600; border-radius: 2px; margin: 2px 10px;
            }
            QPushButton:hover { background-color: #f3f4f6; color: #111827; }
            QPushButton#ActiveNav { background-color: #0056b3; color: white; }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        
        profile_container = QFrame()
        profile_lay = QVBoxLayout(profile_container)
        self.name_lbl = QLabel("USER_ADMIN")
        self.name_lbl.setStyleSheet("color: #111827; font-size: 15px; font-weight: 700; border:none;")
        self.role_lbl = QLabel("Purchase Manager")
        self.role_lbl.setStyleSheet("color: #0056b3; font-size: 11px; font-weight: 600; border:none;")
        profile_lay.addWidget(self.name_lbl)
        profile_lay.addWidget(self.role_lbl)
        sidebar_layout.addWidget(profile_container)

        self.nav_btns = {}
        for text in ["DASHBOARD", "PURCHASE", "INVENTORY", "REPORTS", "MESSAGES"]:
            btn = QPushButton(text)
            if text == "DASHBOARD": btn.setObjectName("ActiveNav")
            sidebar_layout.addWidget(btn)
            self.nav_btns[text] = btn

        sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

        # 3. CONTENT AREA Setup
        content_container = QWidget()
        content_main_layout = QVBoxLayout(content_container)
        content_main_layout.setContentsMargins(25, 25, 25, 25)
        content_main_layout.setSpacing(20)

        # Title Bar
        self.title_bar = QFrame()
        self.title_bar.setObjectName("TitleBar")
        self.title_bar.setFixedHeight(80)
        self.title_bar.setStyleSheet("#TitleBar { background-color: white; border: 1px solid #d1d5db; border-radius: 2px; }")
        
        title_lay = QHBoxLayout(self.title_bar)
        self.title_label = QLabel("DASHBOARD")
        self.title_label.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        self.title_label.setStyleSheet("border: none; color: #111827;")
        title_lay.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        content_main_layout.addWidget(self.title_bar)

        # 4. THE STACKED WIDGET (Created here FIRST)
        self.main_stack = QStackedWidget()
        
        # PAGE 1: DASHBOARD
        self.dash_page = QWidget()
        dash_page_layout = QVBoxLayout(self.dash_page)
        dash_page_layout.setContentsMargins(0, 0, 0, 0)
        dash_page_layout.setSpacing(20)

        kpi_row_layout = QHBoxLayout()
        kpi_row_layout.setSpacing(20)
        kpi_items = [("INVENTORY VALUE", "₱ 0.00"), ("LOW STOCK ALERT", "0"), ("INVENTORY ITEMS", "0")]
        for title, val in kpi_items:
            card = QFrame()
            card.setFixedHeight(150)
            card.setStyleSheet("background-color: white; border: 1px solid #d1d5db; border-radius: 2px;")
            card_lay = QVBoxLayout(card)
            v_lbl = QLabel(val)
            v_lbl.setFont(QFont("Inter", 28, QFont.Weight.Bold))
            v_lbl.setStyleSheet("border:none; color: #111827;")
            v_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("border:none; color: #6b7280; font-size: 11px; font-weight: 700;")
            t_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_lay.addWidget(v_lbl)
            card_lay.addWidget(t_lbl)
            kpi_row_layout.addWidget(card)
        dash_page_layout.addLayout(kpi_row_layout)
        
        self.chart_canvas = QFrame()
        self.chart_canvas.setStyleSheet("background-color: transparent; border: 1px dashed #d1d5db; border-radius: 2px;")
        dash_page_layout.addWidget(self.chart_canvas)
        dash_page_layout.setStretch(1, 1)

        # PAGE 2: PURCHASE (Initialized and added AFTER self.main_stack exists)
        self.purchase_page = PurchasePage()
        
        # PAGE 3: INVENTORY
        self.inventory_page = InventoryPage()
        
        # PAGE 4: REPORTS
        self.reports_page = ReportsPage()
        
        # PAGE 5: MESSAGES
        self.messages_page = MessagesPage()
        
        # 5. Logic & Controllers (Initialized now that views exist)
        self.p_model = purchase_model.PurchaseModel()
        self.m_model = purchase_model.MessageModel()
        self.purchase_ctrl = PurchaseController(self.purchase_page, self.p_model, self)
        self.inventory_ctrl = InventoryController(self.inventory_page, self.p_model)
        self.reports_ctrl = ReportsController(self.reports_page, self.p_model)
        self.messages_ctrl = MessagesController(self.messages_page, self.m_model, self)

        # 6. Assemble Stack
        self.main_stack.addWidget(self.dash_page)     # Index 0
        self.main_stack.addWidget(self.purchase_page) # Index 1
        self.main_stack.addWidget(self.inventory_page) # Index 2
        self.main_stack.addWidget(self.reports_page)  # Index 3
        self.main_stack.addWidget(self.messages_page)  # Index 4

        content_main_layout.addWidget(self.main_stack)
        self.main_layout.addWidget(content_container)

        # 7. Connect Navigation
        self.nav_btns["DASHBOARD"].clicked.connect(lambda: self.switch_page(0, "DASHBOARD"))
        self.nav_btns["PURCHASE"].clicked.connect(lambda: self.switch_page(1, "PURCHASE"))
        self.nav_btns["INVENTORY"].clicked.connect(lambda: self.switch_page(2, "INVENTORY"))
        self.nav_btns["REPORTS"].clicked.connect(lambda: self.switch_page(3, "REPORTS"))
        self.nav_btns["MESSAGES"].clicked.connect(lambda: self.switch_page(4, "MESSAGES"))

    def switch_page(self, index, title):
        self.main_stack.setCurrentIndex(index)
        self.title_label.setText(title)
        
        # Update sidebar styling
        for name, btn in self.nav_btns.items():
            btn.setObjectName("ActiveNav" if name == title else "")
            btn.style().unpolish(btn)
            btn.style().polish(btn)