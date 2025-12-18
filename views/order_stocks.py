from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QComboBox, 
    QSpinBox, QDoubleSpinBox, QMessageBox, QLineEdit, QDateEdit, 
    QScrollArea, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate

# --- Shared Style Constants ---
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"

class AddItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADD NEW LINE ITEM")
        # Make dialog resizable with minimum and initial size
        self.setMinimumSize(480, 550)
        self.resize(520, 700)
        # Allow dialog to be resizable
        self.setSizeGripEnabled(True)
        self.init_ui()

    def init_ui(self):
        # Main layout for the dialog
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Content widget inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #ffffff;")
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        self.setStyleSheet(f"""
            QDialog {{ background-color: #ffffff; }}
            QLabel {{ font-size: 10px; font-weight: 800; color: #6b7280; letter-spacing: 1px; }}
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{
                border: 1px solid {STYLE_BORDER}; border-radius: 2px; padding: 10px; 
                color: {STYLE_NAVY}; background-color: #ffffff;
                min-height: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #ffffff; color: {STYLE_NAVY};
                selection-background-color: #eff6ff; selection-color: {STYLE_BLUE};
            }}
            QScrollArea {{
                border: none;
                background-color: #ffffff;
            }}
            QScrollArea > QWidget {{
                background-color: #ffffff;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: #ffffff;
            }}
        """)

        # Item Name
        layout.addWidget(QLabel("ITEM NAME"))
        self.name_le = QLineEdit()
        self.name_le.setPlaceholderText("e.g., Office Chair, Bed Linens, etc.")
        self.name_le.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.name_le)

        # Category
        layout.addWidget(QLabel("CATEGORY"))
        self.category_cb = QComboBox()
        self.category_cb.addItems(["Room Supplies", "F&B", "Cleaning", "Maintenance", "Others"])
        self.category_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.category_cb)

        # Supplier
        layout.addWidget(QLabel("SUPPLIER"))
        self.supplier_cb = QComboBox()
        self.supplier_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.supplier_cb)

        # Contact Person (read-only, auto-filled from supplier selection)
        layout.addWidget(QLabel("SUPPLIER CONTACT"))
        self.contact_le = QLineEdit()
        self.contact_le.setReadOnly(True)
        self.contact_le.setStyleSheet(f"background-color: #f9fafb; color: #6b7280; min-height: 20px;")
        self.contact_le.setPlaceholderText("Auto-filled from supplier")
        self.contact_le.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.contact_le)

        # Expected Delivery Date
        layout.addWidget(QLabel("EXPECTED DELIVERY DATE"))
        self.expected_date = QDateEdit()
        self.expected_date.setCalendarPopup(True)
        self.expected_date.setDate(QDate.currentDate().addDays(7))  # Default 7 days from now
        self.expected_date.setDisplayFormat("yyyy-MM-dd")
        self.expected_date.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.expected_date)

        # Unit
        layout.addWidget(QLabel("UNIT OF MEASURE"))
        self.unit_le = QLineEdit()
        self.unit_le.setPlaceholderText("e.g., pcs, box, kg, liter")
        self.unit_le.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.unit_le)

        # Quantity and Unit Price Row (responsive)
        row = QHBoxLayout()
        row.setSpacing(10)
        
        qty_layout = QVBoxLayout()
        qty_layout.setSpacing(5)
        qty_layout.addWidget(QLabel("QUANTITY"))
        self.qty_sb = QSpinBox()
        self.qty_sb.setRange(1, 99999)
        self.qty_sb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        qty_layout.addWidget(self.qty_sb)
        
        price_layout = QVBoxLayout()
        price_layout.setSpacing(5)
        price_layout.addWidget(QLabel("UNIT PRICE (₱)"))
        self.price_ds = QDoubleSpinBox()
        self.price_ds.setRange(0, 1000000)
        self.price_ds.setDecimals(2)
        self.price_ds.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        price_layout.addWidget(self.price_ds)
        
        row.addLayout(qty_layout, 1)
        row.addLayout(price_layout, 1)
        layout.addLayout(row)

        # Total Amount Display
        total_frame = QFrame()
        total_frame.setStyleSheet(f"background-color: {STYLE_BG_LIGHT}; border: 1px solid #e5e7eb; border-radius: 2px;")
        total_frame.setMinimumHeight(85)
        total_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        total_lay = QVBoxLayout(total_frame)
        total_lay.setContentsMargins(15, 10, 15, 10)
        self.total_le = QLineEdit("₱ 0.00")
        self.total_le.setReadOnly(True)
        self.total_le.setStyleSheet(f"border: none; background: transparent; font-size: 24px; font-weight: bold; color: {STYLE_BLUE};")
        self.total_le.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        total_lay.addWidget(QLabel("TOTAL AMOUNT"))
        total_lay.addWidget(self.total_le)
        layout.addWidget(total_frame)

        # Add stretch to push content to top when scrolling not needed
        layout.addStretch()

        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)

        # Button container (fixed at bottom, not in scroll area)
        button_container = QWidget()
        button_container.setStyleSheet("background-color: white; border-top: 1px solid #e5e7eb;")
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(25, 15, 25, 15)
        
        # Add Button
        self.add_btn = QPushButton("ADD TO LIST")
        self.add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY}; 
                color: white; 
                padding: 14px; 
                font-weight: bold; 
                border-radius: 2px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {STYLE_BLUE};
            }}
        """)
        self.add_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_layout.addWidget(self.add_btn)
        
        main_layout.addWidget(button_container)

        # Connections
        self.qty_sb.valueChanged.connect(self.recalc)
        self.price_ds.valueChanged.connect(self.recalc)
        self.add_btn.clicked.connect(self.on_add)
        self.supplier_cb.currentIndexChanged.connect(self.on_supplier_changed)

    def on_supplier_changed(self):
        """Update contact field when supplier is selected."""
        contact = self.supplier_cb.currentData(Qt.ItemDataRole.UserRole + 1)
        if contact:
            self.contact_le.setText(contact)
        else:
            self.contact_le.clear()

    def on_add(self):
        # basic validation
        if not self.name_le.text().strip():
            QMessageBox.warning(self, "Validation", "Item name is required.")
            return
        if not self.unit_le.text().strip():
            QMessageBox.warning(self, "Validation", "Unit of measure is required.")
            return
        if self.supplier_cb.currentIndex() == 0 or not self.supplier_cb.currentData():
            QMessageBox.warning(self, "Validation", "Please select a supplier.")
            return
        # qty and price already constrained
        self.accept()

    def recalc(self):
        total = self.qty_sb.value() * self.price_ds.value()
        self.total_le.setText(f"₱ {total:,.2f}")

    def get_data(self):
        return {
            'item_name': self.name_le.text().strip(),
            'category': self.category_cb.currentText(),
            'supplier_id': self.supplier_cb.currentData(),
            'supplier_name': self.supplier_cb.currentText(),
            'contact': self.contact_le.text().strip(),
            'expected_date': self.expected_date.date().toString('yyyy-MM-dd'),
            'unit': self.unit_le.text().strip(),
            'qty': self.qty_sb.value(),
            'price': self.price_ds.value(),
            'total': self.qty_sb.value() * self.price_ds.value()
        }

class OrderStocksDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PROCUREMENT ORDER ENTRY")
        self.resize(1100, 750)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(20)
        self.setStyleSheet("QDialog { background-color: #f4f7f9; }")

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ITEM", "CATEGORY", "UNIT", "QTY", "PRICE", "TOTAL", "ACTION"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setStyleSheet(f"""
            QTableWidget {{ 
                background-color: white; 
                border: 1px solid {STYLE_BORDER}; 
                font-size: 13px;
                color: {STYLE_NAVY};
                alternate-background-color: #fcfcfd;
            }}
            QHeaderView::section {{
                background-color: {STYLE_BG_LIGHT};
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: bold;
                font-size: 10px;
                color: #4b5563;
                text-transform: uppercase;
            }}
            QTableWidget::item {{
                border-bottom: 1px solid #f3f4f6;
                padding: 10px;
                color: {STYLE_NAVY};
            }}
        """)
        root.addWidget(self.table)

        footer = QHBoxLayout()
        self.add_item_btn = QPushButton("+ ADD NEW LINE")
        self.add_item_btn.setStyleSheet(f"border: 1px dashed {STYLE_BLUE}; color: {STYLE_BLUE}; font-weight: bold; padding: 12px;")
        self.total_lbl = QLabel("TOTAL AMOUNT: ₱ 0.00")
        self.total_lbl.setStyleSheet(f"font-size: 24px; font-weight: 900; color: {STYLE_NAVY};")
        footer.addWidget(self.add_item_btn); footer.addStretch(); footer.addWidget(self.total_lbl)
        root.addLayout(footer)

        self.save_btn = QPushButton("CONFIRM PURCHASE ORDER")
        self.save_btn.setStyleSheet(f"background-color: {STYLE_BLUE}; color: white; padding: 16px 40px; font-weight: 900;")
        root.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignRight)