"""Controller for Department Overview functionality."""
from models.purchase import DashboardModel, ItemModel


class DeptOverviewController:
    """Controller for handling department overview operations."""

    def __init__(self, view):
        """Initialize the controller with the view.
        
        Args:
            view: The DepartmentOverviewPage instance
        """
        self.view = view
        self.dashboard_model = DashboardModel()
        
        # Populate departments from database
        self.populate_departments()
        
        # Connect signals
        self.view.dept_selector.currentTextChanged.connect(self.on_department_changed)
        
        # Initial load
        self.load_department_data("All Departments")
    
    def populate_departments(self):
        """Populate department dropdown with actual departments from database."""
        try:
            # Get all unique categories/departments from items table
            item_model = ItemModel()
            items = item_model.list_items()
            
            # Extract unique categories
            departments = set()
            for item in items:
                category = item.get('category')
                if category and category not in ['General', 'Uncategorized']:
                    departments.add(category)
            
            # Sort departments alphabetically
            sorted_departments = sorted(list(departments))
            
            # Add to combobox (All Departments is already added in view)
            for dept in sorted_departments:
                self.view.dept_selector.addItem(dept)
                
        except Exception as e:
            print(f"Error populating departments: {e}")
            # Add default departments if database query fails
            default_depts = ["Housekeeping", "Kitchen", "Front Desk", "Maintenance"]
            for dept in default_depts:
                self.view.dept_selector.addItem(dept)
    
    def on_department_changed(self, department_name):
        """Handle department selection change."""
        self.load_department_data(department_name)
    
    def load_department_data(self, department_name):
        """Load and display data for the selected department.
        
        Args:
            department_name: Name of the department to display data for
        """
        try:
            # Get department-specific data
            if department_name == "All Departments":
                dept_filter = None
            else:
                dept_filter = department_name
            
            # Get KPI values
            kpis = self.dashboard_model.get_department_kpis(dept_filter)
            
            # Update KPI cards
            self.view.update_kpis(
                inventory_value=kpis.get('inventory_value', '₱0.00'),
                inventory_items=kpis.get('inventory_items', 0),
                wastages=kpis.get('wastages', 0)
            )
            
            # Get top items for chart
            items_data = self.dashboard_model.get_department_top_items(dept_filter)
            self.view.update_chart(items_data)
            
        except Exception as e:
            print(f"Error loading department data: {e}")
            # Set default values on error
            self.view.update_kpis("₱0.00", 0, 0)
            self.view.update_chart([])
