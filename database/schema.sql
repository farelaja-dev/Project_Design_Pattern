-- ============================================
-- DATABASE SCHEMA untuk Restaurant Management System
-- ============================================

-- Drop tables if exists
DROP TABLE IF EXISTS order_reports CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS menu_items CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- Table: customers
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    is_member BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: menu_items
CREATE TABLE menu_items (
    item_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE SET NULL,
    item_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(20) NOT NULL, -- food, beverage, package
    base_price DECIMAL(10,2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE SET NULL,
    table_number INTEGER NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, cooking, served, paid, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: order_items (detail items dalam order)
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES menu_items(item_id),
    quantity INTEGER NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: order_reports
CREATE TABLE order_reports (
    report_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    report_type VARCHAR(20) NOT NULL, -- pdf, excel, json
    report_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_menu_items_type ON menu_items(item_type);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- Insert sample customers
INSERT INTO customers (name, phone, email, is_member) VALUES 
    ('Budi Santoso', '081234567890', 'budi@example.com', TRUE),
    ('Siti Nurhaliza', '081234567891', 'siti@example.com', TRUE),
    ('Ahmad Rizki', '081234567892', 'ahmad@example.com', FALSE),
    ('Dewi Lestari', '081234567893', 'dewi@example.com', FALSE);

-- Insert sample menu items - MAKANAN
INSERT INTO menu_items (customer_id, item_name, item_type, base_price, description) VALUES 
    (1, 'Nasi Goreng Spesial', 'food', 25000, 'Nasi goreng dengan ayam, telur, dan sayuran'),
    (1, 'Mie Goreng Seafood', 'food', 30000, 'Mie goreng dengan udang, cumi, dan sayuran'),
    (1, 'Ayam Geprek Sambal Matah', 'food', 28000, 'Ayam goreng geprek dengan sambal matah pedas'),
    (1, 'Sate Ayam (10 tusuk)', 'food', 35000, 'Sate ayam bakar dengan bumbu kacang'),
    (2, 'Pizza Margherita', 'food', 55000, 'Pizza dengan keju mozzarella dan basil'),
    (2, 'Burger Beef Cheese', 'food', 40000, 'Burger daging sapi dengan keju cheddar');

-- Insert sample menu items - MINUMAN
INSERT INTO menu_items (customer_id, item_name, item_type, base_price, description) VALUES 
    (1, 'Es Teh Manis', 'beverage', 5000, 'Teh manis dingin segar'),
    (1, 'Es Jeruk', 'beverage', 8000, 'Jus jeruk segar dengan es'),
    (2, 'Cappuccino', 'beverage', 18000, 'Kopi cappuccino hangat'),
    (2, 'Thai Tea', 'beverage', 15000, 'Thai tea manis dengan susu'),
    (2, 'Jus Alpukat', 'beverage', 15000, 'Jus alpukat segar dengan cokelat'),
    (1, 'Air Mineral', 'beverage', 3000, 'Air mineral kemasan');

-- Insert sample menu items - PAKET
INSERT INTO menu_items (customer_id, item_name, item_type, base_price, description) VALUES 
    (1, 'Paket Hemat A', 'package', 35000, 'Nasi Goreng + Es Teh + Kerupuk'),
    (1, 'Paket Hemat B', 'package', 45000, 'Ayam Geprek + Nasi + Es Jeruk'),
    (2, 'Paket Romantic', 'package', 120000, 'Pizza Margherita + 2 Cappuccino + Dessert'),
    (2, 'Paket Family', 'package', 150000, '2 Nasi Goreng + 2 Mie Goreng + 4 Minuman');

-- Insert sample orders
INSERT INTO orders (customer_id, table_number, total_price, status) VALUES 
    (1, 5, 63000, 'served'),
    (2, 3, 120000, 'cooking'),
    (3, 7, 45000, 'pending'),
    (4, 2, 85000, 'paid');

-- Insert sample order items
INSERT INTO order_items (order_id, item_id, quantity, price, notes) VALUES 
    (1, 1, 2, 25000, 'Pedas sedang'),
    (1, 9, 2, 18000, 'Tanpa gula'),
    (2, 11, 1, 120000, 'Untuk anniversary'),
    (3, 8, 1, 45000, NULL),
    (4, 3, 2, 28000, 'Extra pedas'),
    (4, 10, 1, 15000, 'Less ice'),
    (4, 12, 1, 3000, NULL);

COMMENT ON TABLE customers IS 'Stores customer information';
COMMENT ON TABLE menu_items IS 'Stores menu items (food, beverage, packages)';
COMMENT ON TABLE orders IS 'Stores order headers';
COMMENT ON TABLE order_items IS 'Stores order line items';
COMMENT ON TABLE order_reports IS 'Tracks generated reports history';
