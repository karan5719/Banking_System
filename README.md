# Banking Management System

A comprehensive banking management system with admin and customer interfaces built with Python (Tkinter) and MySQL.

## Features

- **Admin Dashboard**:
  - Customer account management
  - Loan calculator and schemes
  - ATM location management
  - Employee management
  - Report generation

- **Customer Dashboard**:
  - Account management (deposit/withdraw/transfer)
  - Transaction history
  - Loan information
  - Card management
  - E-passbook download

## Technologies Used

- Python (Tkinter for GUI)
- MySQL (Database)
- FPDF (For PDF report generation)

## Installation

1. Clone the repository:
   bash
   git clone https://github.com/your-username/banking-management-system.git
   

2. Set up MySQL database:
   bash
   mysql -u root -p < database/banking_system.sql
   

3. Install dependencies:
   bash
   pip install -r requirements.txt
   

4. Run the application:
   bash
   python src/banking_app.py
   

## Configuration

Edit the database connection details in `banking_app.py`:
python
self.connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",  # Change this
    database="banking_system"
)
