# HMS User Roles and Access Control

## User Accounts

The system now supports three different user roles with different access levels:

### 1. Purchase Admin
- **Email:** purchaseadmin@stash.com
- **Password:** 123
- **Role:** Purchase Admin
- **Access Level:** Full Access

**Available Pages:**
- ✅ Dashboard
- ✅ Purchase (Order Stocks, Suppliers, Track Orders, Report Damages)
- ✅ Inventory (Manage stock levels, add/edit items)
- ✅ Reports (View analytics, export data)
- ✅ Messages (Internal communication)

**Description:** Has complete access to all features of the system. Can manage purchases, inventory, view reports, and communicate with other users.

---

### 2. Owner
- **Email:** owner@stash.com
- **Password:** 123
- **Role:** Owner
- **Access Level:** Reports & Analytics Focused

**Available Pages:**
- ✅ Dashboard
- ✅ Reports (View analytics, export data)
- ✅ Messages (Internal communication)

**Restricted Pages:**
- ❌ Purchase
- ❌ Inventory

**Description:** Focused on oversight and analytics. Can view dashboard metrics, access detailed reports, and communicate with staff. Cannot directly manage purchases or inventory.

---

### 3. Department Manager
- **Email:** department@stash.com
- **Password:** 123
- **Role:** Department
- **Access Level:** Operational Access

**Available Pages:**
- ✅ Dashboard
- ✅ Purchase (Order Stocks, Suppliers, Track Orders, Report Damages)
- ✅ Inventory (Manage stock levels, add/edit items)
- ✅ Messages (Internal communication)

**Restricted Pages:**
- ❌ Reports

**Description:** Can perform day-to-day operations including managing purchases and inventory. Can communicate with other users but cannot access detailed analytics reports.

---

## Features

### Role-Based Navigation
- The sidebar navigation automatically shows/hides menu items based on the logged-in user's role
- Users only see the pages they have permission to access
- Attempting to access unauthorized pages is prevented at the UI level

### Logout Functionality
- A red "LOGOUT" button is available at the bottom of the sidebar for all users
- Clicking logout prompts for confirmation
- After logout, the user is returned to the login screen
- Login credentials are cleared for security

### User Profile Display
- The sidebar shows the logged-in user's name and role
- This helps users identify which account they're currently using

---

## Technical Implementation

### Role Configuration
Defined in `views/dashboard.py`:

```python
ROLE_PAGES = {
    'Purchase Admin': ['DASHBOARD', 'PURCHASE', 'INVENTORY', 'REPORTS', 'MESSAGES'],
    'Owner': ['DASHBOARD', 'REPORTS', 'MESSAGES'],
    'Department': ['DASHBOARD', 'PURCHASE', 'INVENTORY', 'MESSAGES']
}
```

### Database Schema
Users table structure:
- `id` - Unique identifier
- `email` - Login email
- `password` - User password (currently plain text - should be hashed in production)
- `full_name` - Display name
- `role` - User role (Purchase Admin, Owner, Department)

### Authentication Flow
1. User enters credentials on login screen
2. UserModel.authenticate() validates credentials against database
3. On success, DashboardWindow.update_ui_for_role() is called
4. UI is updated to show only authorized pages
5. User profile information is displayed in sidebar

---

## Security Notes

⚠️ **Important:** This implementation uses plain text passwords for demonstration purposes. In a production environment, you should:
- Hash passwords using bcrypt or similar
- Implement session management
- Add server-side authorization checks
- Use HTTPS for all communications
- Implement rate limiting on login attempts
- Add audit logging for user actions

---

## Testing Instructions

1. Start the application: `python main.py`
2. Login with each user account to verify role-based access
3. Verify that navigation buttons match the role's permissions
4. Test logout functionality
5. Verify that after logout, you can login as a different user

---

## Maintenance

To add a new user:
```sql
INSERT INTO users (email, password, full_name, role) VALUES 
('newemail@stash.com', '123', 'User Name', 'Purchase Admin');
```

To change a user's role:
```sql
UPDATE users SET role = 'Owner' WHERE email = 'user@stash.com';
```

To add a new role or modify permissions:
1. Update `ROLE_PAGES` dictionary in `views/dashboard.py`
2. Add the role to the database
3. Restart the application
