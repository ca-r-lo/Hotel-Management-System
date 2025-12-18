# Department Users Setup

## Overview
The HMS system now supports multiple department users, each with access to their specific department's inventory.

## Department User Accounts

### 1. Housekeeping Department
- **Name:** Housekeeping Manager
- **Email:** housekeeping@stash.com
- **Password:** housekeeping123
- **Department:** Housekeeping
- **Access:** Can view and manage Housekeeping inventory items only

### 2. Kitchen Department
- **Name:** Kitchen Manager
- **Email:** kitchen@stash.com
- **Password:** kitchen123
- **Department:** Kitchen
- **Access:** Can view and manage Kitchen inventory items only

### 3. Front Desk Department
- **Name:** Front Desk Manager
- **Email:** frontdesk@stash.com
- **Password:** frontdesk123
- **Department:** Front Desk
- **Access:** Can view and manage Front Desk inventory items only

### 4. Maintenance Department
- **Name:** Maintenance Manager
- **Email:** maintenance@stash.com
- **Password:** maintenance123
- **Department:** Maintenance
- **Access:** Can view and manage Maintenance inventory items only

## Features for Department Users

### Dashboard
- View department-specific KPIs:
  - Inventory Value (for their department only)
  - Inventory Items count
  - Wastages
  - Low Stock alerts

### Inventory Page
- Category filter pre-set to their department
- Can view only items in their department category
- Action buttons (ADD STOCKS, DISTRIBUTE STOCKS, etc.) are hidden
- Category dropdown is clickable and can be used to filter

### Requests Page
- Can create stock requests to Purchase Admin
- Can view their department's request history

### Reports
- Can view usage reports for their department

### Messages
- Can send/receive messages (likely to/from Purchase Admin)

## Adding More Departments

To add a new department:

1. Add the department category to items in the database
2. Create a new user with:
   - role: "Department"
   - department: "[Department Name]"
3. Add the department name to the category filter in `views/inventory.py`

## Technical Implementation

### Database Changes
- Added `department` column to `users` table
- Updated `authenticate()` to return department information
- Department users are filtered by their assigned department category

### Code Updates
- `models/user.py`: Returns department in authentication
- `controllers/login.py`: Passes department to dashboard
- `views/dashboard.py`: Uses department for filtering KPIs and inventory
- `views/inventory.py`: Filters inventory by department category
