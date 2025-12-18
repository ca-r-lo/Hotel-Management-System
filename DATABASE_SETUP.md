# Database Setup Guide - Hotel Management System (HMS)

## Prerequisites

Before setting up the database, ensure you have:
- MariaDB or MySQL installed on your system
- Access to create databases and users
- Python virtual environment activated with dependencies installed

## Step 1: Install MariaDB/MySQL

### For macOS:
```bash
# Using Homebrew
brew install mariadb

# Start MariaDB service
brew services start mariadb

# Or MySQL
brew install mysql
brew services start mysql
```

### For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

### For Windows:
- Download and install MariaDB from: https://mariadb.org/download/
- Or MySQL from: https://dev.mysql.com/downloads/installer/

## Step 2: Secure Your Installation (Recommended)

```bash
# For MariaDB
sudo mysql_secure_installation

# For MySQL
sudo mysql_secure_installation
```

Follow the prompts to:
- Set root password
- Remove anonymous users
- Disallow root login remotely
- Remove test database

## Step 3: Create Database and User

### Login to MariaDB/MySQL:
```bash
mysql -u root -p
# Enter your root password when prompted
```

### Create the database:
```sql
-- Create the database
CREATE DATABASE hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated user (recommended for security)
CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'your_secure_password';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON hotel_management.* TO 'hms_user'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

## Step 4: Configure Database Connection

Update the `configs/db_config.json` file with your database credentials:

```json
{
    "host": "localhost",
    "port": 3306,
    "user": "hms_user",
    "password": "your_secure_password",
    "database": "hotel_management",
    "driver": "mariadb"
}
```

**Important:** Keep this file secure and never commit it with real credentials to version control!

## Step 5: Create Database Tables

The application will automatically create tables on first run, but here's the manual SQL if needed:

```sql
-- Use the database
USE hotel_management;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    department VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Items/Inventory table
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE,
    category VARCHAR(100) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    unit_cost DECIMAL(10, 2) DEFAULT 0,
    stock_qty INT DEFAULT 0,
    min_stock INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Suppliers table
CREATE TABLE IF NOT EXISTS suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Purchases table
CREATE TABLE IF NOT EXISTS purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    status VARCHAR(50) DEFAULT 'Pending',
    expected_date DATE,
    received_date DATE,
    created_by VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
);

-- Purchase items table
CREATE TABLE IF NOT EXISTS purchase_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id INT NOT NULL,
    item_id INT,
    item_name VARCHAR(255),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2),
    FOREIGN KEY (purchase_id) REFERENCES purchases(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE SET NULL
);

-- Requests table (for department stock requests)
CREATE TABLE IF NOT EXISTS requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department VARCHAR(50) NOT NULL,
    requested_by VARCHAR(100) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    unit VARCHAR(50),
    reason TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    subject VARCHAR(255),
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Step 6: Insert Sample Users

```sql
-- Insert default admin user
-- Password is 'admin123' (in production, use properly hashed passwords)
INSERT INTO users (email, password, full_name, role, department) VALUES
('admin@stash.com', 'admin123', 'Purchase Admin', 'Purchase Admin', NULL);

-- Insert owner user
INSERT INTO users (email, password, full_name, role, department) VALUES
('owner@stash.com', 'owner123', 'Hotel Owner', 'Owner', NULL);

-- Insert department managers
INSERT INTO users (email, password, full_name, role, department) VALUES
('housekeeping@stash.com', 'pass123', 'Housekeeping Manager', 'Department', 'Housekeeping'),
('kitchen@stash.com', 'pass123', 'Kitchen Manager', 'Department', 'Kitchen'),
('frontdesk@stash.com', 'pass123', 'Front Desk Manager', 'Department', 'Front Desk'),
('maintenance@stash.com', 'pass123', 'Maintenance Manager', 'Department', 'Maintenance');
```

## Step 7: Insert Sample Data (Optional)

### Sample Suppliers:
```sql
INSERT INTO suppliers (name, contact_person, phone, email, address) VALUES
('ABC Supplies Co.', 'John Smith', '555-0101', 'john@abcsupplies.com', '123 Supply Street'),
('XYZ Wholesale', 'Jane Doe', '555-0102', 'jane@xyzwholesale.com', '456 Wholesale Ave'),
('Premium Goods Ltd', 'Bob Johnson', '555-0103', 'bob@premiumgoods.com', '789 Premium Blvd');
```

