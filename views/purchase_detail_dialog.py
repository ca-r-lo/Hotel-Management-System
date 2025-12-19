from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QPushButton, QFrame, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush

class PurchaseDetailDialog(QDialog):
    def __init__(self, purchase_data, parent=None):
        super().__init__(parent)
        self.purchase_data = purchase_data
        self.setWindowTitle(f"Purchase Order Details - #{purchase_data.get('id', 0):04d}")
        self.resize(900, 700)
        self.setSizeGripEnabled(True)
        self.init_ui()
        self.load_items()
    
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: white; }")
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: white;")
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = QLabel(f"PURCHASE ORDER #{self.purchase_data.get('id', 0):04d}")
        header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #111827;
            padding: 10px 0;
        """)
        layout.addWidget(header)
        
        # Order Information Section
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(12)
        
        # Order details
        order_date = str(self.purchase_data.get('created_at', ''))[:10]
        expected_date = str(self.purchase_data.get('expected_date', ''))[:10]
        supplier = self.purchase_data.get('supplier_name', 'N/A')
        contact = self.purchase_data.get('supplier_contact', 'N/A')
        status = str(self.purchase_data.get('status', 'PENDING')).upper()
        created_by = self.purchase_data.get('created_by', 'N/A')
        total = f"₱ {float(self.purchase_data.get('total_amount', 0)):,.2f}"
        
        # Status badge with color
        status_colors = {
            'PENDING': ('#fef3c7', '#92400e'),       # Yellow bg, dark yellow text
            'RECEIVED': ('#d1fae5', '#065f46'),      # Green bg, dark green text
            'DELIVERED': ('#d1fae5', '#065f46'),     # Green bg, dark green text
            'COMPLETED': ('#d1fae5', '#065f46'),     # Green bg, dark green text
            'CANCELLED': ('#fee2e2', '#991b1b'),     # Red bg, dark red text
            'REJECTED': ('#fee2e2', '#991b1b')       # Red bg, dark red text
        }
        bg_color, text_color = status_colors.get(status, ('#f3f4f6', '#111827'))
        
        status_label = QLabel(f"STATUS: {status}")
        status_label.setStyleSheet(f"""
            background-color: {bg_color};
            color: {text_color};
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 13px;
            letter-spacing: 0.5px;
        """)
        info_layout.addWidget(status_label)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e5e7eb;")
        info_layout.addWidget(separator)
        
        # Details grid
        details = [
            ("Order Date:", order_date),
            ("Expected Date:", expected_date),
            ("Supplier:", supplier),
            ("Contact:", contact),
            ("Created By:", created_by),
            ("Total Amount:", total)
        ]
        
        for label_text, value_text in details:
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; color: #000000; font-size: 13px;")
            label.setFixedWidth(150)
            
            value = QLabel(value_text)
            value.setStyleSheet("color: #000000; font-size: 13px;")
            
            row_layout.addWidget(label)
            row_layout.addWidget(value)
            row_layout.addStretch()
            info_layout.addLayout(row_layout)
        
        layout.addWidget(info_frame)
        
        # Items Section
        items_label = QLabel("ORDER ITEMS")
        items_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #374151;
            margin-top: 10px;
        """)
        layout.addWidget(items_label)
        
        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels([
            "ITEM NAME", "QUANTITY", "UNIT", "UNIT PRICE", "TOTAL"
        ])
        self.items_table.horizontalHeader().setStretchLastSection(True)
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                font-size: 13px;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: bold;
                font-size: 11px;
                color: #6b7280;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f3f4f6;
                color: #000000;
            }
        """)
        layout.addWidget(self.items_table)
        
        # Close button
        close_btn = QPushButton("CLOSE")
        close_btn.setFixedHeight(40)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        close_btn.clicked.connect(self.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
    
    def load_items(self):
        """Load purchase items into the table."""
        from models.database import get_conn, _paramstyle
        
        try:
            conn = get_conn()
            cur = conn.cursor()
            
            purchase_id = self.purchase_data.get('id')
            
            # Adjust SQL based on database
            if _paramstyle == 'qmark':
                sql = """
                    SELECT 
                        COALESCE(pi.item_name, i.name) as item_name,
                        pi.quantity,
                        i.unit,
                        pi.unit_price,
                        pi.total
                    FROM purchase_items pi
                    LEFT JOIN items i ON pi.item_id = i.id
                    WHERE pi.purchase_id = ?
                """
            else:
                sql = """
                    SELECT 
                        COALESCE(pi.item_name, i.name) as item_name,
                        pi.quantity,
                        i.unit,
                        pi.unit_price,
                        pi.total
                    FROM purchase_items pi
                    LEFT JOIN items i ON pi.item_id = i.id
                    WHERE pi.purchase_id = %s
                """
            
            cur.execute(sql, (purchase_id,))
            items = cur.fetchall()
            
            self.items_table.setRowCount(len(items))
            
            for r_idx, row in enumerate(items):
                try:
                    item_dict = dict(row)
                    item_name = item_dict.get('item_name', 'Unknown')
                    quantity = item_dict.get('quantity', 0)
                    unit = item_dict.get('unit', 'pcs')
                    unit_price = float(item_dict.get('unit_price', 0))
                    total = float(item_dict.get('total', 0))
                except:
                    item_name = row[0] if len(row) > 0 else 'Unknown'
                    quantity = row[1] if len(row) > 1 else 0
                    unit = row[2] if len(row) > 2 else 'pcs'
                    unit_price = float(row[3]) if len(row) > 3 else 0
                    total = float(row[4]) if len(row) > 4 else 0
                
                # Add items to table
                name_item = QTableWidgetItem(str(item_name))
                qty_item = QTableWidgetItem(str(quantity))
                unit_item = QTableWidgetItem(str(unit))
                price_item = QTableWidgetItem(f"₱ {unit_price:,.2f}")
                total_item = QTableWidgetItem(f"₱ {total:,.2f}")
                
                name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                unit_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                
                self.items_table.setItem(r_idx, 0, name_item)
                self.items_table.setItem(r_idx, 1, qty_item)
                self.items_table.setItem(r_idx, 2, unit_item)
                self.items_table.setItem(r_idx, 3, price_item)
                self.items_table.setItem(r_idx, 4, total_item)
            
            conn.close()
            
        except Exception as e:
            print(f"Error loading purchase items: {e}")
            import traceback
            traceback.print_exc()
