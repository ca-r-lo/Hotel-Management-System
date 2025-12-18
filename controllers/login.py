from PyQt6.QtWidgets import QMessageBox, QPushButton
from models.purchase import create_tables


class LoginController:
    def __init__(self, view, model, dashboard_view):
        self.view = view
        self.model = model
        self.dashboard_view = dashboard_view
        
        # Connect the view's login button to our logic
        btn = self.view.findChild(QPushButton, "LoginBtn")
        if btn:
            btn.clicked.connect(self.handle_login)

    def handle_login(self):
        email, password = self.view.get_login_data()
        
        if not email or not password:
            QMessageBox.warning(self.view, "Input Error", "Please fill in all fields.")
            return

        user_data = self.model.authenticate(email, password)

        if user_data:
            full_name, role = user_data
            print(f"Login successful for {full_name}")

            # Initialize database tables
            try:
                create_tables()
            except Exception as e:
                print(f"Error initializing database tables: {e}")

            # Switch Windows and update UI based on role
            self.view.hide()
            self.dashboard_view.update_ui_for_role(full_name, role)
            self.dashboard_view.showMaximized()
        else:
            QMessageBox.critical(self.view, "Login Failed", "Invalid email or password.")