### Sample Inventory Items:
```sql
INSERT INTO items (name, sku, category, unit, unit_cost, stock_qty, min_stock) VALUES
('Toilet Paper', 'TP001', 'Housekeeping', 'Rolls', 2.50, 500, 100),
('Hand Soap', 'HS001', 'Housekeeping', 'Bottles', 3.75, 200, 50),
('Towels', 'TW001', 'Housekeeping', 'Pieces', 15.00, 150, 30),
('Bed Sheets', 'BS001', 'Housekeeping', 'Sets', 25.00, 100, 20),
('Shampoo', 'SH001', 'Housekeeping', 'Bottles', 4.50, 180, 40),
('Dish Soap', 'DS001', 'Kitchen', 'Bottles', 5.00, 100, 25),
('Paper Plates', 'PP001', 'Kitchen', 'Packs', 8.00, 80, 20),
('Garbage Bags', 'GB001', 'General', 'Rolls', 12.00, 60, 15),
('Cleaning Spray', 'CS001', 'Housekeeping', 'Bottles', 6.50, 90, 25),
('Mops', 'MP001', 'Housekeeping', 'Pieces', 18.00, 30, 10);
```

## Step 8: Verify Installation

### Check database connection:
```bash
# From the HMS directory
cd /Users/louise/Development/HMS
source .venv/bin/activate  # Activate virtual environment
python -c "from models.database import get_conn; conn = get_conn(); print('Connection successful!'); conn.close()"
```

### Check tables:
```sql
USE hotel_management;
SHOW TABLES;
```

Expected output:
```
+----------------------------+
| Tables_in_hotel_management |
+----------------------------+
| items                      |
| messages                   |
| purchase_items             |
| purchases                  |
| requests                   |
| suppliers                  |
| users                      |
+----------------------------+
```

## Step 9: Run the Application

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run the application
python main.py
```

## Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Purchase Admin | admin@stash.com | admin123 |
| Owner | owner@stash.com | owner123 |
| Housekeeping Manager | housekeeping@stash.com | pass123 |
| Kitchen Manager | kitchen@stash.com | pass123 |
| Front Desk Manager | frontdesk@stash.com | pass123 |
| Maintenance Manager | maintenance@stash.com | pass123 |

**⚠️ IMPORTANT: Change these passwords in production!**

## Troubleshooting

### Connection Issues:

**Error: "Access denied for user"**
- Check your username and password in `db_config.json`
- Verify the user has proper privileges

**Error: "Can't connect to MySQL server"**
- Check if MariaDB/MySQL is running: `sudo systemctl status mariadb`
- Verify host and port in `db_config.json`

**Error: "Unknown database"**
- Make sure you created the database: `CREATE DATABASE hotel_management;`

### Permission Issues:

```sql
-- Grant all privileges again
GRANT ALL PRIVILEGES ON hotel_management.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;
```

### Reset Database:

```sql
-- Drop and recreate database (WARNING: This deletes all data!)
DROP DATABASE IF EXISTS hotel_management;
CREATE DATABASE hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Then run all CREATE TABLE statements again
```

## Database Backup

### Backup command:
```bash
mysqldump -u hms_user -p hotel_management > backup_$(date +%Y%m%d).sql
```

### Restore command:
```bash
mysql -u hms_user -p hotel_management < backup_20241219.sql
```

## Security Best Practices

1. **Never commit `db_config.json` with real credentials**
   - Add it to `.gitignore`
   - Use environment variables for production

2. **Use strong passwords** for database users

3. **Implement proper password hashing** (the current system uses plain text - update for production!)

4. **Regular backups** of your database

5. **Restrict database user privileges** to only what's needed

6. **Keep MariaDB/MySQL updated** to the latest stable version

## Next Steps

After setup:
1. Login with admin credentials
2. Add more suppliers via the Purchase page
3. Add inventory items via the Inventory page
4. Test department workflows
5. Explore all features!

---

**Need Help?** Check the application logs or database logs for detailed error messages.
