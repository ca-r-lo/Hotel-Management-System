from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from views.purchase_view import PurchasePage
from views.inventory import InventoryPage
from views.reports import ReportsPage
from views.messages import MessagesPage
from views.trans_history import TransactionHistoryPage
from views.requests import RequestsPage
from views.dept_overview import DepartmentOverviewPage
from controllers.purchase_controller import PurchaseController
from controllers.inventory_controller import InventoryController
from controllers.reports_controller import ReportsController
from controllers.messages_controller import MessagesController
from controllers.trans_history_controller import TransactionHistoryController
from controllers.requests_controller import RequestsController
from controllers.dept_overview_controller import DeptOverviewController
from models import purchase as purchase_model

class DashboardWindow(QMainWindow):
    # Define role-based access control
    ROLE_PAGES = {
        'Purchase Admin': ['DASHBOARD', 'PURCHASE', 'INVENTORY', 'REPORTS', 'MESSAGES'],
        'Owner': ['DASHBOARD', 'TRANS HISTORY', 'DEPT OVERVIEW', 'REPORTS', 'MESSAGES'],
        # Department role has Requests page and Reports; no Purchase
        'Department': ['DASHBOARD', 'INVENTORY', 'REQUESTS', 'REPORTS', 'MESSAGES']
    }
    
    # Department assignments for Department Managers (would normally come from database)
    DEPARTMENT_ASSIGNMENTS = {
        'Department': 'Housekeeping',  # Default assignment
        # Could be expanded to map specific users to departments
    }
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STASH - Hotel Management System")
        self.current_user = None  # Store logged-in user name
        self.current_role = None  # Store logged-in user role
        self.current_department = None  # Store logged-in user department
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
        profile_container.setStyleSheet("background-color: transparent; border: none; padding: 10px 15px;")
        profile_lay = QHBoxLayout(profile_container)
        profile_lay.setSpacing(10)
        profile_lay.setContentsMargins(0, 0, 0, 0)
        
        # Profile icon (circle with initial)
        profile_icon = QLabel("👤")
        profile_icon.setFixedSize(45, 45)
        profile_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_icon.setStyleSheet("""
            background-color: #e5e7eb;
            border-radius: 22px;
            font-size: 22px;
            border: none;
        """)
        profile_lay.addWidget(profile_icon)
        
        # Name and role container with proper sizing
        name_role_container = QVBoxLayout()
        name_role_container.setSpacing(2)
        name_role_container.setContentsMargins(0, 0, 0, 0)
        
        self.name_lbl = QLabel("Director Name")
        self.name_lbl.setMaximumWidth(165)  # Prevent overflow
        self.name_lbl.setWordWrap(False)
        self.name_lbl.setStyleSheet("""
            color: #111827; 
            font-size: 13px; 
            font-weight: 700; 
            border: none;
        """)
        # Enable text eliding
        self.name_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        
        self.role_lbl = QLabel("Director")
        self.role_lbl.setMaximumWidth(165)  # Prevent overflow
        self.role_lbl.setWordWrap(False)
        self.role_lbl.setStyleSheet("""
            color: #6b7280; 
            font-size: 11px; 
            font-weight: 500; 
            border: none;
        """)
        
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
        nav_pages = ["DASHBOARD", "TRANS HISTORY", "DEPT OVERVIEW", "PURCHASE", "INVENTORY", "REQUESTS", "REPORTS", "MESSAGES"]
        for text in nav_pages:
            btn = QPushButton(text)
            if text == "DASHBOARD": btn.setObjectName("ActiveNav")
            sidebar_layout.addWidget(btn)
            self.nav_btns[text] = btn
        
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
        inv_value_card, self.inventory_value_label = self._create_kpi_card("0", "Inventory Value", "inventory_value")
        kpi_row1_layout.addWidget(inv_value_card)
        
        # Wastages Card
        wastages_card, self.wastages_label = self._create_kpi_card("0", "Wastages", "wastages")
        kpi_row1_layout.addWidget(wastages_card)
        
        kpi_grid_layout.addLayout(kpi_row1_layout)
        
        # Second row
        kpi_row2_layout = QHBoxLayout()
        kpi_row2_layout.setSpacing(20)
        
        # Inventory Items Card
        inv_items_card, self.inventory_items_label = self._create_kpi_card("0", "Inventory Items", "inventory_items")
        kpi_row2_layout.addWidget(inv_items_card)
        
        # Low Stocks Card
        low_stocks_card, self.low_stocks_label = self._create_kpi_card("0", "Low Stocks", "low_stocks")
        kpi_row2_layout.addWidget(low_stocks_card)
        
        kpi_grid_layout.addLayout(kpi_row2_layout)
        
        dash_page_layout.addLayout(kpi_grid_layout)
        dash_page_layout.addStretch()

        # PAGE 2: TRANS HISTORY (Transaction History)
        self.trans_history_page = TransactionHistoryPage()
        
        # PAGE 3: DEPT OVERVIEW (Department Overview)
        self.dept_overview_page = DepartmentOverviewPage()
        
        # PAGE 4: PURCHASE (Initialized and added AFTER self.main_stack exists)
        self.purchase_page = PurchasePage()
        
        # PAGE 5: INVENTORY
        self.inventory_page = InventoryPage()
        
        # PAGE 6: REQUESTS (Department role)
        self.requests_page = RequestsPage()
        
        # PAGE 7: REPORTS
        self.reports_page = ReportsPage()
        
        # PAGE 7: MESSAGES
        self.messages_page = MessagesPage()
        
        # 5. Logic & Controllers (Initialized now that views exist)
        self.p_model = purchase_model.PurchaseModel()
        self.m_model = purchase_model.MessageModel()
        self.purchase_ctrl = PurchaseController(self.purchase_page, self.p_model, self)
        self.inventory_ctrl = InventoryController(self.inventory_page, self.p_model)
        self.reports_ctrl = ReportsController(self.reports_page, self.p_model)
        self.requests_ctrl = RequestsController(self.requests_page)
        self.messages_ctrl = MessagesController(self.messages_page, self.m_model, self)
        self.trans_history_ctrl = TransactionHistoryController(self.trans_history_page, self.p_model)
        self.dept_overview_ctrl = DeptOverviewController(self.dept_overview_page)

        # 6. Assemble Stack
        self.main_stack.addWidget(self.dash_page)          # Index 0
        self.main_stack.addWidget(self.trans_history_page) # Index 1
        self.main_stack.addWidget(self.dept_overview_page) # Index 2
        self.main_stack.addWidget(self.purchase_page)      # Index 3
        self.main_stack.addWidget(self.inventory_page)     # Index 4
        self.main_stack.addWidget(self.requests_page)      # Index 5
        self.main_stack.addWidget(self.reports_page)       # Index 6
        self.main_stack.addWidget(self.messages_page)      # Index 7

        content_main_layout.addWidget(self.main_stack)
        self.main_layout.addWidget(content_container)

        # 7. Connect Navigation
        self.nav_btns["DASHBOARD"].clicked.connect(lambda: self.switch_page(0, "DASHBOARD"))
        self.nav_btns["TRANS HISTORY"].clicked.connect(lambda: self.switch_page(1, "TRANS HISTORY"))
        self.nav_btns["DEPT OVERVIEW"].clicked.connect(lambda: self.switch_page(2, "DEPT OVERVIEW"))
        self.nav_btns["PURCHASE"].clicked.connect(lambda: self.switch_page(3, "PURCHASE"))
        self.nav_btns["INVENTORY"].clicked.connect(lambda: self.switch_page(4, "INVENTORY"))
        self.nav_btns["REQUESTS"].clicked.connect(lambda: self.switch_page(5, "REQUESTS"))
        self.nav_btns["REPORTS"].clicked.connect(lambda: self.switch_page(6, "REPORTS"))
        self.nav_btns["MESSAGES"].clicked.connect(lambda: self.switch_page(7, "MESSAGES"))
        
        # Connect Logout
        self.logout_btn.clicked.connect(self.handle_logout)

    def update_ui_for_role(self, user_name, user_role, user_department=None):
        """Update UI based on user role - show/hide navigation buttons."""
        self.current_user = user_name
        self.current_role = user_role
        self.current_department = user_department
        
        # Update profile labels with text eliding
        self.set_elided_text(self.name_lbl, user_name, 165)
        self.set_elided_text(self.role_lbl, user_role, 165)
        
        # Get allowed pages for this role
        allowed_pages = self.ROLE_PAGES.get(user_role, ['DASHBOARD'])
        
        # Show/hide navigation buttons based on role
        for page_name, btn in self.nav_btns.items():
            if page_name in allowed_pages:
                btn.setVisible(True)
            else:
                btn.setVisible(False)
        
        # Update inventory page UI based on role
        if user_role == "Department":
            # Use the department from the database, or default to Housekeeping
            department = user_department or self.DEPARTMENT_ASSIGNMENTS.get(user_role, "Housekeeping")
            self.inventory_page.update_ui_for_role(user_role, department)
            # Trigger refresh with department filter
            self.inventory_ctrl.current_category_filter = department
            self.inventory_ctrl.refresh_inventory()
            
            # Set user info for requests page
            self.requests_ctrl.set_user_info(user_name, user_role, department)
            
            # Set user info for reports page
            self.reports_ctrl.set_user_info(user_name, user_role, department)
        else:
            self.inventory_page.update_ui_for_role(user_role)
            # Set user info for requests page (for Purchase Admin/Owner)
            self.requests_ctrl.set_user_info(user_name, user_role, None)
            
            # Set user info for reports page
            self.reports_ctrl.set_user_info(user_name, user_role, None)
        
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
            
            # Use department-specific KPIs for Department role
            if self.current_role == "Department":
                # Get department assignment from user's department or default
                department_filter = self.current_department or self.DEPARTMENT_ASSIGNMENTS.get(self.current_role, "Housekeeping")
                kpis = DashboardModel.get_department_kpis(department_filter)
                
                # Update with formatted department values
                self.inventory_value_label.setText(kpis['inventory_value'])
                self.wastages_label.setText(str(kpis['wastages']))
                self.inventory_items_label.setText(str(kpis['inventory_items']))
                
                # For department role, calculate low stocks in their department
                try:
                    from models.database import get_conn, _paramstyle
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute(f"SELECT COUNT(*) FROM items WHERE category = {_paramstyle()} AND stock_qty <= min_stock", (department_filter,))
                    row = cur.fetchone()
                    low_stocks = int(row[0] if row else 0)
                    conn.close()
                except Exception:
                    low_stocks = 0
                
                self.low_stocks_label.setText(str(low_stocks))
            else:
                # For other roles (Owner, Purchase Admin), show all data
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
    
    def _create_kpi_card(self, value, title, kpi_type=None):
        """Create a KPI card widget and return both card and value label."""
        card = QFrame()
        card.setMinimumHeight(200)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
            }
            QFrame:hover {
                border-color: #0056b3;
                background-color: #f9fafb;
                cursor: pointer;
            }
        """)
        card.setProperty("kpi_type", kpi_type)
        
        # Make card clickable
        card.mousePressEvent = lambda event: self.handle_kpi_click(kpi_type)
        
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
        
        # Click hint
        if kpi_type:
            hint_label = QLabel("Click to view details")
            hint_label.setFont(QFont("Arial", 10))
            hint_label.setStyleSheet("border: none; color: #9ca3af; font-size: 10px;")
            hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(hint_label)
        
        return card, value_label
    
    def handle_kpi_click(self, kpi_type):
        """Handle KPI card click to show detailed data."""
        if not kpi_type:
            return
        
        from views.kpi_details import InventoryValueDialog, WastagesDialog, LowStocksDialog
        from models.database import get_conn, _paramstyle
        
        try:
            if kpi_type == "inventory_value":
                # Show inventory value breakdown
                dialog = InventoryValueDialog(self, self.current_department if self.current_role == "Department" else None)
                
                # Fetch inventory data
                conn = get_conn()
                cur = conn.cursor()
                
                if self.current_role == "Department" and self.current_department:
                    # Department-specific items
                    cur.execute(
                        f"SELECT name, category, unit, stock_qty, unit_cost FROM items WHERE category = {_paramstyle()} ORDER BY name",
                        (self.current_department,)
                    )
                else:
                    # All items
                    cur.execute("SELECT name, category, unit, stock_qty, unit_cost FROM items ORDER BY name")
                
                rows = cur.fetchall()
                items = []
                for row in rows:
                    try:
                        items.append(dict(row))
                    except:
                        items.append({
                            'name': row[0],
                            'category': row[1],
                            'unit': row[2],
                            'stock_qty': row[3],
                            'unit_cost': row[4]
                        })
                
                conn.close()
                dialog.populate_data(items)
                dialog.exec()
            
            elif kpi_type == "wastages":
                # Show damage reports
                dialog = WastagesDialog(self)
                
                # Fetch damages data
                conn = get_conn()
                cur = conn.cursor()
                cur.execute("""
                    SELECT d.created_at, i.name as item_name, d.quantity, d.reason, d.created_by
                    FROM damages d
                    LEFT JOIN items i ON d.item_id = i.id
                    ORDER BY d.created_at DESC
                """)
                
                rows = cur.fetchall()
                damages = []
                for row in rows:
                    try:
                        damages.append(dict(row))
                    except:
                        damages.append({
                            'created_at': row[0],
                            'item_name': row[1],
                            'quantity': row[2],
                            'reason': row[3],
                            'created_by': row[4]
                        })
                
                conn.close()
                dialog.populate_data(damages)
                dialog.exec()
            
            elif kpi_type == "inventory_items":
                # Show all inventory items (same as inventory value but different focus)
                dialog = InventoryValueDialog(self, self.current_department if self.current_role == "Department" else None)
                
                # Fetch inventory data
                conn = get_conn()
                cur = conn.cursor()
                
                if self.current_role == "Department" and self.current_department:
                    cur.execute(
                        f"SELECT name, category, unit, stock_qty, unit_cost FROM items WHERE category = {_paramstyle()} ORDER BY name",
                        (self.current_department,)
                    )
                else:
                    cur.execute("SELECT name, category, unit, stock_qty, unit_cost FROM items ORDER BY name")
                
                rows = cur.fetchall()
                items = []
                for row in rows:
                    try:
                        items.append(dict(row))
                    except:
                        items.append({
                            'name': row[0],
                            'category': row[1],
                            'unit': row[2],
                            'stock_qty': row[3],
                            'unit_cost': row[4]
                        })
                
                conn.close()
                dialog.populate_data(items)
                dialog.exec()
            
            elif kpi_type == "low_stocks":
                # Show low stock items
                dialog = LowStocksDialog(self, self.current_department if self.current_role == "Department" else None)
                
                # Fetch low stock items
                conn = get_conn()
                cur = conn.cursor()
                
                if self.current_role == "Department" and self.current_department:
                    cur.execute(
                        f"SELECT name, category, stock_qty, min_stock FROM items WHERE category = {_paramstyle()} AND stock_qty <= min_stock ORDER BY stock_qty ASC",
                        (self.current_department,)
                    )
                else:
                    cur.execute("SELECT name, category, stock_qty, min_stock FROM items WHERE stock_qty <= min_stock ORDER BY stock_qty ASC")
                
                rows = cur.fetchall()
                items = []
                for row in rows:
                    try:
                        items.append(dict(row))
                    except:
                        items.append({
                            'name': row[0],
                            'category': row[1],
                            'stock_qty': row[2],
                            'min_stock': row[3]
                        })
                
                conn.close()
                dialog.populate_data(items)
                dialog.exec()
        
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to load KPI details: {str(e)}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
            print(f"Error loading KPI details: {e}")
            import traceback
            traceback.print_exc()
    
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
        
        # Refresh transaction history when switching to trans history page
        elif title == "TRANS HISTORY":
            self.trans_history_ctrl.refresh_transactions()
        
        # Refresh department overview when switching to dept overview page
        elif title == "DEPT OVERVIEW":
            # Load data for all departments or specific department
            if self.current_role == "Department" and self.current_department:
                self.dept_overview_ctrl.load_department_data(self.current_department)
            else:
                # For Owner, show first department or all
                self.dept_overview_ctrl.load_department_data("Housekeeping")
        
        # Refresh purchase page when switching to purchase page
        elif title == "PURCHASE":
            self.purchase_ctrl.refresh_table()
        
        # Refresh inventory when switching to inventory page
        elif title == "INVENTORY":
            self.inventory_ctrl.refresh_inventory()
        
        # Refresh requests when switching to requests page
        elif title == "REQUESTS":
            self.requests_ctrl.refresh_requests()
        
        # Refresh reports when switching to reports page
        elif title == "REPORTS":
            self.reports_ctrl.refresh_charts()
        
        # Refresh messages when switching to messages page
        elif title == "MESSAGES" and self.current_user:
            # Update the current user ID and refresh messages
            self.messages_ctrl.current_user_id = self.messages_ctrl.get_current_user_id()
            self.messages_ctrl.refresh_messages()
        
        # Update sidebar styling
        for name, btn in self.nav_btns.items():
            btn.setObjectName("ActiveNav" if name == title else "")
            btn.style().unpolish(btn)
            btn.style().polish(btn)    
    def set_elided_text(self, label, text, max_width):
        """Set text on label with eliding if it's too long."""
        from PyQt6.QtGui import QFontMetrics
        from PyQt6.QtCore import Qt
        
        # Get font metrics
        font_metrics = QFontMetrics(label.font())
        
        # Elide text if too wide
        elided_text = font_metrics.elidedText(
            text, 
            Qt.TextElideMode.ElideRight, 
            max_width
        )
        
        # Set the elided text
        label.setText(elided_text)
        # Set tooltip with full text if elided
        if elided_text != text:
            label.setToolTip(text)
        else:
            label.setToolTip("")
