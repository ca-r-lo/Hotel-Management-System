from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import QDate
from views.reports import GenerateReportDialog, ViewReportDialog
from models.purchase import PurchaseModel, ItemModel, DamageModel
from datetime import datetime, timedelta
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


class ReportsController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        
        # Connect action buttons - updated button names
        self.view.btn_view_reports.clicked.connect(self.handle_stock_summary)
        self.view.btn_generate_reports.clicked.connect(self.handle_usage_data)
        self.view.btn_summary.clicked.connect(self.handle_purchasing_trends)
        self.view.btn_export.clicked.connect(self.handle_export_report)
        
        # Connect filters
        self.view.year_filter.currentTextChanged.connect(self.handle_filter_change)
        self.view.month_filter.currentTextChanged.connect(self.handle_filter_change)
        
        # Load initial charts
        self.refresh_charts()
    
    def handle_filter_change(self):
        """Handle year/month filter changes."""
        self.refresh_charts()
    
    def refresh_charts(self):
        """Refresh chart data based on current filters."""
        try:
            year = self.view.year_filter.currentText()
            month = self.view.month_filter.currentText()
            
            # Fetch inventory data grouped by category
            inventory_data = self.get_inventory_by_category()
            
            # Fetch purchase trend data
            trend_data = self.get_purchase_trends(year, month)
            
            # Update the charts in the view
            self.view.update_charts(inventory_data, trend_data)
            
        except Exception as e:
            print(f"Error refreshing charts: {e}")
    
    def get_inventory_by_category(self):
        """Get inventory value grouped by category."""
        try:
            item_model = ItemModel()
            items = item_model.list_items()
            
            # Group by category and calculate total value
            category_totals = {}
            for item in items:
                category = item.get('category') or "Uncategorized"
                stock_qty = item.get('stock_qty') or 0
                unit_cost = item.get('unit_cost') or 0
                total_value = stock_qty * unit_cost
                
                if category in category_totals:
                    category_totals[category] += total_value
                else:
                    category_totals[category] = total_value
            
            # Convert to list of tuples for pie chart
            return [(cat, val) for cat, val in category_totals.items() if val > 0]
        except Exception as e:
            print(f"Error getting inventory by category: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_purchase_trends(self, year, month):
        """Get purchase trends over time."""
        try:
            purchases = self.model.list_purchases()
            
            # Group purchases by month and status
            from datetime import datetime
            
            monthly_data = {
                "Pending": {},
                "Delivered": {},
                "Cancelled": {}
            }
            
            for purchase in purchases:
                created_at = purchase.get('created_at')
                status = purchase.get('status', '').capitalize()
                total_amount = purchase.get('total_amount') or 0
                
                if created_at:
                    # Parse the date
                    if isinstance(created_at, str):
                        try:
                            purchase_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            try:
                                purchase_date = datetime.strptime(created_at, "%Y-%m-%d")
                            except ValueError:
                                continue
                    else:
                        purchase_date = created_at
                    
                    # Filter by year if specified
                    if year != "All" and str(purchase_date.year) != year:
                        continue
                    
                    # Filter by month if specified
                    if month != "All":
                        month_num = ["January", "February", "March", "April", "May", "June",
                                   "July", "August", "September", "October", "November", "December"].index(month) + 1
                        if purchase_date.month != month_num:
                            continue
                    
                    month_key = purchase_date.month
                    
                    if status in monthly_data:
                        if month_key in monthly_data[status]:
                            monthly_data[status][month_key] += total_amount
                        else:
                            monthly_data[status][month_key] = total_amount
            
            # Convert to format expected by line chart
            trend_data = {}
            for status, months in monthly_data.items():
                if months:  # Only include if there's data
                    points = sorted([(month, amount) for month, amount in months.items()])
                    trend_data[status] = points
            
            return trend_data
        except Exception as e:
            print(f"Error getting purchase trends: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def handle_stock_summary(self):
        """Generate and display stock summary report."""
        try:
            item_model = ItemModel()
            items = item_model.list_items()
            
            # Calculate summary statistics
            total_items = len(items)
            total_value = sum((item.get('stock_qty', 0) * item.get('unit_cost', 0)) for item in items)
            low_stock_count = sum(1 for item in items if item.get('stock_qty', 0) <= item.get('min_stock', 0))
            out_of_stock = sum(1 for item in items if item.get('stock_qty', 0) == 0)
            
            # Group by category
            category_stats = {}
            for item in items:
                category = item.get('category') or "Uncategorized"
                if category not in category_stats:
                    category_stats[category] = {'count': 0, 'value': 0, 'qty': 0}
                category_stats[category]['count'] += 1
                category_stats[category]['value'] += (item.get('stock_qty', 0) * item.get('unit_cost', 0))
                category_stats[category]['qty'] += item.get('stock_qty', 0)
            
            # Prepare report data
            report_data = {
                'title': 'STOCK SUMMARY REPORT',
                'date_range': 'Current Stock Levels',
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'summary': {
                    'Total Items': total_items,
                    'Total Stock Value': f'₱{total_value:,.2f}',
                    'Low Stock Items': low_stock_count,
                    'Out of Stock Items': out_of_stock,
                    'Categories': len(category_stats)
                },
                'headers': ['CATEGORY', 'ITEMS COUNT', 'TOTAL QUANTITY', 'TOTAL VALUE'],
                'table_data': [
                    [cat, stats['count'], stats['qty'], f"₱{stats['value']:,.2f}"]
                    for cat, stats in category_stats.items()
                ]
            }
            
            # Show report dialog
            dlg = ViewReportDialog(report_data, self.view)
            dlg.exec()
            
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to generate stock summary:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def handle_usage_data(self):
        """Generate and display usage data report."""
        try:
            damage_model = DamageModel()
            damages = damage_model.list_damages()
            
            item_model = ItemModel()
            
            # Calculate usage statistics
            total_damages = len(damages)
            
            # Group by category
            category_damages = {}
            total_qty_damaged = 0
            
            for damage in damages:
                item_id = damage.get('item_id')
                category = damage.get('category', 'Unknown')
                quantity = damage.get('quantity', 0)
                total_qty_damaged += quantity
                
                if category not in category_damages:
                    category_damages[category] = {'count': 0, 'quantity': 0}
                category_damages[category]['count'] += 1
                category_damages[category]['quantity'] += quantity
            
            # Prepare report data
            report_data = {
                'title': 'USAGE DATA REPORT',
                'date_range': 'All Damage Reports',
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'summary': {
                    'Total Damage Reports': total_damages,
                    'Total Quantity Damaged': total_qty_damaged,
                    'Damage Categories': len(category_damages)
                },
                'headers': ['DAMAGE CATEGORY', 'REPORT COUNT', 'TOTAL QUANTITY'],
                'table_data': [
                    [cat, stats['count'], stats['quantity']]
                    for cat, stats in category_damages.items()
                ]
            }
            
            # Show report dialog
            dlg = ViewReportDialog(report_data, self.view)
            dlg.exec()
            
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to generate usage data:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def handle_purchasing_trends(self):
        """Generate and display purchasing trends report."""
        try:
            purchases = self.model.list_purchases()
            
            # Calculate trends statistics
            total_purchases = len(purchases)
            total_amount = sum(p.get('total_amount', 0) for p in purchases)
            
            # Group by status
            status_stats = {}
            for purchase in purchases:
                status = purchase.get('status', 'Unknown').capitalize()
                amount = purchase.get('total_amount', 0)
                
                if status not in status_stats:
                    status_stats[status] = {'count': 0, 'amount': 0}
                status_stats[status]['count'] += 1
                status_stats[status]['amount'] += amount
            
            # Group by month
            monthly_stats = {}
            for purchase in purchases:
                created_at = purchase.get('created_at')
                if created_at:
                    if isinstance(created_at, str):
                        try:
                            purchase_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            try:
                                purchase_date = datetime.strptime(created_at, "%Y-%m-%d")
                            except ValueError:
                                continue
                    else:
                        purchase_date = created_at
                    
                    month_key = purchase_date.strftime('%Y-%m')
                    amount = purchase.get('total_amount', 0)
                    
                    if month_key not in monthly_stats:
                        monthly_stats[month_key] = {'count': 0, 'amount': 0}
                    monthly_stats[month_key]['count'] += 1
                    monthly_stats[month_key]['amount'] += amount
            
            # Prepare report data
            report_data = {
                'title': 'PURCHASING TRENDS REPORT',
                'date_range': 'All Purchase Orders',
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'summary': {
                    'Total Purchase Orders': total_purchases,
                    'Total Amount': f'₱{total_amount:,.2f}',
                    'Average Order Value': f'₱{(total_amount/total_purchases if total_purchases > 0 else 0):,.2f}'
                },
                'headers': ['MONTH', 'ORDER COUNT', 'TOTAL AMOUNT'],
                'table_data': [
                    [month, stats['count'], f"₱{stats['amount']:,.2f}"]
                    for month, stats in sorted(monthly_stats.items(), reverse=True)
                ]
            }
            
            # Show report dialog
            dlg = ViewReportDialog(report_data, self.view)
            dlg.exec()
            
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to generate purchasing trends:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            msg.exec()
    
    def handle_export_report(self):
        """Export report to CSV, Excel, or PDF file."""
        print("Export button clicked!")  # Debug
        try:
            # First, ask user to select report type and format
            dlg = GenerateReportDialog(self.view)
            print("Dialog created")  # Debug
            
            # Wait for user to click generate or cancel
            if dlg.exec():
                print("Dialog accepted")  # Debug
                data = dlg.get_data()
                report_type = data['report_type']
                format_type = data['format']
                print(f"Report type: {report_type}, Format: {format_type}")  # Debug
                
                # Set file extension based on format
                if format_type == "CSV":
                    file_filter = "CSV Files (*.csv)"
                    default_ext = ".csv"
                elif format_type == "Excel":
                    file_filter = "Excel Files (*.xlsx)"
                    default_ext = ".xlsx"
                elif format_type == "PDF":
                    file_filter = "PDF Files (*.pdf)"
                    default_ext = ".pdf"
                else:
                    file_filter = "All Files (*.*)"
                    default_ext = ""
                
                # Ask user where to save the file
                default_filename = f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{default_ext}"
                file_path, _ = QFileDialog.getSaveFileName(
                    self.view,
                    "Export Report",
                    default_filename,
                    file_filter
                )
                print(f"File path: {file_path}")  # Debug
                
                # If user selected a path, generate and save the report
                if file_path:
                    # Generate the appropriate report data
                    report_data = None
                    if report_type == "Stock Summary":
                        report_data = self.generate_stock_summary_data()
                    elif report_type == "Usage Data":
                        report_data = self.generate_usage_data()
                    elif report_type == "Purchasing Trends":
                        report_data = self.generate_purchasing_trends_data()
                    elif report_type == "Low Stock Alert":
                        report_data = self.generate_low_stock_data()
                    elif report_type == "Damage Reports":
                        report_data = self.generate_usage_data()  # Same as usage data
                    elif report_type == "Supplier Performance":
                        report_data = self.generate_supplier_performance_data()
                    
                    if report_data:
                        # Save based on format
                        if format_type == "CSV":
                            self.export_to_csv(file_path, report_type, report_data)
                        elif format_type == "Excel":
                            self.export_to_excel(file_path, report_type, report_data)
                        elif format_type == "PDF":
                            self.export_to_pdf(file_path, report_type, report_data)
                        
                        msg = QMessageBox(self.view)
                        msg.setIcon(QMessageBox.Icon.Information)
                        msg.setWindowTitle("Success")
                        msg.setText(f"Report exported successfully to {format_type}!\n\nSaved to:\n{file_path}")
                        msg.setStyleSheet("QLabel { color: #000000; }")
                        msg.exec()
                        
        except Exception as e:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to export report:\n{e}")
            msg.setStyleSheet("QLabel { color: #000000; }")
            import traceback
            traceback.print_exc()
            msg.exec()
    
    def generate_stock_summary_data(self):
        """Generate stock summary data for export."""
        item_model = ItemModel()
        items = item_model.list_items()
        
        return {
            'headers': ['Item Name', 'SKU', 'Category', 'Stock Qty', 'Unit Cost', 'Total Value', 'Min Stock', 'Status'],
            'table_data': [
                [
                    item.get('name', ''),
                    item.get('sku', ''),
                    item.get('category', 'Uncategorized'),
                    item.get('stock_qty', 0),
                    item.get('unit_cost', 0),
                    item.get('stock_qty', 0) * item.get('unit_cost', 0),
                    item.get('min_stock', 0),
                    'Low Stock' if item.get('stock_qty', 0) <= item.get('min_stock', 0) else 'In Stock'
                ]
                for item in items
            ]
        }
    
    def generate_usage_data(self):
        """Generate usage data for export."""
        damage_model = DamageModel()
        damages = damage_model.list_damages()
        
        return {
            'headers': ['Damage ID', 'Purchase ID', 'Category', 'Quantity', 'Reason', 'Status', 'Created By', 'Date'],
            'table_data': [
                [
                    damage.get('id', ''),
                    damage.get('purchase_id', ''),
                    damage.get('category', ''),
                    damage.get('quantity', 0),
                    damage.get('reason', ''),
                    damage.get('status', ''),
                    damage.get('created_by', ''),
                    damage.get('created_at', '')
                ]
                for damage in damages
            ]
        }
    
    def generate_purchasing_trends_data(self):
        """Generate purchasing trends data for export."""
        purchases = self.model.list_purchases()
        
        return {
            'headers': ['Order ID', 'Supplier', 'Status', 'Total Amount', 'Expected Date', 'Created By', 'Created At'],
            'table_data': [
                [
                    purchase.get('id', ''),
                    purchase.get('supplier_name', ''),
                    purchase.get('status', ''),
                    purchase.get('total_amount', 0),
                    purchase.get('expected_date', ''),
                    purchase.get('created_by', ''),
                    purchase.get('created_at', '')
                ]
                for purchase in purchases
            ]
        }
    
    def generate_low_stock_data(self):
        """Generate low stock alert data for export."""
        item_model = ItemModel()
        items = item_model.list_items()
        
        # Filter only low stock items
        low_stock_items = [item for item in items if item.get('stock_qty', 0) <= item.get('min_stock', 0)]
        
        return {
            'headers': ['Item Name', 'SKU', 'Category', 'Current Stock', 'Min Stock', 'Reorder Needed', 'Unit Cost'],
            'table_data': [
                [
                    item.get('name', ''),
                    item.get('sku', ''),
                    item.get('category', 'Uncategorized'),
                    item.get('stock_qty', 0),
                    item.get('min_stock', 0),
                    max(0, item.get('min_stock', 0) - item.get('stock_qty', 0)),
                    f"₱{item.get('unit_cost', 0):,.2f}"
                ]
                for item in low_stock_items
            ]
        }
    
    def generate_supplier_performance_data(self):
        """Generate supplier performance data for export."""
        from models.purchase import SupplierModel
        supplier_model = SupplierModel()
        suppliers = supplier_model.list_suppliers()
        purchases = self.model.list_purchases()
        
        # Calculate stats per supplier
        supplier_stats = {}
        for purchase in purchases:
            supplier_id = purchase.get('supplier_id')
            if supplier_id:
                if supplier_id not in supplier_stats:
                    supplier_stats[supplier_id] = {
                        'total_orders': 0,
                        'total_amount': 0,
                        'delivered': 0,
                        'pending': 0,
                        'cancelled': 0
                    }
                supplier_stats[supplier_id]['total_orders'] += 1
                supplier_stats[supplier_id]['total_amount'] += purchase.get('total_amount', 0)
                
                status = purchase.get('status', '').lower()
                if status == 'delivered':
                    supplier_stats[supplier_id]['delivered'] += 1
                elif status == 'pending':
                    supplier_stats[supplier_id]['pending'] += 1
                elif status == 'cancelled':
                    supplier_stats[supplier_id]['cancelled'] += 1
        
        return {
            'headers': ['Supplier Name', 'Contact Person', 'Total Orders', 'Total Amount', 'Delivered', 'Pending', 'Cancelled'],
            'table_data': [
                [
                    supplier.get('name', ''),
                    supplier.get('contact_name', ''),
                    supplier_stats.get(supplier.get('id'), {}).get('total_orders', 0),
                    f"₱{supplier_stats.get(supplier.get('id'), {}).get('total_amount', 0):,.2f}",
                    supplier_stats.get(supplier.get('id'), {}).get('delivered', 0),
                    supplier_stats.get(supplier.get('id'), {}).get('pending', 0),
                    supplier_stats.get(supplier.get('id'), {}).get('cancelled', 0)
                ]
                for supplier in suppliers
            ]
        }
    
    def export_to_csv(self, file_path, report_type, report_data):
        """Export report data to CSV file."""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write title and metadata
            writer.writerow([f"Report Type: {report_type}"])
            writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
            writer.writerow([])  # Empty row
            # Write headers and data
            writer.writerow(report_data['headers'])
            writer.writerows(report_data['table_data'])
    
    def export_to_excel(self, file_path, report_type, report_data):
        """Export report data to Excel file."""
        wb = Workbook()
        ws = wb.active
        ws.title = "Report"
        
        # Title
        ws['A1'] = f"Report Type: {report_type}"
        ws['A1'].font = Font(bold=True, size=14)
        ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ws['A2'].font = Font(size=10, italic=True)
        
        # Headers (starting at row 4)
        header_fill = PatternFill(start_color="0056b3", end_color="0056b3", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for col_idx, header in enumerate(report_data['headers'], 1):
            cell = ws.cell(row=4, column=col_idx)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Data rows
        for row_idx, row_data in enumerate(report_data['table_data'], 5):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.value = value
                cell.alignment = Alignment(horizontal='left', vertical='center')
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        wb.save(file_path)
    
    def export_to_pdf(self, file_path, report_type, report_data):
        """Export report data to PDF file."""
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"<b>{report_type}</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Metadata
        meta = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        elements.append(meta)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Prepare table data
        table_data = [report_data['headers']] + report_data['table_data']
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            # Header row style
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0056b3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # Data rows style
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        elements.append(table)
        doc.build(elements)

