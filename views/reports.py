from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QComboBox, QDialog, QMessageBox, QTextEdit, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt as QtCore

# --- Shared Style Constants ---
STYLE_NAVY = "#111827"
STYLE_BLUE = "#0056b3"
STYLE_BORDER = "#d1d5db"
STYLE_BG_LIGHT = "#f9fafb"


class ViewReportDialog(QDialog):
    """Dialog for viewing generated reports."""
    
    def __init__(self, report_data, parent=None):
        super().__init__(parent)
        self.report_data = report_data
        self.setWindowTitle("VIEW REPORT")
        self.setMinimumSize(900, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.setStyleSheet("QDialog { background-color: white; }")

        # Title
        title = QLabel(self.report_data.get('title', 'REPORT'))
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {STYLE_NAVY}; padding-bottom: 10px; border-bottom: 2px solid {STYLE_BORDER};")
        layout.addWidget(title)

        # Report Info
        info_frame = QFrame()
        info_layout = QHBoxLayout(info_frame)
        
        date_label = QLabel(f"Date Range: {self.report_data.get('date_range', 'N/A')}")
        date_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        info_layout.addWidget(date_label)
        
        info_layout.addStretch()
        
        generated_label = QLabel(f"Generated: {self.report_data.get('generated_at', 'N/A')}")
        generated_label.setStyleSheet(f"color: #6b7280;")
        info_layout.addWidget(generated_label)
        
        layout.addWidget(info_frame)

        # Summary Section
        if 'summary' in self.report_data:
            summary_frame = QFrame()
            summary_frame.setStyleSheet(f"background-color: {STYLE_BG_LIGHT}; border: 1px solid {STYLE_BORDER}; border-radius: 4px; padding: 15px;")
            summary_layout = QVBoxLayout(summary_frame)
            
            summary_title = QLabel("SUMMARY")
            summary_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            summary_title.setStyleSheet(f"color: {STYLE_NAVY};")
            summary_layout.addWidget(summary_title)
            
            for key, value in self.report_data['summary'].items():
                item_label = QLabel(f"{key}: {value}")
                item_label.setStyleSheet(f"color: {STYLE_NAVY}; padding: 2px;")
                summary_layout.addWidget(item_label)
            
            layout.addWidget(summary_frame)

        # Data Table
        if 'table_data' in self.report_data:
            table = QTableWidget()
            table.setStyleSheet(f"""
                QTableWidget {{
                    background-color: white;
                    border: 1px solid {STYLE_BORDER};
                    border-radius: 4px;
                    color: {STYLE_NAVY};
                }}
                QTableWidget::item {{
                    padding: 8px;
                    color: {STYLE_NAVY};
                }}
                QHeaderView::section {{
                    background-color: {STYLE_BG_LIGHT};
                    color: {STYLE_NAVY};
                    font-weight: bold;
                    padding: 8px;
                    border: none;
                }}
            """)
            
            headers = self.report_data.get('headers', [])
            rows = self.report_data['table_data']
            
            table.setColumnCount(len(headers))
            table.setRowCount(len(rows))
            table.setHorizontalHeaderLabels(headers)
            
            for r_idx, row in enumerate(rows):
                for c_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(r_idx, c_idx, item)
            
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            layout.addWidget(table)

        # Close button
        close_btn = QPushButton("CLOSE")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_BLUE};
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #004494;
            }}
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class GenerateReportDialog(QDialog):
    """Dialog for generating custom reports."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GENERATE REPORT")
        self.setFixedSize(500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Set dialog background
        self.setStyleSheet("QDialog { background-color: white; }")

        # Title
        title = QLabel("GENERATE REPORT")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {STYLE_NAVY}; padding-bottom: 10px; border-bottom: 2px solid {STYLE_BORDER};")
        layout.addWidget(title)

        # Form fields
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Report Type
        type_label = QLabel("REPORT TYPE:")
        type_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(type_label)
        
        self.type_cb = QComboBox()
        self.type_cb.addItems([
            "Stock Summary",
            "Usage Data",
            "Purchasing Trends",
            "Low Stock Alert",
            "Damage Reports",
            "Supplier Performance"
        ])
        self.type_cb.setFixedHeight(35)
        self.type_cb.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        form_layout.addWidget(self.type_cb)

        # Date Range
        date_label = QLabel("DATE RANGE:")
        date_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(date_label)
        
        self.range_cb = QComboBox()
        self.range_cb.addItems(["Last 7 Days", "Last 30 Days", "Last 3 Months", "Last 6 Months", "This Year", "All Time"])
        self.range_cb.setFixedHeight(35)
        self.range_cb.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        form_layout.addWidget(self.range_cb)

        # Format
        format_label = QLabel("FORMAT:")
        format_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold;")
        form_layout.addWidget(format_label)
        
        self.format_cb = QComboBox()
        self.format_cb.addItems(["PDF", "Excel (XLSX)", "CSV"])
        self.format_cb.setFixedHeight(35)
        self.format_cb.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                background-color: white;
                color: {STYLE_NAVY};
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        form_layout.addWidget(self.format_cb)

        layout.addLayout(form_layout)
        layout.addStretch()

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
        
        self.generate_btn = QPushButton("GENERATE")
        self.generate_btn.setFixedSize(120, 40)
        self.generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_NAVY};
                color: white;
                border: none;
                font-weight: bold;
                border-radius: 4px;
            }}
            QPushButton:hover {{ background-color: {STYLE_BLUE}; }}
        """)
        self.generate_btn.clicked.connect(self.accept)
        
        button_row.addWidget(self.cancel_btn)
        button_row.addWidget(self.generate_btn)
        layout.addLayout(button_row)

    def get_data(self):
        """Return the form data."""
        return {
            'report_type': self.type_cb.currentText(),
            'date_range': self.range_cb.currentText(),
            'format': self.format_cb.currentText()
        }


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_role = None
        self.current_department = None
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        # Header with Title
        header_layout = QHBoxLayout()
        
        title = QLabel("USAGE REPORTS")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {STYLE_NAVY};")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.layout.addLayout(header_layout)

        # Action Buttons Row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        self.btn_view_reports = QPushButton("STOCK LEVELS")
        self.btn_generate_reports = QPushButton("VIEW REPORTS")
        self.btn_summary = QPushButton("LOW STOCK ALERT")
        self.btn_export = QPushButton("EXPORT REPORT")

        self.actions = [self.btn_view_reports, self.btn_generate_reports, self.btn_summary, self.btn_export]
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
        
        # Create actions container to hide for Department role if needed
        self.actions_container = QWidget()
        self.actions_container.setLayout(actions_layout)
        self.layout.addWidget(self.actions_container)

        # Filters Row
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(12)
        
        # Year Filter
        year_label = QLabel("YEAR:")
        year_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 11px;")
        filters_layout.addWidget(year_label)
        
        self.year_filter = QComboBox()
        current_year = QDate.currentDate().year()
        years = [str(current_year - i) for i in range(5)]
        self.year_filter.addItems(years)
        self.year_filter.setFixedWidth(120)
        self.year_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: white;
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                color: {STYLE_NAVY};
                font-size: 11px;
                font-weight: bold;
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        filters_layout.addWidget(self.year_filter)
        
        filters_layout.addSpacing(20)
        
        # Month Filter
        month_label = QLabel("MONTH:")
        month_label.setStyleSheet(f"color: {STYLE_NAVY}; font-weight: bold; font-size: 11px;")
        filters_layout.addWidget(month_label)
        
        self.month_filter = QComboBox()
        months = ["All", "January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        self.month_filter.addItems(months)
        self.month_filter.setFixedWidth(150)
        self.month_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: white;
                border: 2px solid {STYLE_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                color: {STYLE_NAVY};
                font-size: 11px;
                font-weight: bold;
            }}
            QComboBox:hover {{ border-color: {STYLE_BLUE}; }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {STYLE_NAVY};
                selection-background-color: {STYLE_BG_LIGHT};
                selection-color: {STYLE_NAVY};
            }}
        """)
        filters_layout.addWidget(self.month_filter)
        
        filters_layout.addStretch()
        self.layout.addLayout(filters_layout)

        # Bar Chart Container - Full Width
        chart_container = QFrame()
        chart_container.setStyleSheet(f"background-color: white; border: 1px solid {STYLE_BORDER}; border-radius: 2px;")
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(20, 20, 20, 20)

        # Bar Chart
        self.bar_chart = self.create_sample_bar_chart()
        self.bar_view = QChartView(self.bar_chart)
        self.bar_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.bar_view.setStyleSheet("background-color: transparent; border: none;")
        self.bar_view.setMinimumHeight(400)
        chart_layout.addWidget(self.bar_view)

        self.layout.addWidget(chart_container)

    def update_charts(self, inventory_data):
        """Update bar chart with real data from database."""
        # Update bar chart with all inventory items
        self.bar_chart = self.create_inventory_bar_chart(inventory_data)
        self.bar_view.setChart(self.bar_chart)

    def create_inventory_bar_chart(self, inventory_data):
        """Create a bar chart showing all inventory stock levels."""
        bar_set = QBarSet("Stock Quantity")
        bar_set.setColor(QColor(STYLE_BLUE))
        
        categories = []
        
        if not inventory_data or len(inventory_data) == 0:
            # Show placeholder if no data
            bar_set.append(0)
            categories.append("No Data")
        else:
            # Add all items to bar chart
            for item in inventory_data:
                item_name = item.get('name', 'Unknown')
                stock_qty = item.get('stock_qty', 0)
                
                bar_set.append(stock_qty)
                categories.append(item_name)
        
        series = QBarSeries()
        series.append(bar_set)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("ALL STOCK LEVELS")
        chart.setTitleFont(QFont("Arial", 16, QFont.Weight.Bold))
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Category axis (X-axis)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsAngle(-45)  # Rotate labels for better readability
        axis_x.setLabelsColor(QColor(STYLE_NAVY))
        axis_x.setLabelsFont(QFont("Arial", 11))  # Bigger readable font size
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        # Value axis (Y-axis)
        axis_y = QValueAxis()
        axis_y.setLabelsColor(QColor(STYLE_NAVY))
        axis_y.setLabelsFont(QFont("Arial", 11))  # Bigger readable font size
        axis_y.setGridLineColor(QColor(STYLE_BORDER))
        axis_y.setTitleText("Quantity")
        axis_y.setTitleFont(QFont("Arial", 11, QFont.Weight.Bold))
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        chart.setBackgroundVisible(False)
        
        return chart

    def create_sample_bar_chart(self):
        """Create a sample bar chart for initial display."""
        bar_set = QBarSet("Stock Quantity")
        bar_set.setColor(QColor(STYLE_BLUE))
        bar_set.append(0)
        
        series = QBarSeries()
        series.append(bar_set)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("ALL STOCK LEVELS")
        chart.setTitleFont(QFont("Arial", 16, QFont.Weight.Bold))
        
        axis_x = QBarCategoryAxis()
        axis_x.append(["Loading..."])
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setTitleText("Quantity")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        
        chart.legend().setVisible(False)
        chart.setBackgroundVisible(False)
        
        return chart
