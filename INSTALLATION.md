# HMS Installation Guide

## System Requirements

### Python
- **Version**: Python 3.11 or higher
- **Download**: https://www.python.org/downloads/

### Database
- **MariaDB** 10.x or **MySQL** 5.7+
- MariaDB is recommended

### Operating System
- macOS 10.15+
- Ubuntu 20.04+ / Debian 10+
- Windows 10/11

## Quick Installation

### 1. Clone/Download the Project

```bash
cd /path/to/your/projects
# If using git:
git clone <repository-url> HMS
cd HMS
```

### 2. Install System Dependencies

#### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install MariaDB
brew install mariadb

# Install MariaDB Connector/C
brew install mariadb-connector-c

# Start MariaDB service
brew services start mariadb
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt-get update

# Install MariaDB
sudo apt-get install mariadb-server mariadb-client

# Install development libraries
sudo apt-get install libmariadb-dev python3-dev build-essential

# Start MariaDB service
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Secure installation (recommended)
sudo mysql_secure_installation
```

#### Windows
1. Download MariaDB from: https://mariadb.org/download/
2. Run the installer and follow the setup wizard
3. Download MariaDB Connector/C from: https://mariadb.com/downloads/connectors/connectors-data-access/c-connector/
4. Add MariaDB bin directory to PATH

### 3. Create Python Virtual Environment

```bash
# Navigate to project directory
cd /path/to/HMS

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Verify activation (should show .venv in prompt)
which python  # macOS/Linux
where python  # Windows
```

### 4. Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# If mariadb installation fails on macOS:
pip install --no-binary :all: mariadb
```

### 5. Setup Database

```bash
# Login to MariaDB
mysql -u root -p
# or
mariadb -u root -p
```

```sql
-- Create database
CREATE DATABASE hms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit
EXIT;
```

```bash
# Run setup script to create tables and insert default data
mysql -u hms_user -p hms_db < hms_setup.sql
```

### 6. Configure Application

Edit `configs/db_config.json`:

```json
{
    "host": "localhost",
    "port": 3306,
    "user": "hms_user",
    "password": "your_secure_password",
    "database": "hms_db"
}
```

### 7. Run the Application

```bash
# Make sure virtual environment is activated
python main.py
```

## Verification

### Check Python Version
```bash
python --version
# Should show: Python 3.11.x or higher
```

### Check Installed Packages
```bash
pip list
# Should show all packages from requirements.txt
```

### Test Database Connection
```bash
mysql -u hms_user -p hms_db -e "SHOW TABLES;"
# Should list all HMS tables
```

## Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Owner | owner@stash.com | owner123 |
| Purchase Admin | admin@stash.com | admin123 |
| Housekeeping | housekeeping@stash.com | housekeeping123 |
| Kitchen | kitchen@stash.com | kitchen123 |
| Front Desk | frontdesk@stash.com | frontdesk123 |
| Maintenance | maintenance@stash.com | maintenance123 |

## Troubleshooting

### MariaDB Connection Issues

**Error: "Can't connect to local MySQL server"**
```bash
# Check if MariaDB is running
# macOS:
brew services list

# Linux:
sudo systemctl status mariadb

# Windows:
services.msc  # Look for MariaDB service
```

**Error: "Access denied for user"**
```bash
# Reset user permissions
mysql -u root -p
GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;
```

### Python Package Installation Issues

**Error: "mariadb-connector-c not found"**

macOS:
```bash
# Install connector
brew install mariadb-connector-c

# Set environment variables
export MARIADB_CONFIG=/usr/local/bin/mariadb_config
pip install mariadb
```

Linux:
```bash
sudo apt-get install libmariadb-dev
pip install mariadb
```

Windows:
- Download and install MariaDB Connector/C
- Add to system PATH

**Error: "No module named PyQt6"**
```bash
pip install PyQt6==6.6.1
```

### Application Runtime Errors

**Error: "Database connection failed"**
1. Check `configs/db_config.json` credentials
2. Verify database exists: `mysql -u hms_user -p -e "SHOW DATABASES;"`
3. Check MariaDB is running

**Error: "Table doesn't exist"**
```bash
# Run setup script again
mysql -u hms_user -p hms_db < hms_setup.sql
```

