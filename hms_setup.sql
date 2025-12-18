-- =====================================================
-- HMS (Hotel Management System) Database Setup Script
-- =====================================================
-- This script creates all necessary tables and inserts default users
-- Run this after creating the database and user

-- =====================================================
-- 1. USERS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    department VARCHAR(100) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 2. SUPPLIERS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(64),
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 3. ITEMS TABLE (Inventory)
-- =====================================================
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) DEFAULT NULL,
    unit VARCHAR(50) NOT NULL,
    unit_cost DECIMAL(12,2) DEFAULT 0.00,
    stock_qty INT DEFAULT 0,
    min_stock INT DEFAULT 10,
    category VARCHAR(100) DEFAULT 'General',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_stock (stock_qty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 4. PURCHASES TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    expected_date DATE,
    total_amount DECIMAL(12,2) DEFAULT 0.00,
    status VARCHAR(32) DEFAULT 'pending',
    created_by VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL,
    INDEX idx_supplier (supplier_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 5. PURCHASE_ITEMS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS purchase_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id INT NOT NULL,
    item_name VARCHAR(255),
    item_id INT,
    qty INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (purchase_id) REFERENCES purchases(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE SET NULL,
    INDEX idx_purchase (purchase_id),
    INDEX idx_item (item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 6. DAMAGES TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS damages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    quantity INT NOT NULL,
    reason TEXT,
    created_by VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE SET NULL,
    INDEX idx_item (item_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 7. MESSAGES TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    category VARCHAR(64) DEFAULT 'General',
    title VARCHAR(255),
    body TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sender (sender_id),
    INDEX idx_recipient (recipient_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 8. REQUESTS TABLE (Stock Requests)
-- =====================================================
CREATE TABLE IF NOT EXISTS requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department VARCHAR(50) NOT NULL,
    requested_by VARCHAR(100) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    unit VARCHAR(50),
    reason TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    notes TEXT,
    INDEX idx_department (department),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- INSERT DEFAULT USERS
-- =====================================================

-- Note: In production, passwords should be hashed!
-- These are plain text passwords for demonstration only.

-- Owner Account
INSERT INTO users (email, password, full_name, role, department) VALUES 
('owner@stash.com', 'owner123', 'Hotel Owner', 'Owner', NULL);

-- Purchase Admin Account
INSERT INTO users (email, password, full_name, role, department) VALUES 
('admin@stash.com', 'admin123', 'Purchase Admin', 'Purchase Admin', NULL);

-- Department Users
INSERT INTO users (email, password, full_name, role, department) VALUES 
('housekeeping@stash.com', 'housekeeping123', 'Housekeeping Manager', 'Department', 'Housekeeping');

INSERT INTO users (email, password, full_name, role, department) VALUES 
('kitchen@stash.com', 'kitchen123', 'Kitchen Manager', 'Department', 'Kitchen');

INSERT INTO users (email, password, full_name, role, department) VALUES 
('frontdesk@stash.com', 'frontdesk123', 'Front Desk Manager', 'Department', 'Front Desk');

INSERT INTO users (email, password, full_name, role, department) VALUES 
('maintenance@stash.com', 'maintenance123', 'Maintenance Manager', 'Department', 'Maintenance');

-- =====================================================
-- INSERT SAMPLE SUPPLIERS (Optional)
-- =====================================================

INSERT INTO suppliers (name, contact_name, email, phone, address) VALUES 
('ABC Supplies Inc.', 'John Smith', 'john@abcsupplies.com', '+1-555-0101', '123 Supply Street, City, State 12345');

INSERT INTO suppliers (name, contact_name, email, phone, address) VALUES 
('Hotel Essentials Co.', 'Jane Doe', 'jane@hotelessen.com', '+1-555-0102', '456 Commerce Ave, City, State 12345');

INSERT INTO suppliers (name, contact_name, email, phone, address) VALUES 
('Kitchen Wholesale', 'Bob Johnson', 'bob@kitchenwhole.com', '+1-555-0103', '789 Market Road, City, State 12345');

-- =====================================================
-- INSERT SAMPLE INVENTORY ITEMS (Optional)
-- =====================================================

-- Housekeeping Items
INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Bath Towels', 'HK-001', 'pcs', 15.00, 100, 50, 'Housekeeping');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Hand Soap', 'HK-002', 'bottles', 5.00, 200, 100, 'Housekeeping');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Bed Sheets', 'HK-003', 'sets', 25.00, 150, 75, 'Housekeeping');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Toilet Paper', 'HK-004', 'rolls', 2.00, 500, 200, 'Housekeeping');

-- Kitchen Items
INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Cooking Oil', 'KT-001', 'liters', 8.00, 50, 20, 'Kitchen');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Rice', 'KT-002', 'kg', 3.00, 200, 100, 'Kitchen');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Dish Soap', 'KT-003', 'bottles', 4.00, 30, 15, 'Kitchen');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Paper Plates', 'KT-004', 'packs', 6.00, 40, 20, 'Kitchen');

-- Front Desk Items
INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Key Cards', 'FD-001', 'pcs', 1.00, 500, 200, 'Front Desk');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Pens', 'FD-002', 'boxes', 10.00, 50, 25, 'Front Desk');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Receipt Paper', 'FD-003', 'rolls', 5.00, 100, 50, 'Front Desk');

-- Maintenance Items
INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Light Bulbs', 'MT-001', 'pcs', 3.00, 200, 100, 'Maintenance');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Paint', 'MT-002', 'gallons', 25.00, 20, 10, 'Maintenance');

INSERT INTO items (name, sku, unit, unit_cost, stock_qty, min_stock, category) VALUES 
('Cleaning Supplies', 'MT-003', 'sets', 15.00, 30, 15, 'Maintenance');

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Verify users were created
-- SELECT * FROM users;

-- Verify suppliers were created
-- SELECT * FROM suppliers;

-- Verify items were created
-- SELECT * FROM items;

-- Check database structure
-- SHOW TABLES;

-- =====================================================
-- NOTES
-- =====================================================
-- 
-- Default User Credentials:
-- -------------------------
-- Owner:          owner@stash.com / owner123
-- Purchase Admin: admin@stash.com / admin123
-- Housekeeping:   housekeeping@stash.com / housekeeping123
-- Kitchen:        kitchen@stash.com / kitchen123
-- Front Desk:     frontdesk@stash.com / frontdesk123
-- Maintenance:    maintenance@stash.com / maintenance123
--
-- Role Permissions:
-- -----------------
-- Owner:          Dashboard, Trans History, Dept Overview, Reports, Messages
-- Purchase Admin: Dashboard, Purchase, Inventory, Reports, Messages
-- Department:     Dashboard, Inventory, Requests, Reports, Messages
--
-- Important Security Notes:
-- -------------------------
-- 1. Change all default passwords before production use
-- 2. Implement password hashing (bcrypt recommended)
-- 3. Use SSL/TLS for database connections
-- 4. Implement proper session management
-- 5. Add input validation and sanitization
-- 6. Enable database audit logging
-- 7. Set up regular backups
--
-- =====================================================
