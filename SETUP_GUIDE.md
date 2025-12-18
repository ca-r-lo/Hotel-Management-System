# HMS Database Setup Guide

## Quick Start

### Step 1: Create Database and User

```bash
# Login to MariaDB/MySQL
mysql -u root -p

# Or if using MariaDB specifically
mariadb -u root -p
```

```sql
-- Create database
CREATE DATABASE hms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user and grant privileges
CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit
EXIT;
```

### Step 2: Run the Setup Script

```bash
# Run the SQL setup file
mysql -u hms_user -p hms_db < hms_setup.sql

# Or if using MariaDB
mariadb -u hms_user -p hms_db < hms_setup.sql
```

### Step 3: Configure the Application

Update `configs/db_config.json` with your database credentials:

```json
{
    "host": "localhost",
    "port": 3306,
    "user": "hms_user",
    "password": "your_secure_password",
    "database": "hms_db"
}
```

### Step 4: Run the Application

```bash
# Activate virtual environment (if using one)
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Run the application
python main.py
```

## Default User Accounts

| Role | Email | Password | Access |
|------|-------|----------|--------|
| **Owner** | owner@stash.com | owner123 | Dashboard, Trans History, Dept Overview, Reports, Messages |
| **Purchase Admin** | admin@stash.com | admin123 | Dashboard, Purchase, Inventory, Reports, Messages |
| **Housekeeping** | housekeeping@stash.com | housekeeping123 | Dashboard, Inventory (Housekeeping), Requests, Reports, Messages |
| **Kitchen** | kitchen@stash.com | kitchen123 | Dashboard, Inventory (Kitchen), Requests, Reports, Messages |
| **Front Desk** | frontdesk@stash.com | frontdesk123 | Dashboard, Inventory (Front Desk), Requests, Reports, Messages |
| **Maintenance** | maintenance@stash.com | maintenance123 | Dashboard, Inventory (Maintenance), Requests, Reports, Messages |

> ⚠️ **IMPORTANT**: Change these default passwords immediately after first login!

## What Gets Created

### Tables Created:
1. **users** - User accounts and authentication
2. **suppliers** - Supplier information
3. **items** - Inventory items
4. **purchases** - Purchase orders
5. **purchase_items** - Line items for purchases
6. **damages** - Damaged items tracking
7. **messages** - Internal messaging system
8. **requests** - Stock requests from departments

### Sample Data Inserted:
- ✅ 6 User accounts (Owner, Purchase Admin, 4 Department Managers)
- ✅ 3 Sample suppliers
- ✅ 14 Sample inventory items (across all departments)

## Verifying the Setup

```sql
-- Check all tables were created
SHOW TABLES;

-- Verify users
SELECT id, email, full_name, role, department FROM users;

-- Check suppliers
SELECT * FROM suppliers;

-- Check inventory items
SELECT id, name, category, stock_qty, min_stock FROM items;

-- Verify database structure
DESCRIBE users;
DESCRIBE items;
```

## Troubleshooting

### Connection Issues

**Error: Access denied for user**
```bash
# Make sure you granted privileges correctly
mysql -u root -p
GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;
```

**Error: Unknown database 'hms_db'**
```bash
# Create the database first
mysql -u root -p
CREATE DATABASE hms_db;
```

### Setup Script Issues

**Error: Table already exists**
- This is normal if running the script multiple times
- The script uses `CREATE TABLE IF NOT EXISTS` so it's safe to re-run
- User inserts might fail if users already exist (this is expected)

**Error: Duplicate entry for users**
```sql
-- If you need to reset users
DELETE FROM users;
-- Then run the setup script again
```

## Customization

### Adding More Users

```sql
-- Template for adding new users
INSERT INTO users (email, password, full_name, role, department) VALUES 
('newemail@stash.com', 'password123', 'User Full Name', 'Role', 'Department');

-- Role options: 'Owner', 'Purchase Admin', 'Department'
-- Department options: 'Housekeeping', 'Kitchen', 'Front Desk', 'Maintenance', or NULL
```

### Adding More Departments

```sql
-- 1. Add a new user with the department
INSERT INTO users (email, password, full_name, role, department) VALUES 
('spa@stash.com', 'spa123', 'Spa Manager', 'Department', 'Spa');

-- 2. Add items for that department
INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Massage Oil', 'SPA-001', 'bottles', 20.00, 50, 25, 'Spa');
```

### Resetting the Database

```bash
# Complete reset (WARNING: Deletes all data!)
mysql -u root -p

DROP DATABASE hms_db;
CREATE DATABASE hms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Then run the setup script again
mysql -u hms_user -p hms_db < hms_setup.sql
```

## Security Best Practices

### 1. Change Default Passwords
```sql
-- Change passwords for all default users
UPDATE users SET password = 'new_secure_password' WHERE email = 'owner@stash.com';
UPDATE users SET password = 'new_secure_password' WHERE email = 'admin@stash.com';
-- Repeat for all users
```

### 2. Implement Password Hashing
The current system uses plain text passwords for development. For production:
- Implement bcrypt or similar hashing
- Update the authentication logic
- Hash all existing passwords

### 3. Database User Permissions
```sql
-- For production, consider limiting permissions
REVOKE ALL PRIVILEGES ON hms_db.* FROM 'hms_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON hms_db.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;
```

## Backup and Restore

### Creating a Backup
```bash
# Backup database
mysqldump -u hms_user -p hms_db > hms_backup_$(date +%Y%m%d).sql

# Backup with compression
mysqldump -u hms_user -p hms_db | gzip > hms_backup_$(date +%Y%m%d).sql.gz
```

### Restoring from Backup
```bash
# Restore uncompressed backup
mysql -u hms_user -p hms_db < hms_backup_20231219.sql

# Restore compressed backup
gunzip < hms_backup_20231219.sql.gz | mysql -u hms_user -p hms_db
```

## Next Steps

1. ✅ Run the setup script
2. ✅ Login with default credentials
3. ✅ Change all default passwords
4. ✅ Add real supplier data
5. ✅ Add actual inventory items
6. ✅ Test all user roles
7. ✅ Configure backups
8. ✅ Implement password hashing for production

## Support

For issues or questions:
1. Check the `DATABASE_SETUP.md` file for detailed MariaDB installation
2. Review the `ROLES_AND_ACCESS.md` for role permissions
3. Check the `DEPARTMENT_USERS.md` for department-specific features

---

**System Requirements:**
- MariaDB 10.x or MySQL 5.7+
- Python 3.11+
- PyQt6
- mariadb Python connector

**Recommended:**
- Regular database backups (daily)
- Monitor database size and performance
- Review logs regularly
- Keep software updated