**Error: "QApplication: no such file or directory"**
```bash
# Reinstall PyQt6
pip uninstall PyQt6
pip install PyQt6==6.6.1
```

## Development Setup

### Installing Optional Packages

Uncomment desired packages in `requirements.txt`, then:

```bash
pip install -r requirements.txt
```

### Recommended Optional Packages

**PDF Export:**
```bash
pip install reportlab
```

**Excel Export:**
```bash
pip install openpyxl xlsxwriter
```

**Password Hashing (IMPORTANT for production):**
```bash
pip install bcrypt
```

**Barcode/QR Generation:**
```bash
pip install python-barcode qrcode Pillow
```

### Development Tools

```bash
# Code formatting
pip install black

# Linting
pip install pylint flake8

# Testing
pip install pytest pytest-qt
```

## Updating Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade PyQt6

# Check outdated packages
pip list --outdated
```

## Creating a Standalone Executable

### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --name="HMS" --windowed --icon=assets/logo_taskbar.png main.py

# Output will be in dist/HMS/
```

## Backup and Maintenance

### Backup Database
```bash
mysqldump -u hms_user -p hms_db > backup_$(date +%Y%m%d).sql
```

### Backup Configuration
```bash
cp configs/db_config.json configs/db_config.json.backup
```

### Update System
```bash
# Pull latest code (if using git)
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run database migrations if any
mysql -u hms_user -p hms_db < migrations/update_YYYYMMDD.sql
```

## Production Deployment Checklist

- [ ] Change all default passwords
- [ ] Implement password hashing (bcrypt)
- [ ] Configure SSL/TLS for database connections
- [ ] Set up regular database backups
- [ ] Enable database audit logging
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Review and harden security settings
- [ ] Test disaster recovery procedures
- [ ] Document system architecture
- [ ] Create user training materials

## Getting Help

### Documentation Files
- `README.md` - Project overview
- `SETUP_GUIDE.md` - Database setup guide
- `ROLES_AND_ACCESS.md` - User roles and permissions
- `DEPARTMENT_USERS.md` - Department-specific features
- `DATABASE_SETUP.md` - Detailed database setup

### Common Commands Reference

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Run application
python main.py

# Check logs
tail -f logs/hms.log  # If logging is enabled

# Database backup
mysqldump -u hms_user -p hms_db > backup.sql

# Database restore
mysql -u hms_user -p hms_db < backup.sql

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Deactivate virtual environment
deactivate
```

## Performance Optimization

### Database
- Enable query caching in MariaDB
- Add indexes for frequently queried columns
- Optimize table structures
- Regular ANALYZE and OPTIMIZE TABLE commands

### Application
- Use connection pooling
- Implement caching for frequently accessed data
- Optimize image loading
- Profile and optimize slow queries

## Security Best Practices

1. **Never commit `db_config.json` to version control**
   ```bash
   # Add to .gitignore
   echo "configs/db_config.json" >> .gitignore
   ```

2. **Use environment variables for sensitive data**
   ```bash
   pip install python-dotenv
   ```

3. **Implement password hashing**
   ```python
   import bcrypt
   hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
   ```

4. **Regular security updates**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## System Architecture

```
HMS/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── hms_setup.sql          # Database setup script
├── configs/
│   ├── config.py          # Application configuration
│   └── db_config.json     # Database credentials
├── models/
│   ├── database.py        # Database connection
│   ├── user.py           # User model
│   ├── purchase.py       # Purchase/Item models
│   └── request.py        # Request model
├── views/
│   ├── dashboard.py      # Main dashboard
│   ├── login.py          # Login screen
│   ├── inventory.py      # Inventory management
│   ├── purchase_view.py  # Purchase orders
│   ├── reports.py        # Reports and analytics
│   └── messages.py       # Messaging system
├── controllers/
│   ├── login.py          # Login logic
│   ├── inventory_controller.py
│   ├── purchase_controller.py
│   └── ...
└── assets/
    └── logo_taskbar.png   # Application icon
```

---

**Version**: 1.0.0  
**Last Updated**: December 19, 2025  
**Python**: 3.11+  
**Database**: MariaDB 10.x / MySQL 5.7+
