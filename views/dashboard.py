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
    # Define role-based access control
    ROLE_PAGES = {
        'Purchase Admin': ['DASHBOARD', 'PURCHASE', 'INVENTORY', 'REPORTS', 'MESSAGES'],
        'Owner': ['DASHBOARD', 'TRANS HISTORY', 'DEPT OVERVIEW', 'REPORTS', 'MESSAGES'],
        'Department Manager': ['DASHBOARD', 'PURCHASE', 'INVENTORY', 'MESSAGES']
    }
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STASH - Hotel Management System")
        self.setMinimumSize(1200, 800)
        self.current_user = None  # Store logged-in user name
        self.current_role = None  # Store logged-in user role
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
        sidebar_layout.setSpacing(5)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        
        # Welcome message
        welcome_label = QLabel("Welcome back!")
        welcome_label.setStyleSheet("color: #6b7280; font-size: 11px; font-weight: 600; border:none; padding: 0 20px;")
        sidebar_layout.addWidget(welcome_label)
        
        # Profile container
        profile_container = QFrame()
        profile_container.setStyleSheet("background-color: transparent; border: none; padding: 10px 20px;")
        profile_lay = QHBoxLayout(profile_container)
        profile_lay.setSpacing(12)
        
        # Profile icon (circle with initial)
        profile_icon = QLabel("👤")
        profile_icon.setFixedSize(50, 50)
        profile_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_icon.setStyleSheet("""
            background-color: #e5e7eb;
            border-radius: 25px;
            font-size: 24px;
            border: none;
        """)
        profile_lay.addWidget(profile_icon)
        
        # Name and role
        name_role_container = QVBoxLayout()
        name_role_container.setSpacing(2)
        self.name_lbl = QLabel("Director Name")
        self.name_lbl.setStyleSheet("color: #111827; font-size: 14px; font-weight: 700; border:none;")
        self.role_lbl = QLabel("Director")
        self.role_lbl.setStyleSheet("color: #6b7280; font-size: 11px; font-weight: 500; border:none;")
        name_role_container.addWidget(self.name_lbl)
        name_role_container.addWidget(self.role_lbl)
        profile_lay.addLayout(name_role_container)
        profile_lay.addStretch()
        
        sidebar_layout.addWidget(profile_container)
        
        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setStyleSheet("background-color: #e5e7eb; max-height: 1px; border: none; margin: 10px 15px;")
        sidebar_layout.addWidget(separator1)

        self.nav_btns = {}
        nav_pages = ["DASHBOARD", "TRANS HISTORY", "DEPT OVERVIEW", "PURCHASE", "INVENTORY", "REPORTS", "MESSAGES"]
        for text in nav_pages:
            btn = QPushButton(text)
            if text == "DASHBOARD": btn.setObjectName("ActiveNav")
            sidebar_layout.addWidget(btn)
            self.nav_btns[text] = btn
        
        # Separator before notifications
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("background-color: #e5e7eb; max-height: 1px; border: none; margin: 10px 15px;")
        sidebar_layout.addWidget(separator2)
        
        # Notifications section
        notifications_header = QLabel("Notifications")
        notifications_header.setStyleSheet("color: #111827; font-size: 12px; font-weight: 700; border:none; padding: 10px 20px 5px 20px;")
        sidebar_layout.addWidget(notifications_header)
        
        # Notification items container with scroll
        from PyQt6.QtWidgets import QScrollArea
        notifications_scroll = QScrollArea()
        notifications_scroll.setWidgetResizable(True)
        notifications_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f3f4f6;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db;
                border-radius: 3px;
                min-height: 20px;
            }
        """)
        
        notifications_widget = QWidget()
        notifications_widget.setStyleSheet("background-color: transparent; border: none;")
        notifications_layout = QVBoxLayout(notifications_widget)
        notifications_layout.setContentsMargins(10, 0, 10, 0)
        notifications_layout.setSpacing(5)
        
        # Add placeholder notifications (these will be populated dynamically)
        self.notifications_layout = notifications_layout
        notifications_layout.addStretch()
        
        notifications_scroll.setWidget(notifications_widget)
        sidebar_layout.addWidget(notifications_scroll)

        sidebar_layout.addStretch()
        
        # Logout Button
        self.logout_btn = QPushButton("LOGOUT")
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                padding: 12px 20px;
                text-align: center;
                font-size: 12px;
                font-weight: 700;
                border-radius: 4px;
                margin: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        sidebar_layout.addWidget(self.logout_btn)
        
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

        # KPI Cards in 2x2 grid
        kpi_grid_layout = QVBoxLayout()
        kpi_grid_layout.setSpacing(20)
        
        # First row
        kpi_row1_layout = QHBoxLayout()
        kpi_row1_layout.setSpacing(20)
        
        # Inventory Value Card
        inv_value_card, self.inventory_value_label = self._create_kpi_card("0", "Inventory Value")
        kpi_row1_layout.addWidget(inv_value_card)
        
        # Wastages Card
        wastages_card, self.wastages_label = self._create_kpi_card("0", "Wastages")
        kpi_row1_layout.addWidget(wastages_card)
        
        kpi_grid_layout.addLayout(kpi_row1_layout)
        
        # Second row
        kpi_row2_layout = QHBoxLayout()
        kpi_row2_layout.setSpacing(20)
        
        # Inventory Items Card
        inv_items_card, self.inventory_items_label = self._create_kpi_card("0", "Inventory Items")
        kpi_row2_layout.addWidget(inv_items_card)
        
        # Low Stocks Card
        low_stocks_card, self.low_stocks_label = self._create_kpi_card("0", "Low Stocks")
        kpi_row2_layout.addWidget(low_stocks_card)
        
        kpi_grid_layout.addLayout(kpi_row2_layout)
        
        dash_page_layout.addLayout(kpi_grid_layout)
        dash_page_layout.addStretch()

        # PAGE 2: TRANS HISTORY (Transaction History)
        self.trans_history_page = QWidget()
        trans_history_layout = QVBoxLayout(self.trans_history_page)
        trans_history_layout.setContentsMargins(20, 20, 20, 20)
        trans_history_label = QLabel("Transaction History - Coming Soon")
        trans_history_label.setFont(QFont("Arial", 18))
        trans_history_label.setStyleSheet("color: #6b7280;")
        trans_history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trans_history_layout.addWidget(trans_history_label)
        
        # PAGE 3: DEPT OVERVIEW (Department Overview)
        self.dept_overview_page = QWidget()
        dept_overview_layout = QVBoxLayout(self.dept_overview_page)
        dept_overview_layout.setContentsMargins(20, 20, 20, 20)
        dept_overview_label = QLabel("Department Overview - Coming Soon")
        dept_overview_label.setFont(QFont("Arial", 18))
        dept_overview_label.setStyleSheet("color: #6b7280;")
        dept_overview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dept_overview_layout.addWidget(dept_overview_label)
        
        # PAGE 4: PURCHASE (Initialized and added AFTER self.main_stack exists)
        self.purchase_page = PurchasePage()
        
        # PAGE 5: INVENTORY
        self.inventory_page = InventoryPage()
        
        # PAGE 6: REPORTS
        self.reports_page = ReportsPage()
        
        # PAGE 7: MESSAGES
        self.messages_page = MessagesPage()
        
        # 5. Logic & Controllers (Initialized now that views exist)
        self.p_model = purchase_model.PurchaseModel()
        self.m_model = purchase_model.MessageModel()
        self.purchase_ctrl = PurchaseController(self.purchase_page, self.p_model, self)
        self.inventory_ctrl = InventoryController(self.inventory_page, self.p_model)
        self.reports_ctrl = ReportsController(self.reports_page, self.p_model)
        self.messages_ctrl = MessagesController(self.messages_page, self.m_model, self)

        # 6. Assemble Stack
        self.main_stack.addWidget(self.dash_page)          # Index 0
        self.main_stack.addWidget(self.trans_history_page) # Index 1
        self.main_stack.addWidget(self.dept_overview_page) # Index 2
        self.main_stack.addWidget(self.purchase_page)      # Index 3
        self.main_stack.addWidget(self.inventory_page)     # Index 4
        self.main_stack.addWidget(self.reports_page)       # Index 5
        self.main_stack.addWidget(self.messages_page)      # Index 6

        content_main_layout.addWidget(self.main_stack)
        self.main_layout.addWidget(content_container)

        # 7. Connect Navigation
        self.nav_btns["DASHBOARD"].clicked.connect(lambda: self.switch_page(0, "DASHBOARD"))
        self.nav_btns["TRANS HISTORY"].clicked.connect(lambda: self.switch_page(1, "TRANS HISTORY"))
        self.nav_btns["DEPT OVERVIEW"].clicked.connect(lambda: self.switch_page(2, "DEPT OVERVIEW"))
        self.nav_btns["PURCHASE"].clicked.connect(lambda: self.switch_page(3, "PURCHASE"))
        self.nav_btns["INVENTORY"].clicked.connect(lambda: self.switch_page(4, "INVENTORY"))
        self.nav_btns["REPORTS"].clicked.connect(lambda: self.switch_page(5, "REPORTS"))
        self.nav_btns["MESSAGES"].clicked.connect(lambda: self.switch_page(6, "MESSAGES"))
        
        # Connect Logout
        self.logout_btn.clicked.connect(self.handle_logout)

    def update_ui_for_role(self, user_name, user_role):
        """Update UI based on user role - show/hide navigation buttons."""
        self.current_user = user_name
        self.current_role = user_role
        
        # Update profile labels
        self.name_lbl.setText(user_name)
        self.role_lbl.setText(user_role)
        
        # Get allowed pages for this role
        allowed_pages = self.ROLE_PAGES.get(user_role, ['DASHBOARD'])
        
        # Show/hide navigation buttons based on role
        for page_name, btn in self.nav_btns.items():
            if page_name in allowed_pages:
                btn.setVisible(True)
            else:
                btn.setVisible(False)
        
        # Switch to dashboard on login
        self.switch_page(0, "DASHBOARD")
    
    def add_notification(self, message, type="info"):
        """Add a notification to the sidebar."""
        notification_frame = QFrame()
        notification_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-left: 3px solid #0056b3;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        notification_layout = QVBoxLayout(notification_frame)
        notification_layout.setContentsMargins(8, 8, 8, 8)
        
        notification_label = QLabel(message)
        notification_label.setWordWrap(True)
        notification_label.setStyleSheet("border: none; color: #374151; font-size: 11px; font-weight: 500;")
        notification_layout.addWidget(notification_label)
        
        # Insert before the stretch
        self.notifications_layout.insertWidget(self.notifications_layout.count() - 1, notification_frame)
    
    def refresh_dashboard_kpis(self):
        """Refresh dashboard KPI values from database."""
        try:
            from models.purchase import DashboardModel
            
            kpis = DashboardModel.get_all_kpis()
            
            # Update Inventory Value (format as currency)
            inventory_value = kpis['inventory_value']
            self.inventory_value_label.setText(f"₱ {inventory_value:,.2f}")
            
            # Update Wastages
            wastages = kpis['wastages']
            self.wastages_label.setText(str(wastages))
            
            # Update Inventory Items
            inventory_items = kpis['inventory_items']
            self.inventory_items_label.setText(str(inventory_items))
            
            # Update Low Stocks
            low_stocks = kpis['low_stocks']
            self.low_stocks_label.setText(str(low_stocks))
            
        except Exception as e:
            print(f"Error refreshing dashboard KPIs: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_kpi_card(self, value, title):
        """Create a KPI card widget and return both card and value label."""
        card = QFrame()
        card.setMinimumHeight(200)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        # Value label (large number)
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        value_label.setStyleSheet("border: none; color: #111827;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(value_label)
        
        # Title label
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        title_label.setStyleSheet("border: none; color: #6b7280; font-weight: 500; font-style: italic;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)
        
        return card, value_label
    
    def handle_logout(self):
        """Handle logout - clear session and return to login."""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.current_user = None
            self.current_role = None
            # Signal to show login window
            if hasattr(self, 'on_logout'):
                self.on_logout()
            self.close()

    def switch_page(self, index, title):
        self.main_stack.setCurrentIndex(index)
        self.title_label.setText(title)
        
        # Refresh dashboard KPIs when switching to dashboard page
        if title == "DASHBOARD":
            self.refresh_dashboard_kpis()
        
        # Refresh messages when switching to messages page
        if title == "MESSAGES" and self.current_user:
            # Update the current user ID and refresh messages
            self.messages_ctrl.current_user_id = self.messages_ctrl.get_current_user_id()
            self.messages_ctrl.refresh_messages()
        
        # Update sidebar styling
        for name, btn in self.nav_btns.items():
            btn.setObjectName("ActiveNav" if name == title else "")
            btn.style().unpolish(btn)
            btn.style().polish(btn)