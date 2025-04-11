-- Create database
CREATE DATABASE IF NOT EXISTS banking_system;
USE banking_system;


-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table with PIN column
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE,
    nominee_name VARCHAR(100),
    nominee_relation VARCHAR(50),
    pin VARCHAR(4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type ENUM('Savings', 'Current', 'Fixed Deposit') NOT NULL,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    opened_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Active', 'Inactive', 'Closed') DEFAULT 'Active',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type ENUM('Deposit', 'Withdrawal', 'Transfer', 'Loan Payment') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    description TEXT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    related_account VARCHAR(20),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

-- Loans table
CREATE TABLE IF NOT EXISTS loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_id INT NOT NULL,
    loan_type ENUM('Home', 'Personal', 'Business', 'Education', 'Car') NOT NULL,
    loan_amount DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    term_months INT NOT NULL,
    monthly_payment DECIMAL(15, 2) NOT NULL,
    remaining_balance DECIMAL(15, 2) NOT NULL,
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status ENUM('Active', 'Paid', 'Defaulted') DEFAULT 'Active',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

-- Cards table
CREATE TABLE IF NOT EXISTS cards (
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_id INT NOT NULL,
    card_type ENUM('Debit', 'Credit', 'Prepaid') NOT NULL,
    card_number VARCHAR(20) NOT NULL UNIQUE,
    expiry_date DATE NOT NULL,
    cvv VARCHAR(5) NOT NULL,
    issued_date DATE NOT NULL,
    status ENUM('Active', 'Blocked', 'Expired') DEFAULT 'Active',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

-- Employees table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(15, 2) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL
);

-- ATM locations table
CREATE TABLE IF NOT EXISTS atm_locations (
    atm_id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

-- Loan schemes table
CREATE TABLE IF NOT EXISTS loan_schemes (
    scheme_id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_name VARCHAR(100) NOT NULL,
    loan_type ENUM('Home', 'Personal', 'Business', 'Education', 'Car') NOT NULL,
    min_amount DECIMAL(15, 2) NOT NULL,
    max_amount DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    min_term_months INT NOT NULL,
    max_term_months INT NOT NULL,
    description TEXT
);

-- Insert sample admin
INSERT INTO admin (username, password, full_name, email) 
VALUES ('admin', 'admin123', 'System Administrator', 'admin@bank.com')
ON DUPLICATE KEY UPDATE username = username;

-- Insert sample customers with PINs
INSERT INTO customers (first_name, last_name, date_of_birth, gender, address, city, state, country, postal_code, phone, email, nominee_name, nominee_relation, pin)
VALUES 
('Rahul', 'Sharma', '1990-05-15', 'Male', '123 MG Road', 'Mumbai', 'Maharashtra', 'India', '400001', '9876543210', 'rahul@example.com', 'Priya Sharma', 'Wife', '1234'),
('Priya', 'Patel', '1985-08-22', 'Female', '456 Linking Road', 'Delhi', 'Delhi', 'India', '110001', '8765432109', 'priya@example.com', 'Rahul Patel', 'Husband', '5678')
ON DUPLICATE KEY UPDATE email = email;

-- Insert sample accounts
INSERT INTO accounts (customer_id, account_type, account_number, balance)
VALUES 
((SELECT customer_id FROM customers WHERE email = 'rahul@example.com'), 'Savings', '100000000001', 50000.00),
((SELECT customer_id FROM customers WHERE email = 'priya@example.com'), 'Current', '100000000002', 100000.00)
ON DUPLICATE KEY UPDATE account_number = account_number;

-- Insert sample transactions
INSERT INTO transactions (account_id, transaction_type, amount, description)
VALUES 
((SELECT account_id FROM accounts WHERE account_number = '100000000001'), 'Deposit', 50000.00, 'Initial deposit'),
((SELECT account_id FROM accounts WHERE account_number = '100000000002'), 'Deposit', 100000.00, 'Initial deposit')
ON DUPLICATE KEY UPDATE transaction_id = transaction_id;

-- Insert sample loan schemes
INSERT INTO loan_schemes (scheme_name, loan_type, min_amount, max_amount, interest_rate, min_term_months, max_term_months, description)
VALUES 
('Home Loan Basic', 'Home', 500000, 5000000, 8.5, 60, 240, 'Basic home loan scheme for residential properties'),
('Personal Loan Standard', 'Personal', 10000, 500000, 12.0, 12, 60, 'Standard personal loan for various needs'),
('Business Startup', 'Business', 100000, 2000000, 10.5, 24, 120, 'Loan scheme for new business ventures'),
('Education Loan', 'Education', 50000, 1000000, 9.0, 12, 84, 'Loan for higher education expenses'),
('Car Loan Premium', 'Car', 200000, 2000000, 8.0, 12, 84, 'Loan for purchasing new vehicles')
ON DUPLICATE KEY UPDATE scheme_id = scheme_id;
-- Insert sample ATM locations (Kolkata, India)
INSERT INTO atm_locations (location_name, address, city, state, country, postal_code, latitude, longitude)
VALUES 
('Park Street ATM', '12 Park Street', 'Kolkata', 'West Bengal', 'India', '700016', 22.552221, 88.352777),
('Salt Lake Sector V ATM', 'DLF Building, Salt Lake Sector V', 'Kolkata', 'West Bengal', 'India', '700091', 22.581828, 88.437189),
('Howrah Station ATM', 'Howrah Railway Station Complex', 'Howrah', 'West Bengal', 'India', '711101', 22.585000, 88.342000),
('South City Mall ATM', '375 Prince Anwar Shah Road', 'Kolkata', 'West Bengal', 'India', '700068', 22.501669, 88.361924),
('Esplanade Metro ATM', 'Near Metro Gate No. 3, Esplanade', 'Kolkata', 'West Bengal', 'India', '700069', 22.564518, 88.352826)

ON DUPLICATE KEY UPDATE atm_id = atm_id;
