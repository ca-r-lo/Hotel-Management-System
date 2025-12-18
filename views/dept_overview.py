from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QColor
from PyQt6.QtWidgets import QSizePolicy


class DepartmentOverviewPage(QWidget):
    """Department Overview page for Directors/Owners to view department-wise inventory."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # Department Selector
        selector_layout = QHBoxLayout()
        selector_layout.setSpacing(15)
        
        dept_label = QLabel("DEPARTMENT:")
        dept_label.setStyleSheet("font-weight: 700; font-size: 11px; color: #374151;")
        selector_layout.addWidget(dept_label)
        
        self.dept_selector = QComboBox()
        self.dept_selector.setFixedHeight(40)
        self.dept_selector.setFixedWidth(250)
        self.dept_selector.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                color: #111827;
            }
            QComboBox:hover {
                border-color: #0056b3;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6b7280;
                margin-right: 8px;
            }
        """)
        # Populate with departments
        departments = ["All Departments", "Housekeeping", "Kitchen", "Front Desk", "Maintenance", "Laundry"]
        self.dept_selector.addItems(departments)
        selector_layout.addWidget(self.dept_selector)
        
        selector_layout.addStretch()
        self.layout.addLayout(selector_layout)

        # Main content area - split into left KPIs and right chart
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Left side - KPI Cards (vertical stack)
        left_panel = QVBoxLayout()
        left_panel.setSpacing(20)
        
        # Inventory Value Card
        inv_value_card, self.inv_value_label = self._create_kpi_card("0", "Inventory Value")
        left_panel.addWidget(inv_value_card)
        
        # Inventory Items Card
        inv_items_card, self.inv_items_label = self._create_kpi_card("0", "Inventory Items")
        left_panel.addWidget(inv_items_card)
        
        # Wastages Card
        wastages_card, self.wastages_label = self._create_kpi_card("0", "Wastages")
        left_panel.addWidget(wastages_card)
        
        left_panel.addStretch()
        
        # Add left panel to content
        content_layout.addLayout(left_panel, 1)

        # Right side - Inventory Items Chart
        chart_container = QFrame()
        chart_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
            }
        """)
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(20, 20, 20, 20)
        chart_layout.setSpacing(15)
        
        # Chart title
        chart_title = QLabel("Inventory Items")
        chart_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        chart_title.setStyleSheet("color: #111827; border: none; font-style: italic;")
        chart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_layout.addWidget(chart_title)
        
        # Chart area
        self.chart_widget = BarChartWidget()
        chart_layout.addWidget(self.chart_widget)
        
        content_layout.addWidget(chart_container, 2)
        
        self.layout.addLayout(content_layout)

    def _create_kpi_card(self, value, title):
        """Create a KPI card widget and return both card and value label."""
        card = QFrame()
        card.setMinimumHeight(140)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)
        
        # Value label (large number)
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        value_label.setStyleSheet("border: none; color: #111827;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(value_label)
        
        # Title label
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))
        title_label.setStyleSheet("border: none; color: #6b7280; font-weight: 500; font-style: italic;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)
        
        return card, value_label
    
    def update_kpis(self, inventory_value, inventory_items, wastages):
        """Update the KPI values."""
        self.inv_value_label.setText(str(inventory_value))
        self.inv_items_label.setText(str(inventory_items))
        self.wastages_label.setText(str(wastages))
    
    def update_chart(self, items_data):
        """Update the bar chart with new data."""
        self.chart_widget.set_data(items_data)


class BarChartWidget(QWidget):
    """Simple horizontal bar chart widget for displaying inventory items."""
    
    def __init__(self):
        super().__init__()
        self.data = []  # List of tuples: (item_name, quantity)
        self.setMinimumHeight(300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    
    def set_data(self, data):
        """Set chart data and trigger repaint.
        
        Args:
            data: List of dicts with 'name' and 'quantity' keys
        """
        self.data = [(item.get('name', 'Unknown'), item.get('stock_qty', 0)) for item in data[:4]]
        self.update()
    
    def paintEvent(self, event):
        """Paint the bar chart."""
        if not self.data:
            # Show placeholder text if no data
            painter = QPainter(self)
            painter.setPen(QColor("#9ca3af"))
            painter.setFont(QFont("Arial", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No inventory data available")
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Chart dimensions
        width = self.width()
        height = self.height()
        margin = 40
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Find max value for scaling
        max_value = max([qty for _, qty in self.data]) if self.data else 1
        if max_value == 0:
            max_value = 1
        
        # Calculate bar height and spacing
        num_bars = len(self.data)
        bar_spacing = 15
        bar_height = (chart_height - (num_bars - 1) * bar_spacing) / num_bars
        
        # Draw bars
        for i, (name, quantity) in enumerate(self.data):
            y = margin + i * (bar_height + bar_spacing)
            bar_width = (quantity / max_value) * chart_width * 0.8  # 80% of chart width
            
            # Draw bar
            painter.setBrush(QColor("#22d3ee"))  # Cyan color
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(margin, int(y), int(bar_width), int(bar_height), 4, 4)
            
            # Draw item name on the left
            painter.setPen(QColor("#111827"))
            painter.setFont(QFont("Arial", 10))
            text_rect = painter.boundingRect(0, int(y), margin - 5, int(bar_height), 
                                            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, 
                                            name)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, 
                           name if len(name) <= 15 else name[:12] + "...")
        
        # Draw scale on bottom
        painter.setPen(QColor("#6b7280"))
        painter.setFont(QFont("Arial", 9))
        scale_y = height - 20
        for i in range(5):
            value = int(max_value * i / 4)
            x = margin + (chart_width * 0.8 * i / 4)
            painter.drawText(int(x) - 15, scale_y, 30, 20, 
                           Qt.AlignmentFlag.AlignCenter, str(value))
