-- Create inventory_history table to track all inventory movements
CREATE TABLE IF NOT EXISTS inventory_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    movement_type VARCHAR(50) NOT NULL COMMENT 'stock_in, stock_out, distributed, adjustment, damage',
    quantity INT NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    notes TEXT,
    department VARCHAR(100),
    created_at DATETIME NOT NULL,
    INDEX idx_created_at (created_at),
    INDEX idx_item_name (item_name),
    INDEX idx_movement_type (movement_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
