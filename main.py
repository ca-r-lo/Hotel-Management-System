import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt

from controllers.purchase_controller import PurchaseController
from views.login import LoginWindow
from views.dashboard import DashboardWindow

from controllers.login import LoginController
from views.purchase_view import PurchasePage
from models.purchase import PurchaseModel
from models.user import UserModel

from configs.config import DB_CONFIG


def main():
    app = QApplication(sys.argv)

    icon_pixmap = QPixmap("assets/logo_taskbar.png")
    scaled_icon = icon_pixmap.scaled(256, 256, 
                                    Qt.AspectRatioMode.KeepAspectRatio, 
                                    Qt.TransformationMode.SmoothTransformation)

    app.setWindowIcon(QIcon(scaled_icon))
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("stash.hms.v1")
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    login_view = LoginWindow()
    dashboard_view = DashboardWindow()

    user_model = UserModel(DB_CONFIG)

    controller = LoginController(login_view, user_model, dashboard_view)
    
    purchase_view = PurchasePage()
    purchase_model = PurchaseModel()
    purchase_controller = PurchaseController(purchase_view, purchase_model)
    
    login_view.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
