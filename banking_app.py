import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import random
import os
from fpdf import FPDF
import webbrowser

class BankingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Database connection
        self.connection = None
        self.connect_to_database()
        
        # Current user info
        self.current_user = None
        self.user_type = None
        
        # Fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.button_font = Font(family="Helvetica", size=12)
        self.label_font = Font(family="Helvetica", size=12)
        
        # Colors
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"
        self.light_color = "#ecf0f1"
        self.dark_color = "#2c3e50"
        
        # Show login screen
        self.show_login_screen()
    
    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Replace with your MySQL password
                database="", # Replace wuth your MYSQL DATABASE
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            self.root.destroy()
    
    def show_login_screen(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container frame
        container = tk.Frame(self.root, bg=self.light_color)
        container.pack(fill="both", expand=True)
        
        # Create a canvas and scrollbar
        canvas = tk.Canvas(container, bg=self.light_color)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.light_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Login frame
        login_frame = tk.Frame(scrollable_frame, bg=self.light_color, padx=20, pady=20)
        login_frame.pack(pady=20)
        
        # Title
        tk.Label(login_frame, text="BANK OF IIITK LOGIN", font=self.title_font, bg=self.light_color).grid(row=0, column=0, columnspan=2, pady=20)
        
        # User type selection
        self.user_type_var = tk.StringVar(value="Customer")
        tk.Label(login_frame, text="Login As:", font=self.label_font, bg=self.light_color).grid(row=1, column=0, sticky="w", pady=5)
        tk.Radiobutton(login_frame, text="Customer", variable=self.user_type_var, value="Customer", bg=self.light_color, 
                      command=self.toggle_login_fields).grid(row=1, column=1, sticky="w")
        tk.Radiobutton(login_frame, text="Admin", variable=self.user_type_var, value="Admin", bg=self.light_color,
                      command=self.toggle_login_fields).grid(row=2, column=1, sticky="w")
        
        # Login fields frame
        self.login_fields_frame = tk.Frame(login_frame, bg=self.light_color)
        self.login_fields_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Customer PIN creation frame (initially hidden)
        self.pin_creation_frame = tk.Frame(login_frame, bg=self.light_color)
        
        # Toggle between login and PIN creation
        self.toggle_login_button = tk.Button(login_frame, text="Create/Reset PIN", font=self.button_font,
                                           command=self.toggle_pin_creation, bg=self.secondary_color, fg="white", width=15)
        self.toggle_login_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Initialize fields
        self.toggle_login_fields()
        
        # Login button
        login_button = tk.Button(login_frame, text="Login", font=self.button_font, bg=self.secondary_color, fg="white", 
                               command=self.authenticate_user, width=15)
        login_button.grid(row=5, column=0, columnspan=2, pady=20, ipady=5)
        
        # Focus on username field
        if hasattr(self, 'username_entry'):
            self.username_entry.focus_set()

    def toggle_login_fields(self):
        # Clear existing fields
        for widget in self.login_fields_frame.winfo_children():
            widget.destroy()
        
        for widget in self.pin_creation_frame.winfo_children():
            widget.destroy()
        
        self.pin_creation_frame.grid_forget()
        self.toggle_login_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        if self.user_type_var.get() == "Admin":
            # Admin login fields
            tk.Label(self.login_fields_frame, text="Username:", font=self.label_font, bg=self.light_color).grid(row=0, column=0, sticky="w", pady=5)
            self.username_entry = tk.Entry(self.login_fields_frame, font=self.label_font)
            self.username_entry.grid(row=0, column=1, pady=5, ipadx=50, ipady=5)
            
            tk.Label(self.login_fields_frame, text="Password:", font=self.label_font, bg=self.light_color).grid(row=1, column=0, sticky="w", pady=5)
            self.password_entry = tk.Entry(self.login_fields_frame, font=self.label_font, show="*")
            self.password_entry.grid(row=1, column=1, pady=5, ipadx=50, ipady=5)
        else:
            # Customer login fields
            tk.Label(self.login_fields_frame, text="Email:", font=self.label_font, bg=self.light_color).grid(row=0, column=0, sticky="w", pady=5)
            self.username_entry = tk.Entry(self.login_fields_frame, font=self.label_font)
            self.username_entry.grid(row=0, column=1, pady=5, ipadx=50, ipady=5)
            
            tk.Label(self.login_fields_frame, text="PIN:", font=self.label_font, bg=self.light_color).grid(row=1, column=0, sticky="w", pady=5)
            self.password_entry = tk.Entry(self.login_fields_frame, font=self.label_font, show="*")
            self.password_entry.grid(row=1, column=1, pady=5, ipadx=50, ipady=5)

    def toggle_pin_creation(self):
        if self.user_type_var.get() != "Customer":
            messagebox.showinfo("Info", "PIN creation is only available for customers")
            return
        
        # Clear existing fields
        for widget in self.login_fields_frame.winfo_children():
            widget.destroy()
        
        for widget in self.pin_creation_frame.winfo_children():
            widget.destroy()
        
        self.login_fields_frame.grid_forget()
        self.toggle_login_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # PIN creation fields
        self.pin_creation_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Label(self.pin_creation_frame, text="Account ID:", font=self.label_font, bg=self.light_color).grid(row=0, column=0, sticky="w", pady=5)
        self.account_id_entry = tk.Entry(self.pin_creation_frame, font=self.label_font)
        self.account_id_entry.grid(row=0, column=1, pady=5, ipadx=50, ipady=5)
        
        tk.Label(self.pin_creation_frame, text="Date of Birth (YYYY-MM-DD):", font=self.label_font, bg=self.light_color).grid(row=1, column=0, sticky="w", pady=5)
        self.dob_entry = tk.Entry(self.pin_creation_frame, font=self.label_font)
        self.dob_entry.grid(row=1, column=1, pady=5, ipadx=50, ipady=5)
        
        tk.Label(self.pin_creation_frame, text="New PIN (4 digits):", font=self.label_font, bg=self.light_color).grid(row=2, column=0, sticky="w", pady=5)
        self.new_pin_entry = tk.Entry(self.pin_creation_frame, font=self.label_font, show="*")
        self.new_pin_entry.grid(row=2, column=1, pady=5, ipadx=50, ipady=5)
        
        tk.Label(self.pin_creation_frame, text="Confirm PIN:", font=self.label_font, bg=self.light_color).grid(row=3, column=0, sticky="w", pady=5)
        self.confirm_pin_entry = tk.Entry(self.pin_creation_frame, font=self.label_font, show="*")
        self.confirm_pin_entry.grid(row=3, column=1, pady=5, ipadx=50, ipady=5)
        
        # Create PIN button
        create_pin_button = tk.Button(self.pin_creation_frame, text="Create PIN", font=self.button_font, 
                                    bg=self.secondary_color, fg="white", command=self.create_pin, width=15)
        create_pin_button.grid(row=4, column=0, columnspan=2, pady=20, ipady=5)
        
        # Back to login button
        back_button = tk.Button(self.pin_creation_frame, text="Back to Login", font=self.button_font,
                              bg=self.accent_color, fg="white", command=self.toggle_login_fields, width=15)
        back_button.grid(row=5, column=0, columnspan=2, pady=10, ipady=5)

    def create_pin(self):
        account_id = self.account_id_entry.get()
        dob = self.dob_entry.get()
        new_pin = self.new_pin_entry.get()
        confirm_pin = self.confirm_pin_entry.get()
        
        if not account_id or not dob or not new_pin or not confirm_pin:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if new_pin != confirm_pin:
            messagebox.showerror("Error", "PINs do not match")
            return
        
        if not new_pin.isdigit() or len(new_pin) != 4:
            messagebox.showerror("Error", "PIN must be 4 digits")
            return
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Verify account and DOB
            cursor.execute("""
                SELECT c.customer_id 
                FROM customers c
                JOIN accounts a ON c.customer_id = a.customer_id
                WHERE a.account_id = %s AND c.date_of_birth = %s
            """, (account_id, dob))
            
            customer = cursor.fetchone()
            
            if not customer:
                messagebox.showerror("Error", "Account not found or date of birth doesn't match")
                return
            
            # In a real system, you would hash the PIN before storing
            # For this demo, we'll store it directly (not secure for production)
            cursor.execute("""
                UPDATE customers 
                SET pin = %s 
                WHERE customer_id = %s
            """, (new_pin, customer['customer_id']))
            
            self.connection.commit()
            
            messagebox.showinfo("Success", "PIN created successfully")
            self.toggle_login_fields()
            
        except Error as e:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to create PIN: {e}")

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get() if hasattr(self, 'password_entry') else ""
        user_type = self.user_type_var.get()
        
        if user_type == "Customer" and self.pin_creation_frame.winfo_ismapped():
            messagebox.showinfo("Info", "Please complete PIN creation or go back to login")
            return
        
        if not username or (user_type == "Admin" and not password):
            messagebox.showerror("Error", "Please enter all required fields")
            return
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if user_type == "Admin":
                query = "SELECT * FROM admin WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
            else:  # Customer
                query = "SELECT * FROM customers WHERE email = %s AND pin = %s"
                cursor.execute(query, (username, password))
            
            user = cursor.fetchone()
            
            if user:
                self.current_user = user
                self.user_type = user_type
                
                if user_type == "Admin":
                    self.show_admin_dashboard()
                else:
                    self.show_customer_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error during authentication: {e}")
    
    def show_admin_dashboard(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.primary_color, padx=20, pady=10)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="Admin Dashboard", font=self.title_font, bg=self.primary_color, fg="white").pack(side="left")
        
        # User info and logout
        user_frame = tk.Frame(header_frame, bg=self.primary_color)
        user_frame.pack(side="right")
        
        tk.Label(user_frame, text=f"Welcome, {self.current_user['full_name']}", font=self.label_font, 
                bg=self.primary_color, fg="white").grid(row=0, column=0, padx=10)
        
        logout_button = tk.Button(user_frame, text="Logout", font=self.button_font, bg=self.accent_color, fg="white",
                                command=self.show_login_screen)
        logout_button.grid(row=0, column=1)
        
        # Dashboard buttons
        buttons_frame = tk.Frame(main_frame, bg=self.light_color, padx=20, pady=20)
        buttons_frame.pack(fill="both", expand=True)
        
        # Button configuration
        buttons = [
            ("Create Customer Account", self.show_create_customer),
            ("Loan Calculator", self.show_loan_calculator),
            ("ATM Locator", self.show_atm_locator),
            ("Loan Schemes", self.show_loan_schemes),
            ("Employee Management", self.show_employee_management),
            ("View Customers", self.show_customers_list),
            ("Generate Reports", self.generate_reports)
        ]
        
        # Create buttons in a grid
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            button = tk.Button(buttons_frame, text=text, font=self.button_font, bg=self.secondary_color, fg="white",
                             command=command, height=3, width=20)
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            buttons_frame.grid_columnconfigure(col, weight=1)
        
        buttons_frame.grid_rowconfigure(len(buttons) // 3 + 1, weight=1)
    
    def show_customer_dashboard(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.primary_color, padx=20, pady=10)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="Customer Dashboard", font=self.title_font, bg=self.primary_color, fg="white").pack(side="left")
        
        # User info and logout
        user_frame = tk.Frame(header_frame, bg=self.primary_color)
        user_frame.pack(side="right")
        
        tk.Label(user_frame, text=f"Welcome, {self.current_user['first_name']} {self.current_user['last_name']}", 
                font=self.label_font, bg=self.primary_color, fg="white").grid(row=0, column=0, padx=10)
        
        logout_button = tk.Button(user_frame, text="Logout", font=self.button_font, bg=self.accent_color, fg="white",
                                command=self.show_login_screen)
        logout_button.grid(row=0, column=1)
        
        # Dashboard buttons
        buttons_frame = tk.Frame(main_frame, bg=self.light_color, padx=20, pady=20)
        buttons_frame.pack(fill="both", expand=True)
        
        # Button configuration
        buttons = [
            ("Customer Details", self.show_customer_details),
            ("Account Details", self.show_account_details),
            ("Transaction History", self.show_transaction_history),
            ("Loan Information", self.show_loan_information),
            ("Card Information", self.show_card_information),
            ("Download E-Passbook", self.download_passbook)
        ]
        
        # Create buttons in a grid
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            button = tk.Button(buttons_frame, text=text, font=self.button_font, bg=self.secondary_color, fg="white",
                             command=command, height=3, width=20)
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            buttons_frame.grid_columnconfigure(col, weight=1)
        
        buttons_frame.grid_rowconfigure(len(buttons) // 3 + 1, weight=1)
    
    # Admin Functions
    def show_create_customer(self):
        # Create a new window
        create_window = tk.Toplevel(self.root)
        create_window.title("Create Customer Account")
        create_window.geometry("800x600")
        create_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(create_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Create New Customer Account", font=self.title_font).pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Personal Information
        personal_frame = tk.LabelFrame(form_frame, text="Personal Information", padx=10, pady=10)
        personal_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        tk.Label(personal_frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=5)
        first_name_entry = tk.Entry(personal_frame)
        first_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(personal_frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=5)
        last_name_entry = tk.Entry(personal_frame)
        last_name_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(personal_frame, text="Date of Birth:").grid(row=2, column=0, sticky="w", pady=5)
        dob_entry = tk.Entry(personal_frame)
        dob_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        dob_entry.insert(0, "YYYY-MM-DD")
        
        tk.Label(personal_frame, text="Gender:").grid(row=3, column=0, sticky="w", pady=5)
        gender_var = tk.StringVar(value="Male")
        tk.Radiobutton(personal_frame, text="Male", variable=gender_var, value="Male").grid(row=3, column=1, sticky="w")
        tk.Radiobutton(personal_frame, text="Female", variable=gender_var, value="Female").grid(row=4, column=1, sticky="w")
        tk.Radiobutton(personal_frame, text="Other", variable=gender_var, value="Other").grid(row=5, column=1, sticky="w")
        
        # Contact Information
        contact_frame = tk.LabelFrame(form_frame, text="Contact Information", padx=10, pady=10)
        contact_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        tk.Label(contact_frame, text="Email:").grid(row=0, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(contact_frame)
        email_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(contact_frame, text="Phone:").grid(row=1, column=0, sticky="w", pady=5)
        phone_entry = tk.Entry(contact_frame)
        phone_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Address Information
        address_frame = tk.LabelFrame(form_frame, text="Address Information", padx=10, pady=10)
        address_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        tk.Label(address_frame, text="Address:").grid(row=0, column=0, sticky="w", pady=5)
        address_entry = tk.Entry(address_frame)
        address_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(address_frame, text="City:").grid(row=1, column=0, sticky="w", pady=5)
        city_entry = tk.Entry(address_frame)
        city_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(address_frame, text="State:").grid(row=2, column=0, sticky="w", pady=5)
        state_entry = tk.Entry(address_frame)
        state_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(address_frame, text="Country:").grid(row=3, column=0, sticky="w", pady=5)
        country_entry = tk.Entry(address_frame)
        country_entry.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(address_frame, text="Postal Code:").grid(row=4, column=0, sticky="w", pady=5)
        postal_code_entry = tk.Entry(address_frame)
        postal_code_entry.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
        
        # Nominee Information
        nominee_frame = tk.LabelFrame(form_frame, text="Nominee Information", padx=10, pady=10)
        nominee_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        tk.Label(nominee_frame, text="Nominee Name:").grid(row=0, column=0, sticky="w", pady=5)
        nominee_name_entry = tk.Entry(nominee_frame)
        nominee_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(nominee_frame, text="Nominee Relation:").grid(row=1, column=0, sticky="w", pady=5)
        nominee_relation_entry = tk.Entry(nominee_frame)
        nominee_relation_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Account Information
        account_frame = tk.LabelFrame(form_frame, text="Account Information", padx=10, pady=10)
        account_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        tk.Label(account_frame, text="Account Type:").grid(row=0, column=0, sticky="w", pady=5)
        account_type_var = tk.StringVar(value="Savings")
        tk.OptionMenu(account_frame, account_type_var, "Savings", "Current", "Fixed Deposit").grid(row=0, column=1, sticky="ew")
        
        tk.Label(account_frame, text="Initial Deposit:").grid(row=1, column=0, sticky="w", pady=5)
        initial_deposit_entry = tk.Entry(account_frame)
        initial_deposit_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def create_account():
            # Validate inputs
            required_fields = [
                (first_name_entry, "First name"),
                (last_name_entry, "Last name"),
                (email_entry, "Email"),
                (phone_entry, "Phone"),
                (address_entry, "Address"),
                (city_entry, "City"),
                (state_entry, "State"),
                (country_entry, "Country"),
                (postal_code_entry, "Postal code")
            ]
            
            for field, name in required_fields:
                if not field.get().strip():
                    messagebox.showerror("Error", f"Please enter {name}")
                    return
            
            try:
                # Create customer record
                cursor = self.connection.cursor()
                
                customer_data = {
                    'first_name': first_name_entry.get(),
                    'last_name': last_name_entry.get(),
                    'date_of_birth': dob_entry.get(),
                    'gender': gender_var.get(),
                    'address': address_entry.get(),
                    'city': city_entry.get(),
                    'state': state_entry.get(),
                    'country': country_entry.get(),
                    'postal_code': postal_code_entry.get(),
                    'phone': phone_entry.get(),
                    'email': email_entry.get(),
                    'nominee_name': nominee_name_entry.get() or None,
                    'nominee_relation': nominee_relation_entry.get() or None
                }
                
                cursor.execute("""
                    INSERT INTO customers (first_name, last_name, date_of_birth, gender, address, city, state, 
                                         country, postal_code, phone, email, nominee_name, nominee_relation)
                    VALUES (%(first_name)s, %(last_name)s, %(date_of_birth)s, %(gender)s, %(address)s, %(city)s, 
                            %(state)s, %(country)s, %(postal_code)s, %(phone)s, %(email)s, %(nominee_name)s, %(nominee_relation)s)
                """, customer_data)
                
                customer_id = cursor.lastrowid
                
                # Create account record
                account_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
                initial_deposit = float(initial_deposit_entry.get()) if initial_deposit_entry.get() else 0.0
                
                cursor.execute("""
                    INSERT INTO accounts (customer_id, account_type, account_number, balance)
                    VALUES (%s, %s, %s, %s)
                """, (customer_id, account_type_var.get(), account_number, initial_deposit))
                
                account_id = cursor.lastrowid
                
                # Record initial deposit transaction if any
                if initial_deposit > 0:
                    cursor.execute("""
                        INSERT INTO transactions (account_id, transaction_type, amount, description)
                        VALUES (%s, 'Deposit', %s, 'Initial deposit')
                    """, (account_id, initial_deposit))
                
                self.connection.commit()
                
                messagebox.showinfo("Success", 
                    f"Customer account created successfully!\n\n"
                    f"Customer ID: {customer_id}\n"
                    f"Account Number: {account_number}\n"
                    f"Account Type: {account_type_var.get()}\n"
                    f"Initial Balance: {initial_deposit}")
                
                create_window.destroy()
                
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to create account: {e}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid initial deposit amount")
        
        create_button = tk.Button(button_frame, text="Create Account", command=create_account, 
                                bg=self.secondary_color, fg="white", font=self.button_font)
        create_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=create_window.destroy,
                                bg=self.accent_color, fg="white", font=self.button_font)
        cancel_button.pack(side="left", padx=10)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
    
    def show_loan_calculator(self):
        # Create a new window
        calculator_window = tk.Toplevel(self.root)
        calculator_window.title("Loan Calculator")
        calculator_window.geometry("500x400")
        calculator_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(calculator_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Loan Calculator", font=self.title_font).pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Loan type
        tk.Label(form_frame, text="Loan Type:").grid(row=0, column=0, sticky="w", pady=5)
        loan_type_var = tk.StringVar(value="Home")
        loan_types = ["Home", "Personal", "Business", "Education", "Car"]
        tk.OptionMenu(form_frame, loan_type_var, *loan_types).grid(row=0, column=1, sticky="ew")
        
        # Loan amount
        tk.Label(form_frame, text="Loan Amount:").grid(row=1, column=0, sticky="w", pady=5)
        loan_amount_entry = tk.Entry(form_frame)
        loan_amount_entry.grid(row=1, column=1, pady=5, sticky="ew")
        
        # Interest rate
        tk.Label(form_frame, text="Interest Rate (%):").grid(row=2, column=0, sticky="w", pady=5)
        interest_rate_entry = tk.Entry(form_frame)
        interest_rate_entry.grid(row=2, column=1, pady=5, sticky="ew")
        
        # Loan term
        tk.Label(form_frame, text="Loan Term (months):").grid(row=3, column=0, sticky="w", pady=5)
        loan_term_entry = tk.Entry(form_frame)
        loan_term_entry.grid(row=3, column=1, pady=5, sticky="ew")
        
        # Result frame
        result_frame = tk.LabelFrame(form_frame, text="Calculation Results", padx=10, pady=10)
        result_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
        
        tk.Label(result_frame, text="Monthly Payment:").grid(row=0, column=0, sticky="w")
        monthly_payment_label = tk.Label(result_frame, text="Rs0.00", font=("Helvetica", 12, "bold"))
        monthly_payment_label.grid(row=0, column=1, sticky="e")
        
        tk.Label(result_frame, text="Total Interest:").grid(row=1, column=0, sticky="w")
        total_interest_label = tk.Label(result_frame, text="Rs0.00", font=("Helvetica", 12, "bold"))
        total_interest_label.grid(row=1, column=1, sticky="e")
        
        tk.Label(result_frame, text="Total Payment:").grid(row=2, column=0, sticky="w")
        total_payment_label = tk.Label(result_frame, text="Rs0.00", font=("Helvetica", 12, "bold"))
        total_payment_label.grid(row=2, column=1, sticky="e")
        
        def calculate_loan():
            try:
                loan_amount = float(loan_amount_entry.get())
                interest_rate = float(interest_rate_entry.get()) / 100 / 12  # Monthly rate
                loan_term = int(loan_term_entry.get())
                
                if loan_amount <= 0 or interest_rate <= 0 or loan_term <= 0:
                    raise ValueError("Values must be positive")
                
                # Calculate monthly payment
                monthly_payment = (loan_amount * interest_rate * (1 + interest_rate)**loan_term) / \
                                ((1 + interest_rate)**loan_term - 1)
                
                total_payment = monthly_payment * loan_term
                total_interest = total_payment - loan_amount
                
                # Update labels
                monthly_payment_label.config(text=f"Rs{monthly_payment:,.2f}")
                total_interest_label.config(text=f"Rs{total_interest:,.2f}")
                total_payment_label.config(text=f"Rs{total_payment:,.2f}")
                
            except ValueError as e:
                messagebox.showerror("Input Error", f"Please enter valid numbers: {e}")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        calculate_button = tk.Button(button_frame, text="Calculate", command=calculate_loan, 
                                  bg=self.secondary_color, fg="white", font=self.button_font)
        calculate_button.pack(side="left", padx=10)
        
        close_button = tk.Button(button_frame, text="Close", command=calculator_window.destroy,
                               bg=self.accent_color, fg="white", font=self.button_font)
        close_button.pack(side="left", padx=10)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
    
    def show_atm_locator(self):
        # Create a new window
        atm_window = tk.Toplevel(self.root)
        atm_window.title("ATM Locator")
        atm_window.geometry("800x600")
        atm_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(atm_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="ATM Locator", font=self.title_font).pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search Location:").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        def search_atms():
            search_term = search_entry.get().strip()
            query = "SELECT * FROM atm_locations"
            params = ()
            
            if search_term:
                query += " WHERE location_name LIKE %s OR city LIKE %s OR state LIKE %s"
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
            
            try:
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute(query, params)
                atms = cursor.fetchall()
                
                # Clear existing items
                for item in atm_tree.get_children():
                    atm_tree.delete(item)
                
                # Add new items
                for atm in atms:
                    atm_tree.insert("", "end", values=(
                        atm['location_name'],
                        atm['address'],
                        atm['city'],
                        atm['state'],
                        atm['postal_code']
                    ))
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to fetch ATM locations: {e}")
        
        search_button = tk.Button(search_frame, text="Search", command=search_atms,
                                bg=self.secondary_color, fg="white")
        search_button.pack(side="left", padx=5)
        
        # ATM Treeview
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("Location", "Address", "City", "State", "Postal Code")
        atm_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            atm_tree.heading(col, text=col)
            atm_tree.column(col, width=150, anchor="w")
        
        atm_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=atm_tree.yview)
        scrollbar.pack(side="right", fill="y")
        atm_tree.configure(yscrollcommand=scrollbar.set)
        
        # Map button
        def show_on_map():
            selected = atm_tree.focus()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select an ATM location first")
                return
            
            item = atm_tree.item(selected)
            location = item['values'][0]
            address = ", ".join(item['values'][1:4])
            
            # In a real application, you would integrate with Google Maps API
            # For this demo, we'll just show a message
            messagebox.showinfo("Map Location", 
                             f"ATM Location: {location}\n"
                             f"Address: {address}\n\n"
                             "In a real application, this would open a map view.")
            
            # This would be the actual implementation to open in browser:
            # webbrowser.open(f"https://www.google.com/maps/search/?api=1&query={address}")
        
        map_button = tk.Button(main_frame, text="Show on Map", command=show_on_map,
                              bg=self.secondary_color, fg="white", font=self.button_font)
        map_button.pack(pady=10)
        
        # Close button
        close_button = tk.Button(main_frame, text="Close", command=atm_window.destroy,
                               bg=self.accent_color, fg="white", font=self.button_font)
        close_button.pack(pady=10)
        
        # Load initial data
        search_atms()
    
    def show_loan_schemes(self):
        # Create a new window
        schemes_window = tk.Toplevel(self.root)
        schemes_window.title("Loan Schemes")
        schemes_window.geometry("800x600")
        schemes_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(schemes_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Loan Schemes", font=self.title_font).pack(pady=10)
        
        # Treeview frame
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        
        # Columns
        columns = ("Scheme Name", "Loan Type", "Min Amount", "Max Amount", "Interest Rate", "Min Term", "Max Term")
        
        # Treeview
        schemes_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Configure columns
        for col in columns:
            schemes_tree.heading(col, text=col)
            schemes_tree.column(col, width=100, anchor="w")
        
        schemes_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=schemes_tree.yview)
        scrollbar.pack(side="right", fill="y")
        schemes_tree.configure(yscrollcommand=scrollbar.set)
        
        # Load data
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM loan_schemes")
            schemes = cursor.fetchall()
            
            for scheme in schemes:
                schemes_tree.insert("", "end", values=(
                    scheme['scheme_name'],
                    scheme['loan_type'],
                    f"Rs{scheme['min_amount']:,.2f}",
                    f"Rs{scheme['max_amount']:,.2f}",
                    f"{scheme['interest_rate']}%",
                    f"{scheme['min_term_months']} months",
                    f"{scheme['max_term_months']} months"
                ))
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load loan schemes: {e}")
        
        # Details frame
        details_frame = tk.LabelFrame(main_frame, text="Scheme Details", padx=10, pady=10)
        details_frame.pack(fill="x", pady=10)
        
        # Description label
        description_label = tk.Label(details_frame, text="Select a scheme to view details", wraplength=700, justify="left")
        description_label.pack(fill="x")
        
        def show_scheme_details(event):
            selected = schemes_tree.focus()
            if not selected:
                return
            
            item = schemes_tree.item(selected)
            scheme_name = item['values'][0]
            
            try:
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute("SELECT description FROM loan_schemes WHERE scheme_name = %s", (scheme_name,))
                scheme = cursor.fetchone()
                
                if scheme and scheme['description']:
                    description_label.config(text=scheme['description'])
                else:
                    description_label.config(text="No description available for this scheme")
                    
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to fetch scheme details: {e}")
        
        schemes_tree.bind("<<TreeviewSelect>>", show_scheme_details)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        close_button = tk.Button(button_frame, text="Close", command=schemes_window.destroy,
                               bg=self.accent_color, fg="white", font=self.button_font)
        close_button.pack()
    
    def show_employee_management(self):
        # Create a new window
        emp_window = tk.Toplevel(self.root)
        emp_window.title("Employee Management")
        emp_window.geometry("1000x700")
        emp_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(emp_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Employee Management", font=self.title_font).pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        def refresh_employees():
            try:
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM employees")
                employees = cursor.fetchall()
                
                # Clear existing items
                for item in emp_tree.get_children():
                    emp_tree.delete(item)
                
                # Add new items
                for emp in employees:
                    emp_tree.insert("", "end", values=(
                        emp['employee_id'],
                        f"{emp['first_name']} {emp['last_name']}",
                        emp['position'],
                        emp['department'],
                        emp['hire_date'],
                        f"Rs{emp['salary']:,.2f}",
                        emp['email'],
                        emp['phone']
                    ))
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to fetch employees: {e}")
        
        refresh_button = tk.Button(button_frame, text="Refresh", command=refresh_employees,
                                 bg=self.secondary_color, fg="white", font=self.button_font)
        refresh_button.pack(side="left", padx=5)
        
        add_button = tk.Button(button_frame, text="Add Employee", command=self.show_add_employee,
                             bg=self.secondary_color, fg="white", font=self.button_font)
        add_button.pack(side="left", padx=5)
        
        edit_button = tk.Button(button_frame, text="Edit Employee", command=lambda: self.edit_employee(emp_tree),
                              bg=self.secondary_color, fg="white", font=self.button_font)
        edit_button.pack(side="left", padx=5)
        
        delete_button = tk.Button(button_frame, text="Delete Employee", command=lambda: self.delete_employee(emp_tree),
                                bg=self.accent_color, fg="white", font=self.button_font)
        delete_button.pack(side="left", padx=5)
        
        # Employee Treeview
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Name", "Position", "Department", "Hire Date", "Salary", "Email", "Phone")
        emp_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            emp_tree.heading(col, text=col)
            emp_tree.column(col, width=100, anchor="w")
        
        emp_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=emp_tree.yview)
        scrollbar.pack(side="right", fill="y")
        emp_tree.configure(yscrollcommand=scrollbar.set)
        
        # Close button
        close_button = tk.Button(main_frame, text="Close", command=emp_window.destroy,
                               bg=self.accent_color, fg="white", font=self.button_font)
        close_button.pack(pady=10)
        
        # Load initial data
        refresh_employees()
    
    def show_add_employee(self):
        # Create a new window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Employee")
        add_window.geometry("600x500")
        add_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(add_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Add New Employee", font=self.title_font).pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Personal Information
        tk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=5)
        first_name_entry = tk.Entry(form_frame)
        first_name_entry.grid(row=0, column=1, pady=5, sticky="ew")
        
        tk.Label(form_frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=5)
        last_name_entry = tk.Entry(form_frame)
        last_name_entry.grid(row=1, column=1, pady=5, sticky="ew")
        
        # Job Information
        tk.Label(form_frame, text="Position:").grid(row=2, column=0, sticky="w", pady=5)
        position_entry = tk.Entry(form_frame)
        position_entry.grid(row=2, column=1, pady=5, sticky="ew")
        
        tk.Label(form_frame, text="Department:").grid(row=3, column=0, sticky="w", pady=5)
        department_entry = tk.Entry(form_frame)
        department_entry.grid(row=3, column=1, pady=5, sticky="ew")
        
        tk.Label(form_frame, text="Hire Date:").grid(row=4, column=0, sticky="w", pady=5)
        hire_date_entry = tk.Entry(form_frame)
        hire_date_entry.grid(row=4, column=1, pady=5, sticky="ew")
        hire_date_entry.insert(0, "YYYY-MM-DD")
        
        tk.Label(form_frame, text="Salary:").grid(row=5, column=0, sticky="w", pady=5)
        salary_entry = tk.Entry(form_frame)
        salary_entry.grid(row=5, column=1, pady=5, sticky="ew")
        
        # Contact Information
        tk.Label(form_frame, text="Email:").grid(row=6, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(form_frame)
        email_entry.grid(row=6, column=1, pady=5, sticky="ew")
        
        tk.Label(form_frame, text="Phone:").grid(row=7, column=0, sticky="w", pady=5)
        phone_entry = tk.Entry(form_frame)
        phone_entry.grid(row=7, column=1, pady=5, sticky="ew")
        
        tk.Label(form_frame, text="Address:").grid(row=8, column=0, sticky="w", pady=5)
        address_entry = tk.Entry(form_frame)
        address_entry.grid(row=8, column=1, pady=5, sticky="ew")
        
        def add_employee():
            # Validate inputs
            required_fields = [
                (first_name_entry, "First name"),
                (last_name_entry, "Last name"),
                (position_entry, "Position"),
                (department_entry, "Department"),
                (hire_date_entry, "Hire date"),
                (salary_entry, "Salary"),
                (email_entry, "Email"),
                (phone_entry, "Phone"),
                (address_entry, "Address")
            ]
            
            for field, name in required_fields:
                if not field.get().strip():
                    messagebox.showerror("Error", f"Please enter {name}")
                    return
            
            try:
                # Create employee record
                cursor = self.connection.cursor()
                
                employee_data = {
                    'first_name': first_name_entry.get(),
                    'last_name': last_name_entry.get(),
                    'position': position_entry.get(),
                    'department': department_entry.get(),
                    'hire_date': hire_date_entry.get(),
                    'salary': float(salary_entry.get()),
                    'email': email_entry.get(),
                    'phone': phone_entry.get(),
                    'address': address_entry.get()
                }
                
                cursor.execute("""
                    INSERT INTO employees (first_name, last_name, position, department, hire_date, 
                                         salary, email, phone, address)
                    VALUES (%(first_name)s, %(last_name)s, %(position)s, %(department)s, %(hire_date)s, 
                            %(salary)s, %(email)s, %(phone)s, %(address)s)
                """, employee_data)
                
                self.connection.commit()
                
                messagebox.showinfo("Success", "Employee added successfully!")
                add_window.destroy()
                
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to add employee: {e}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid salary amount")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        save_button = tk.Button(button_frame, text="Save", command=add_employee, 
                              bg=self.secondary_color, fg="white", font=self.button_font)
        save_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=add_window.destroy,
                                bg=self.accent_color, fg="white", font=self.button_font)
        cancel_button.pack(side="left", padx=10)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
    
    def edit_employee(self, emp_tree):
        selected = emp_tree.focus()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an employee to edit")
            return
        
        item = emp_tree.item(selected)
        emp_id = item['values'][0]
        
        # Fetch employee details
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (emp_id,))
            employee = cursor.fetchone()
            
            if not employee:
                messagebox.showerror("Error", "Selected employee not found")
                return
            
            # Create a new window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Employee")
            edit_window.geometry("600x500")
            edit_window.grab_set()
            
            # Main frame
            main_frame = tk.Frame(edit_window, padx=20, pady=20)
            main_frame.pack(fill="both", expand=True)
            
            # Title
            tk.Label(main_frame, text="Edit Employee", font=self.title_font).pack(pady=10)
            
            # Form frame
            form_frame = tk.Frame(main_frame)
            form_frame.pack(fill="both", expand=True, pady=10)
            
            # Personal Information
            tk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=5)
            first_name_entry = tk.Entry(form_frame)
            first_name_entry.grid(row=0, column=1, pady=5, sticky="ew")
            first_name_entry.insert(0, employee['first_name'])
            
            tk.Label(form_frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=5)
            last_name_entry = tk.Entry(form_frame)
            last_name_entry.grid(row=1, column=1, pady=5, sticky="ew")
            last_name_entry.insert(0, employee['last_name'])
            
            # Job Information
            tk.Label(form_frame, text="Position:").grid(row=2, column=0, sticky="w", pady=5)
            position_entry = tk.Entry(form_frame)
            position_entry.grid(row=2, column=1, pady=5, sticky="ew")
            position_entry.insert(0, employee['position'])
            
            tk.Label(form_frame, text="Department:").grid(row=3, column=0, sticky="w", pady=5)
            department_entry = tk.Entry(form_frame)
            department_entry.grid(row=3, column=1, pady=5, sticky="ew")
            department_entry.insert(0, employee['department'])
            
            tk.Label(form_frame, text="Hire Date:").grid(row=4, column=0, sticky="w", pady=5)
            hire_date_entry = tk.Entry(form_frame)
            hire_date_entry.grid(row=4, column=1, pady=5, sticky="ew")
            hire_date_entry.insert(0, str(employee['hire_date']))
            
            tk.Label(form_frame, text="Salary:").grid(row=5, column=0, sticky="w", pady=5)
            salary_entry = tk.Entry(form_frame)
            salary_entry.grid(row=5, column=1, pady=5, sticky="ew")
            salary_entry.insert(0, str(employee['salary']))
            
            # Contact Information
            tk.Label(form_frame, text="Email:").grid(row=6, column=0, sticky="w", pady=5)
            email_entry = tk.Entry(form_frame)
            email_entry.grid(row=6, column=1, pady=5, sticky="ew")
            email_entry.insert(0, employee['email'])
            
            tk.Label(form_frame, text="Phone:").grid(row=7, column=0, sticky="w", pady=5)
            phone_entry = tk.Entry(form_frame)
            phone_entry.grid(row=7, column=1, pady=5, sticky="ew")
            phone_entry.insert(0, employee['phone'])
            
            tk.Label(form_frame, text="Address:").grid(row=8, column=0, sticky="w", pady=5)
            address_entry = tk.Entry(form_frame)
            address_entry.grid(row=8, column=1, pady=5, sticky="ew")
            address_entry.insert(0, employee['address'])
            
            def update_employee():
                # Validate inputs
                required_fields = [
                    (first_name_entry, "First name"),
                    (last_name_entry, "Last name"),
                    (position_entry, "Position"),
                    (department_entry, "Department"),
                    (hire_date_entry, "Hire date"),
                    (salary_entry, "Salary"),
                    (email_entry, "Email"),
                    (phone_entry, "Phone"),
                    (address_entry, "Address")
                ]
                
                for field, name in required_fields:
                    if not field.get().strip():
                        messagebox.showerror("Error", f"Please enter {name}")
                        return
                
                try:
                    # Update employee record
                    cursor = self.connection.cursor()
                    
                    employee_data = {
                        'employee_id': emp_id,
                        'first_name': first_name_entry.get(),
                        'last_name': last_name_entry.get(),
                        'position': position_entry.get(),
                        'department': department_entry.get(),
                        'hire_date': hire_date_entry.get(),
                        'salary': float(salary_entry.get()),
                        'email': email_entry.get(),
                        'phone': phone_entry.get(),
                        'address': address_entry.get()
                    }
                    
                    cursor.execute("""
                        UPDATE employees 
                        SET first_name = %(first_name)s, last_name = %(last_name)s, 
                            position = %(position)s, department = %(department)s, 
                            hire_date = %(hire_date)s, salary = %(salary)s, 
                            email = %(email)s, phone = %(phone)s, address = %(address)s
                        WHERE employee_id = %(employee_id)s
                    """, employee_data)
                    
                    self.connection.commit()
                    
                    messagebox.showinfo("Success", "Employee updated successfully!")
                    edit_window.destroy()
                    
                except Error as e:
                    self.connection.rollback()
                    messagebox.showerror("Database Error", f"Failed to update employee: {e}")
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid salary amount")
            
            # Button frame
            button_frame = tk.Frame(main_frame)
            button_frame.pack(pady=10)
            
            save_button = tk.Button(button_frame, text="Save", command=update_employee, 
                                  bg=self.secondary_color, fg="white", font=self.button_font)
            save_button.pack(side="left", padx=10)
            
            cancel_button = tk.Button(button_frame, text="Cancel", command=edit_window.destroy,
                                    bg=self.accent_color, fg="white", font=self.button_font)
            cancel_button.pack(side="left", padx=10)
            
            # Configure grid weights
            form_frame.grid_columnconfigure(1, weight=1)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch employee details: {e}")
    
    def delete_employee(self, emp_tree):
        selected = emp_tree.focus()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an employee to delete")
            return
        
        item = emp_tree.item(selected)
        emp_id = item['values'][0]
        emp_name = item['values'][1]
        
        confirm = messagebox.askyesno("Confirm Deletion", 
                                    f"Are you sure you want to delete employee {emp_name} (ID: {emp_id})?")
        
        if confirm:
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM employees WHERE employee_id = %s", (emp_id,))
                self.connection.commit()
                
                messagebox.showinfo("Success", "Employee deleted successfully!")
                
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to delete employee: {e}")
    
    def show_customers_list(self):
        # Create a new window
        customers_window = tk.Toplevel(self.root)
        customers_window.title("Customer List")
        customers_window.geometry("1000x700")
        customers_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(customers_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Customer List", font=self.title_font).pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        def search_customers():
            search_term = search_entry.get().strip()
            query = """
                SELECT c.customer_id, c.first_name, c.last_name, c.email, c.phone, 
                       a.account_number, a.account_type, a.balance
                FROM customers c
                LEFT JOIN accounts a ON c.customer_id = a.customer_id
            """
            params = ()
            
            if search_term:
                query += " WHERE c.first_name LIKE %s OR c.last_name LIKE %s OR c.email LIKE %s OR c.phone LIKE %s OR a.account_number LIKE %s"
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
            
            try:
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute(query, params)
                customers = cursor.fetchall()
                
                # Clear existing items
                for item in cust_tree.get_children():
                    cust_tree.delete(item)
                
                # Add new items
                for cust in customers:
                    cust_tree.insert("", "end", values=(
                        cust['customer_id'],
                        f"{cust['first_name']} {cust['last_name']}",
                        cust['email'],
                        cust['phone'],
                        cust['account_number'] if cust['account_number'] else "N/A",
                        cust['account_type'] if cust['account_type'] else "N/A",
                        f"Rs{cust['balance']:,.2f}" if cust['balance'] is not None else "N/A"
                    ))
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to fetch customers: {e}")
        
        search_button = tk.Button(search_frame, text="Search", command=search_customers,
                                bg=self.secondary_color, fg="white")
        search_button.pack(side="left", padx=5)
        
        # Customer Treeview
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("Customer ID", "Name", "Email", "Phone", "Account No.", "Account Type", "Balance")
        cust_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            cust_tree.heading(col, text=col)
            cust_tree.column(col, width=120, anchor="w")
        
        cust_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=cust_tree.yview)
        scrollbar.pack(side="right", fill="y")
        cust_tree.configure(yscrollcommand=scrollbar.set)
        
        # View details button
        def view_customer_details():
            selected = cust_tree.focus()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a customer first")
                return
            
            item = cust_tree.item(selected)
            customer_id = item['values'][0]
            
            # Show customer details in a new window
            self.show_customer_details_admin(customer_id)
        
        details_button = tk.Button(main_frame, text="View Details", command=view_customer_details,
                                 bg=self.secondary_color, fg="white", font=self.button_font)
        details_button.pack(pady=10)
        
        # Close button
        close_button = tk.Button(main_frame, text="Close", command=customers_window.destroy,
                               bg=self.accent_color, fg="white", font=self.button_font)
        close_button.pack(pady=10)
        
        # Load initial data
        search_customers()
    
    def show_customer_details_admin(self, customer_id):
        # Create a new window
        details_window = tk.Toplevel(self.root)
        details_window.title("Customer Details")
        details_window.geometry("800x600")
        details_window.grab_set()
        
        # Fetch customer details
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Get customer info
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            customer = cursor.fetchone()
            
            if not customer:
                messagebox.showerror("Error", "Customer not found")
                details_window.destroy()
                return
            
            # Get accounts
            cursor.execute("SELECT * FROM accounts WHERE customer_id = %s", (customer_id,))
            accounts = cursor.fetchall()
            
            # Get loans
            cursor.execute("SELECT * FROM loans WHERE customer_id = %s", (customer_id,))
            loans = cursor.fetchall()
            
            # Get cards
            cursor.execute("SELECT * FROM cards WHERE customer_id = %s", (customer_id,))
            cards = cursor.fetchall()
            
            # Main frame
            main_frame = tk.Frame(details_window, padx=20, pady=20)
            main_frame.pack(fill="both", expand=True)
            
            # Title
            tk.Label(main_frame, text=f"Customer Details - {customer['first_name']} {customer['last_name']}", 
                   font=self.title_font).pack(pady=10)
            
            # Notebook for tabs
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill="both", expand=True)
            
            # Personal Info Tab
            personal_frame = tk.Frame(notebook, padx=10, pady=10)
            notebook.add(personal_frame, text="Personal Information")
            
            # Personal info labels
            info_labels = [
                ("Customer ID:", customer['customer_id']),
                ("Name:", f"{customer['first_name']} {customer['last_name']}"),
                ("Date of Birth:", customer['date_of_birth']),
                ("Gender:", customer['gender']),
                ("Email:", customer['email']),
                ("Phone:", customer['phone']),
                ("Address:", customer['address']),
                ("City:", customer['city']),
                ("State:", customer['state']),
                ("Country:", customer['country']),
                ("Postal Code:", customer['postal_code']),
                ("Nominee Name:", customer['nominee_name'] or "N/A"),
                ("Nominee Relation:", customer['nominee_relation'] or "N/A")
            ]
            
            for i, (label, value) in enumerate(info_labels):
                tk.Label(personal_frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
                tk.Label(personal_frame, text=value).grid(row=i, column=1, sticky="w", pady=2)
            
            # Accounts Tab
            accounts_frame = tk.Frame(notebook)
            notebook.add(accounts_frame, text="Accounts")
            
            if accounts:
                columns = ("Account ID", "Account Number", "Type", "Balance", "Status", "Opened Date")
                accounts_tree = ttk.Treeview(accounts_frame, columns=columns, show="headings")
                
                for col in columns:
                    accounts_tree.heading(col, text=col)
                    accounts_tree.column(col, width=120, anchor="w")
                
                for account in accounts:
                    accounts_tree.insert("", "end", values=(
                        account['account_id'],
                        account['account_number'],
                        account['account_type'],
                        f"Rs{account['balance']:,.2f}",
                        account['status'],
                        account['opened_date'].strftime("%Y-%m-%d") if account['opened_date'] else "N/A"
                    ))
                
                accounts_tree.pack(fill="both", expand=True)
            else:
                tk.Label(accounts_frame, text="No accounts found for this customer").pack(pady=50)
            
            # Loans Tab
            loans_frame = tk.Frame(notebook)
            notebook.add(loans_frame, text="Loans")
            
            if loans:
                columns = ("Loan ID", "Type", "Amount", "Interest Rate", "Term", "Monthly Payment", "Remaining", "Status")
                loans_tree = ttk.Treeview(loans_frame, columns=columns, show="headings")
                
                for col in columns:
                    loans_tree.heading(col, text=col)
                    loans_tree.column(col, width=100, anchor="w")
                
                for loan in loans:
                    loans_tree.insert("", "end", values=(
                        loan['loan_id'],
                        loan['loan_type'],
                        f"Rs{loan['loan_amount']:,.2f}",
                        f"{loan['interest_rate']}%",
                        f"{loan['term_months']} months",
                        f"Rs{loan['monthly_payment']:,.2f}",
                        f"Rs{loan['remaining_balance']:,.2f}",
                        loan['status']
                    ))
                
                loans_tree.pack(fill="both", expand=True)
            else:
                tk.Label(loans_frame, text="No loans found for this customer").pack(pady=50)
            
            # Cards Tab
            cards_frame = tk.Frame(notebook)
            notebook.add(cards_frame, text="Cards")
            
            if cards:
                columns = ("Card ID", "Type", "Card Number", "Expiry Date", "Status")
                cards_tree = ttk.Treeview(cards_frame, columns=columns, show="headings")
                
                for col in columns:
                    cards_tree.heading(col, text=col)
                    cards_tree.column(col, width=120, anchor="w")
                
                for card in cards:
                    # Mask card number except last 4 digits
                    card_number = f"**** **** **** {card['card_number'][-4:]}" if card['card_number'] else "N/A"
                    
                    cards_tree.insert("", "end", values=(
                        card['card_id'],
                        card['card_type'],
                        card_number,
                        card['expiry_date'].strftime("%m/%Y") if card['expiry_date'] else "N/A",
                        card['status']
                    ))
                
                cards_tree.pack(fill="both", expand=True)
            else:
                tk.Label(cards_frame, text="No cards found for this customer").pack(pady=50)
            
            # Close button
            close_button = tk.Button(main_frame, text="Close", command=details_window.destroy,
                                   bg=self.accent_color, fg="white", font=self.button_font)
            close_button.pack(pady=10)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch customer details: {e}")
            details_window.destroy()
    
    def generate_reports(self):
        # Create a new window
        report_window = tk.Toplevel(self.root)
        report_window.title("Generate Reports")
        report_window.geometry("600x400")
        report_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(report_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Generate Reports", font=self.title_font).pack(pady=10)
        
        # Report options
        report_frame = tk.Frame(main_frame)
        report_frame.pack(fill="both", expand=True, pady=20)
        
        report_options = [
            ("Customer List", "customer_list"),
            ("Account Summary", "account_summary"),
            ("Transaction History", "transaction_history"),
            ("Loan Portfolio", "loan_portfolio"),
            ("Employee Directory", "employee_directory")
        ]
        
        self.report_var = tk.StringVar(value=report_options[0][1])
        
        for i, (text, value) in enumerate(report_options):
            tk.Radiobutton(report_frame, text=text, variable=self.report_var, 
                          value=value, bg=self.light_color).grid(row=i, column=0, sticky="w", pady=5)
        
        # Date range
        date_frame = tk.LabelFrame(report_frame, text="Date Range (if applicable)", padx=10, pady=10)
        date_frame.grid(row=len(report_options), column=0, pady=10, sticky="ew")
        
        tk.Label(date_frame, text="From:").grid(row=0, column=0, padx=5)
        self.from_date_entry = tk.Entry(date_frame)
        self.from_date_entry.grid(row=0, column=1, padx=5)
        self.from_date_entry.insert(0, "YYYY-MM-DD")
        
        tk.Label(date_frame, text="To:").grid(row=0, column=2, padx=5)
        self.to_date_entry = tk.Entry(date_frame)
        self.to_date_entry.grid(row=0, column=3, padx=5)
        self.to_date_entry.insert(0, "YYYY-MM-DD")
        
        # Format options
        format_frame = tk.LabelFrame(report_frame, text="Report Format", padx=10, pady=10)
        format_frame.grid(row=len(report_options)+1, column=0, pady=10, sticky="ew")
        
        self.format_var = tk.StringVar(value="pdf")
        tk.Radiobutton(format_frame, text="PDF", variable=self.format_var, value="pdf", bg=self.light_color).pack(side="left", padx=10)
        tk.Radiobutton(format_frame, text="CSV", variable=self.format_var, value="csv", bg=self.light_color).pack(side="left", padx=10)
        tk.Radiobutton(format_frame, text="Text", variable=self.format_var, value="txt", bg=self.light_color).pack(side="left", padx=10)
        
        def generate_report():
            report_type = self.report_var.get()
            from_date = self.from_date_entry.get()
            to_date = self.to_date_entry.get()
            report_format = self.format_var.get()
            
            try:
                cursor = self.connection.cursor(dictionary=True)
                
                if report_type == "customer_list":
                    query = "SELECT * FROM customers ORDER BY last_name, first_name"
                    cursor.execute(query)
                    data = cursor.fetchall()
                    
                    if report_format == "pdf":
                        self.generate_pdf_report("Customer List", ["ID", "Name", "Email", "Phone", "City"], 
                                              [(str(c['customer_id']), f"{c['first_name']} {c['last_name']}", 
                                               c['email'], c['phone'], c['city']) for c in data])
                    elif report_format == "csv":
                        self.generate_csv_report("customer_list", ["ID", "Name", "Email", "Phone", "City"], 
                                              [(str(c['customer_id']), f"{c['first_name']} {c['last_name']}", 
                                               c['email'], c['phone'], c['city']) for c in data])
                    else:
                        self.generate_text_report("customer_list", ["ID", "Name", "Email", "Phone", "City"], 
                                               [(str(c['customer_id']), f"{c['first_name']} {c['last_name']}", 
                                                c['email'], c['phone'], c['city']) for c in data])
                
                elif report_type == "account_summary":
                    query = """
                        SELECT a.account_id, a.account_number, a.account_type, a.balance, 
                               c.customer_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name
                        FROM accounts a
                        JOIN customers c ON a.customer_id = c.customer_id
                        ORDER BY a.account_type, a.balance DESC
                    """
                    cursor.execute(query)
                    data = cursor.fetchall()
                    
                    if report_format == "pdf":
                        self.generate_pdf_report("Account Summary", ["Account No.", "Type", "Balance", "Customer"], 
                                              [(a['account_number'], a['account_type'], 
                                                f"Rs{a['balance']:,.2f}", a['customer_name']) for a in data])
                    elif report_format == "csv":
                        self.generate_csv_report("account_summary", ["Account No.", "Type", "Balance", "Customer"], 
                                              [(a['account_number'], a['account_type'], 
                                                str(a['balance']), a['customer_name']) for a in data])
                    else:
                        self.generate_text_report("account_summary", ["Account No.", "Type", "Balance", "Customer"], 
                                               [(a['account_number'], a['account_type'], 
                                                 f"Rs{a['balance']:,.2f}", a['customer_name']) for a in data])
                
                elif report_type == "transaction_history":
                    if from_date == "YYYY-MM-DD" or to_date == "YYYY-MM-DD":
                        messagebox.showwarning("Date Required", "Please specify a date range for transaction history")
                        return
                    
                    query = """
                        SELECT t.transaction_id, t.transaction_type, t.amount, t.transaction_date, 
                               a.account_number, CONCAT(c.first_name, ' ', c.last_name) AS customer_name
                        FROM transactions t
                        JOIN accounts a ON t.account_id = a.account_id
                        JOIN customers c ON a.customer_id = c.customer_id
                        WHERE t.transaction_date BETWEEN %s AND %s
                        ORDER BY t.transaction_date DESC
                    """
                    cursor.execute(query, (from_date, to_date))
                    data = cursor.fetchall()
                    
                    if report_format == "pdf":
                        self.generate_pdf_report("Transaction History", ["Date", "Type", "Amount", "Account", "Customer"], 
                                              [(t['transaction_date'].strftime("%Y-%m-%d"), t['transaction_type'], 
                                               f"Rs{t['amount']:,.2f}", t['account_number'], t['customer_name']) for t in data])
                    elif report_format == "csv":
                        self.generate_csv_report("transaction_history", ["Date", "Type", "Amount", "Account", "Customer"], 
                                              [(t['transaction_date'].strftime("%Y-%m-%d"), t['transaction_type'], 
                                               str(t['amount']), t['account_number'], t['customer_name']) for t in data])
                    else:
                        self.generate_text_report("transaction_history", ["Date", "Type", "Amount", "Account", "Customer"], 
                                               [(t['transaction_date'].strftime("%Y-%m-%d"), t['transaction_type'], 
                                                f"Rs{t['amount']:,.2f}", t['account_number'], t['customer_name']) for t in data])
                
                elif report_type == "loan_portfolio":
                    query = """
                        SELECT l.loan_id, l.loan_type, l.loan_amount, l.interest_rate, l.term_months, 
                               l.monthly_payment, l.remaining_balance, l.status,
                               CONCAT(c.first_name, ' ', c.last_name) AS customer_name
                        FROM loans l
                        JOIN customers c ON l.customer_id = c.customer_id
                        ORDER BY l.loan_type, l.remaining_balance DESC
                    """
                    cursor.execute(query)
                    data = cursor.fetchall()
                    
                    if report_format == "pdf":
                        self.generate_pdf_report("Loan Portfolio", ["Type", "Amount", "Interest", "Term", "Monthly", "Remaining", "Status", "Customer"], 
                                              [(l['loan_type'], f"Rs{l['loan_amount']:,.2f}", f"{l['interest_rate']}%", 
                                               f"{l['term_months']} months", f"Rs{l['monthly_payment']:,.2f}", 
                                               f"Rs{l['remaining_balance']:,.2f}", l['status'], l['customer_name']) for l in data])
                    elif report_format == "csv":
                        self.generate_csv_report("loan_portfolio", ["Type", "Amount", "Interest", "Term", "Monthly", "Remaining", "Status", "Customer"], 
                                              [(l['loan_type'], str(l['loan_amount']), str(l['interest_rate']), 
                                               str(l['term_months']), str(l['monthly_payment']), 
                                               str(l['remaining_balance']), l['status'], l['customer_name']) for l in data])
                    else:
                        self.generate_text_report("loan_portfolio", ["Type", "Amount", "Interest", "Term", "Monthly", "Remaining", "Status", "Customer"], 
                                               [(l['loan_type'], f"Rs{l['loan_amount']:,.2f}", f"{l['interest_rate']}%", 
                                                 f"{l['term_months']} months", f"Rs{l['monthly_payment']:,.2f}", 
                                                 f"Rs{l['remaining_balance']:,.2f}", l['status'], l['customer_name']) for l in data])
                
                elif report_type == "employee_directory":
                    query = "SELECT * FROM employees ORDER BY department, last_name, first_name"
                    cursor.execute(query)
                    data = cursor.fetchall()
                    
                    if report_format == "pdf":
                        self.generate_pdf_report("Employee Directory", ["Name", "Position", "Department", "Hire Date", "Salary"], 
                                              [(f"{e['first_name']} {e['last_name']}", e['position'], e['department'], 
                                                e['hire_date'].strftime("%Y-%m-%d"), f"Rs{e['salary']:,.2f}") for e in data])
                    elif report_format == "csv":
                        self.generate_csv_report("employee_directory", ["Name", "Position", "Department", "Hire Date", "Salary"], 
                                              [(f"{e['first_name']} {e['last_name']}", e['position'], e['department'], 
                                                e['hire_date'].strftime("%Y-%m-%d"), str(e['salary'])) for e in data])
                    else:
                        self.generate_text_report("employee_directory", ["Name", "Position", "Department", "Hire Date", "Salary"], 
                                               [(f"{e['first_name']} {e['last_name']}", e['position'], e['department'], 
                                                 e['hire_date'].strftime("%Y-%m-%d"), f"Rs{e['salary']:,.2f}") for e in data])
                
                messagebox.showinfo("Success", "Report generated successfully!")
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to generate report: {e}")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        generate_button = tk.Button(button_frame, text="Generate Report", command=generate_report,
                                  bg=self.secondary_color, fg="white", font=self.button_font)
        generate_button.pack(side="left", padx=10)
        
        close_button = tk.Button(button_frame, text="Close", command=report_window.destroy,
                               bg=self.accent_color, fg="white", font=self.button_font)
        close_button.pack(side="left", padx=10)
    
    def generate_pdf_report(self, title, headers, data):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                               filetypes=[("PDF Files", "*.pdf")],
                                               title="Save PDF Report As",
                                               initialfile=f"{title.lower().replace(' ', '_')}.pdf")
        
        if not file_path:
            return
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, title, 0, 1, "C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "B", 12)
        col_widths = [pdf.get_string_width(header) + 6 for header in headers]
        
        # Adjust column widths based on data
        for row in data:
            for i, item in enumerate(row):
                if pdf.get_string_width(str(item)) + 6 > col_widths[i]:
                    col_widths[i] = pdf.get_string_width(str(item)) + 6
        
        # Create header
        pdf.set_fill_color(200, 220, 255)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1, 0, "C", 1)
        pdf.ln()
        
        # Add data
        pdf.set_font("Arial", "", 10)
        fill = False
        for row in data:
            for i, item in enumerate(row):
                pdf.cell(col_widths[i], 10, str(item), 1, 0, "L", fill)
            pdf.ln()
            fill = not fill
        
        pdf.output(file_path)
        messagebox.showinfo("Success", f"PDF report saved to:\n{file_path}")
    
    def generate_csv_report(self, default_name, headers, data):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                               filetypes=[("CSV Files", "*.csv")],
                                               title="Save CSV Report As",
                                               initialfile=f"{default_name}.csv")
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                # Write header
                csvfile.write(",".join(headers) + "\n")
                
                # Write data
                for row in data:
                    csvfile.write(",".join(str(item) for item in row) + "\n")
            
            messagebox.showinfo("Success", f"CSV report saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file: {e}")
    
    def generate_text_report(self, default_name, headers, data):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text Files", "*.txt")],
                                               title="Save Text Report As",
                                               initialfile=f"{default_name}.txt")
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", encoding="utf-8") as txtfile:
                # Write header
                txtfile.write("\t".join(headers) + "\n")
                txtfile.write("-" * (sum(len(h) for h in headers) + len(headers) * 4) + "\n")
                
                # Write data
                for row in data:
                    txtfile.write("\t".join(str(item) for item in row) + "\n")
            
            messagebox.showinfo("Success", f"Text report saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save text file: {e}")
    
    # Customer Functions
    def show_customer_details(self):
        # Create a new window
        details_window = tk.Toplevel(self.root)
        details_window.title("Customer Details")
        details_window.geometry("600x500")
        details_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(details_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Your Profile Details", font=self.title_font).pack(pady=10)
        
        # Fetch customer details
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (self.current_user['customer_id'],))
            customer = cursor.fetchone()
            
            if not customer:
                messagebox.showerror("Error", "Customer details not found")
                details_window.destroy()
                return
            
            # Personal Information
            personal_frame = tk.LabelFrame(main_frame, text="Personal Information", padx=10, pady=10)
            personal_frame.pack(fill="x", pady=10)
            
            info_labels = [
                ("Customer ID:", customer['customer_id']),
                ("Name:", f"{customer['first_name']} {customer['last_name']}"),
                ("Date of Birth:", customer['date_of_birth']),
                ("Gender:", customer['gender']),
                ("Email:", customer['email']),
                ("Phone:", customer['phone'])
            ]
            
            for i, (label, value) in enumerate(info_labels):
                tk.Label(personal_frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
                tk.Label(personal_frame, text=value).grid(row=i, column=1, sticky="w", pady=2)
            
            # Address Information
            address_frame = tk.LabelFrame(main_frame, text="Address Information", padx=10, pady=10)
            address_frame.pack(fill="x", pady=10)
            
            address_labels = [
                ("Address:", customer['address']),
                ("City:", customer['city']),
                ("State:", customer['state']),
                ("Country:", customer['country']),
                ("Postal Code:", customer['postal_code'])
            ]
            
            for i, (label, value) in enumerate(address_labels):
                tk.Label(address_frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
                tk.Label(address_frame, text=value).grid(row=i, column=1, sticky="w", pady=2)
            
            # Nominee Information
            nominee_frame = tk.LabelFrame(main_frame, text="Nominee Information", padx=10, pady=10)
            nominee_frame.pack(fill="x", pady=10)
            
            nominee_labels = [
                ("Nominee Name:", customer['nominee_name'] or "Not specified"),
                ("Nominee Relation:", customer['nominee_relation'] or "Not specified")
            ]
            
            for i, (label, value) in enumerate(nominee_labels):
                tk.Label(nominee_frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
                tk.Label(nominee_frame, text=value).grid(row=i, column=1, sticky="w", pady=2)
            
            # Close button
            close_button = tk.Button(main_frame, text="Close", command=details_window.destroy,
                                   bg=self.accent_color, fg="white", font=self.button_font)
            close_button.pack(pady=10)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch customer details: {e}")
            details_window.destroy()
    
    def show_account_details(self):
        # Create a new window
        account_window = tk.Toplevel(self.root)
        account_window.title("Account Details")
        account_window.geometry("600x400")
        account_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(account_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Your Account Details", font=self.title_font).pack(pady=10)
        
        # Fetch account details
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.* 
                FROM accounts a
                JOIN customers c ON a.customer_id = c.customer_id
                WHERE c.customer_id = %s
            """, (self.current_user['customer_id'],))
            accounts = cursor.fetchall()
            
            if not accounts:
                messagebox.showinfo("No Accounts", "You don't have any accounts yet")
                account_window.destroy()
                return
            
            # Notebook for multiple accounts
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill="both", expand=True)
            
            for account in accounts:
                # Create a tab for each account
                account_frame = tk.Frame(notebook, padx=10, pady=10)
                notebook.add(account_frame, text=f"{account['account_type']} Account")
                
                # Account details
                details = [
                    ("Account Number:", account['account_number']),
                    ("Account Type:", account['account_type']),
                    ("Current Balance:", f"Rs{account['balance']:,.2f}"),
                    ("Account Status:", account['status']),
                    ("Opened Date:", account['opened_date'].strftime("%Y-%m-%d") if account['opened_date'] else "N/A")
                ]
                
                for i, (label, value) in enumerate(details):
                    tk.Label(account_frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky="w", pady=5)
                    tk.Label(account_frame, text=value).grid(row=i, column=1, sticky="w", pady=5)
                
                # Quick actions frame
                actions_frame = tk.Frame(account_frame)
                actions_frame.grid(row=len(details), column=0, columnspan=2, pady=20)
                
                deposit_button = tk.Button(actions_frame, text="Deposit", 
                                         command=lambda a=account: self.show_deposit_window(a),
                                         bg=self.secondary_color, fg="white")
                deposit_button.pack(side="left", padx=5)
                
                withdraw_button = tk.Button(actions_frame, text="Withdraw", 
                                          command=lambda a=account: self.show_withdraw_window(a),
                                          bg=self.secondary_color, fg="white")
                withdraw_button.pack(side="left", padx=5)
                
                transfer_button = tk.Button(actions_frame, text="Transfer", 
                                          command=lambda a=account: self.show_transfer_window(a),
                                          bg=self.secondary_color, fg="white")
                transfer_button.pack(side="left", padx=5)
            
            # Close button
            close_button = tk.Button(main_frame, text="Close", command=account_window.destroy,
                                   bg=self.accent_color, fg="white", font=self.button_font)
            close_button.pack(pady=10)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch account details: {e}")
            account_window.destroy()
    
    def show_deposit_window(self, account):
        # Create a new window
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Deposit Funds")
        deposit_window.geometry("400x300")
        deposit_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(deposit_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text=f"Deposit to {account['account_type']} Account", 
               font=self.title_font).pack(pady=10)
        
        # Account info
        tk.Label(main_frame, text=f"Account Number: {account['account_number']}").pack(pady=5)
        tk.Label(main_frame, text=f"Current Balance: Rs{account['balance']:,.2f}").pack(pady=5)
        
        # Amount entry
        tk.Label(main_frame, text="Deposit Amount:").pack(pady=10)
        amount_entry = tk.Entry(main_frame, font=("Helvetica", 14))
        amount_entry.pack(pady=5)
        
        # Description
        tk.Label(main_frame, text="Description (optional):").pack(pady=10)
        desc_entry = tk.Entry(main_frame)
        desc_entry.pack(pady=5, fill="x")
        
        def process_deposit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                description = desc_entry.get() or "Deposit"
                
                # Update database
                cursor = self.connection.cursor()
                
                # Update account balance
                cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance + %s 
                    WHERE account_id = %s
                """, (amount, account['account_id']))
                
                # Record transaction
                cursor.execute("""
                    INSERT INTO transactions (account_id, transaction_type, amount, description)
                    VALUES (%s, 'Deposit', %s, %s)
                """, (account['account_id'], amount, description))
                
                self.connection.commit()
                
                messagebox.showinfo("Success", f"Deposit of Rs{amount:,.2f} processed successfully")
                deposit_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive amount")
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to process deposit: {e}")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        deposit_button = tk.Button(button_frame, text="Deposit", command=process_deposit,
                                 bg=self.secondary_color, fg="white", font=self.button_font)
        deposit_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=deposit_window.destroy,
                                bg=self.accent_color, fg="white", font=self.button_font)
        cancel_button.pack(side="left", padx=10)
    
    def show_withdraw_window(self, account):
        # Create a new window
        withdraw_window = tk.Toplevel(self.root)
        withdraw_window.title("Withdraw Funds")
        withdraw_window.geometry("400x300")
        withdraw_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(withdraw_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text=f"Withdraw from {account['account_type']} Account", 
               font=self.title_font).pack(pady=10)
        
        # Account info
        tk.Label(main_frame, text=f"Account Number: {account['account_number']}").pack(pady=5)
        tk.Label(main_frame, text=f"Current Balance: Rs{account['balance']:,.2f}").pack(pady=5)
        
        # Amount entry
        tk.Label(main_frame, text="Withdrawal Amount:").pack(pady=10)
        amount_entry = tk.Entry(main_frame, font=("Helvetica", 14))
        amount_entry.pack(pady=5)
        
        # Description
        tk.Label(main_frame, text="Description (optional):").pack(pady=10)
        desc_entry = tk.Entry(main_frame)
        desc_entry.pack(pady=5, fill="x")
        
        def process_withdrawal():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                if amount > account['balance']:
                    messagebox.showerror("Error", "Insufficient funds for this withdrawal")
                    return
                
                description = desc_entry.get() or "Withdrawal"
                
                # Update database
                cursor = self.connection.cursor()
                
                # Update account balance
                cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance - %s 
                    WHERE account_id = %s
                """, (amount, account['account_id']))
                
                # Record transaction
                cursor.execute("""
                    INSERT INTO transactions (account_id, transaction_type, amount, description)
                    VALUES (%s, 'Withdrawal', %s, %s)
                """, (account['account_id'], amount, description))
                
                self.connection.commit()
                
                messagebox.showinfo("Success", f"Withdrawal of Rs{amount:,.2f} processed successfully")
                withdraw_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive amount")
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to process withdrawal: {e}")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        withdraw_button = tk.Button(button_frame, text="Withdraw", command=process_withdrawal,
                                  bg=self.secondary_color, fg="white", font=self.button_font)
        withdraw_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=withdraw_window.destroy,
                                bg=self.accent_color, fg="white", font=self.button_font)
        cancel_button.pack(side="left", padx=10)
    
    def show_transfer_window(self, from_account):
        # Create a new window
        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Transfer Funds")
        transfer_window.geometry("500x400")
        transfer_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(transfer_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text=f"Transfer from {from_account['account_type']} Account", 
               font=self.title_font).pack(pady=10)
        
        # From account info
        tk.Label(main_frame, text=f"From Account: {from_account['account_number']}").pack(pady=5)
        tk.Label(main_frame, text=f"Current Balance: Rs{from_account['balance']:,.2f}").pack(pady=5)
        
        # To account entry
        tk.Label(main_frame, text="To Account Number:").pack(pady=10)
        to_account_entry = tk.Entry(main_frame, font=("Helvetica", 12))
        to_account_entry.pack(pady=5)
        
        # Amount entry
        tk.Label(main_frame, text="Transfer Amount:").pack(pady=10)
        amount_entry = tk.Entry(main_frame, font=("Helvetica", 14))
        amount_entry.pack(pady=5)
        
        # Description
        tk.Label(main_frame, text="Description (optional):").pack(pady=10)
        desc_entry = tk.Entry(main_frame)
        desc_entry.pack(pady=5, fill="x")
        
        def process_transfer():
            try:
                to_account_number = to_account_entry.get().strip()
                amount = float(amount_entry.get())
                
                if not to_account_number:
                    messagebox.showerror("Error", "Please enter the destination account number")
                    return
                
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                if amount > from_account['balance']:
                    messagebox.showerror("Error", "Insufficient funds for this transfer")
                    return
                
                description = desc_entry.get() or f"Transfer to {to_account_number}"
                
                # Check if destination account exists
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (to_account_number,))
                to_account = cursor.fetchone()
                
                if not to_account:
                    messagebox.showerror("Error", "Destination account not found")
                    return
                
                if to_account['account_id'] == from_account['account_id']:
                    messagebox.showerror("Error", "Cannot transfer to the same account")
                    return
                
                # Process transfer
                cursor = self.connection.cursor()
                
                # Update from account balance
                cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance - %s 
                    WHERE account_id = %s
                """, (amount, from_account['account_id']))
                
                # Update to account balance
                cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance + %s 
                    WHERE account_id = %s
                """, (amount, to_account['account_id']))
                
                # Record transaction for from account
                cursor.execute("""
                    INSERT INTO transactions (account_id, transaction_type, amount, description, related_account)
                    VALUES (%s, 'Transfer', %s, %s, %s)
                """, (from_account['account_id'], amount, description, to_account_number))
                
                # Record transaction for to account
                cursor.execute("""
                    INSERT INTO transactions (account_id, transaction_type, amount, description, related_account)
                    VALUES (%s, 'Transfer', %s, %s, %s)
                """, (to_account['account_id'], amount, f"Transfer from {from_account['account_number']}", from_account['account_number']))
                
                self.connection.commit()
                
                messagebox.showinfo("Success", 
                                  f"Transfer of Rs{amount:,.2f} to account {to_account_number} processed successfully")
                transfer_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive amount")
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to process transfer: {e}")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        transfer_button = tk.Button(button_frame, text="Transfer", command=process_transfer,
                                  bg=self.secondary_color, fg="white", font=self.button_font)
        transfer_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=transfer_window.destroy,
                                bg=self.accent_color, fg="white", font=self.button_font)
        cancel_button.pack(side="left", padx=10)
    
    def show_transaction_history(self):
        # Create a new window
        trans_window = tk.Toplevel(self.root)
        trans_window.title("Transaction History")
        trans_window.geometry("800x600")
        trans_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(trans_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Your Transaction History", font=self.title_font).pack(pady=10)
        
        # Date range frame
        date_frame = tk.Frame(main_frame)
        date_frame.pack(fill="x", pady=10)
        
        tk.Label(date_frame, text="From:").pack(side="left", padx=5)
        from_date_entry = tk.Entry(date_frame)
        from_date_entry.pack(side="left", padx=5)
        from_date_entry.insert(0, "YYYY-MM-DD")
        
        tk.Label(date_frame, text="To:").pack(side="left", padx=5)
        to_date_entry = tk.Entry(date_frame)
        to_date_entry.pack(side="left", padx=5)
        to_date_entry.insert(0, "YYYY-MM-DD")
        
        def load_transactions():
            from_date = from_date_entry.get()
            to_date = to_date_entry.get()
            
            try:
                cursor = self.connection.cursor(dictionary=True)
                
                query = """
                    SELECT t.transaction_id, t.transaction_type, t.amount, t.transaction_date, 
                           t.description, t.related_account, a.account_type
                    FROM transactions t
                    JOIN accounts a ON t.account_id = a.account_id
                    WHERE a.customer_id = %s
                """
                params = [self.current_user['customer_id']]
                
                if from_date != "YYYY-MM-DD" and to_date != "YYYY-MM-DD":
                    query += " AND t.transaction_date BETWEEN %s AND %s"
                    params.extend([from_date, to_date])
                elif from_date != "YYYY-MM-DD":
                    query += " AND t.transaction_date >= %s"
                    params.append(from_date)
                elif to_date != "YYYY-MM-DD":
                    query += " AND t.transaction_date <= %s"
                    params.append(to_date)
                
                query += " ORDER BY t.transaction_date DESC"
                
                cursor.execute(query, tuple(params))
                transactions = cursor.fetchall()
                
                # Clear existing items
                for item in trans_tree.get_children():
                    trans_tree.delete(item)
                
                # Add new items
                for trans in transactions:
                    amount = trans['amount']
                    if trans['transaction_type'] == 'Withdrawal' or \
                       (trans['transaction_type'] == 'Transfer' and not trans['related_account']):
                        amount = f"-Rs{amount:,.2f}"
                    else:
                        amount = f"Rs{amount:,.2f}"
                    
                    trans_tree.insert("", "end", values=(
                        trans['transaction_date'].strftime("%Y-%m-%d %H:%M:%S"),
                        trans['account_type'],
                        trans['transaction_type'],
                        amount,
                        trans['description'],
                        trans['related_account'] or ""
                    ))
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to fetch transactions: {e}")
        
        load_button = tk.Button(date_frame, text="Load", command=load_transactions,
                               bg=self.secondary_color, fg="white")
        load_button.pack(side="left", padx=10)
        
        # Transaction Treeview
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("Date", "Account", "Type", "Amount", "Description", "Related Account")
        trans_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            trans_tree.heading(col, text=col)
            trans_tree.column(col, width=120, anchor="w")
        
        trans_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=trans_tree.yview)
        scrollbar.pack(side="right", fill="y")
        trans_tree.configure(yscrollcommand=scrollbar.set)
        
        # Close button
        close_button = tk.Button(main_frame, text="Close", command=trans_window.destroy,
                               bg=self.accent_color, fg="white", font=self.button_font)
        close_button.pack(pady=10)
        
        # Load initial data
        load_transactions()
    
    def show_loan_information(self):
        # Create a new window
        loan_window = tk.Toplevel(self.root)
        loan_window.title("Loan Information")
        loan_window.geometry("800x600")
        loan_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(loan_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Your Loan Information", font=self.title_font).pack(pady=10)
        
        # Fetch loan information
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT l.*, a.account_number
                FROM loans l
                JOIN accounts a ON l.account_id = a.account_id
                WHERE l.customer_id = %s
                ORDER BY l.status, l.due_date
            """, (self.current_user['customer_id'],))
            loans = cursor.fetchall()
            
            if not loans:
                tk.Label(main_frame, text="You don't have any active loans").pack(pady=50)
                
                # Apply for new loan button
                apply_button = tk.Button(main_frame, text="Apply for New Loan", 
                                       command=self.show_loan_application,
                                       bg=self.secondary_color, fg="white", font=self.button_font)
                apply_button.pack(pady=20)
                
            else:
                # Notebook for multiple loans
                notebook = ttk.Notebook(main_frame)
                notebook.pack(fill="both", expand=True)
                
                for loan in loans:
                    # Create a tab for each loan
                    loan_frame = tk.Frame(notebook, padx=10, pady=10)
                    notebook.add(loan_frame, text=loan['loan_type'])
                    
                    # Loan details
                    details = [
                        ("Loan ID:", loan['loan_id']),
                        ("Account Number:", loan['account_number']),
                        ("Loan Amount:", f"Rs{loan['loan_amount']:,.2f}"),
                        ("Interest Rate:", f"{loan['interest_rate']}%"),
                        ("Term:", f"{loan['term_months']} months"),
                        ("Monthly Payment:", f"Rs{loan['monthly_payment']:,.2f}"),
                        ("Remaining Balance:", f"Rs{loan['remaining_balance']:,.2f}"),
                        ("Start Date:", loan['start_date'].strftime("%Y-%m-%d")),
                        ("Due Date:", loan['due_date'].strftime("%Y-%m-%d")),
                        ("Status:", loan['status'])
                    ]
                    
                    for i, (label, value) in enumerate(details):
                        tk.Label(loan_frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
                        tk.Label(loan_frame, text=value).grid(row=i, column=1, sticky="w", pady=2)
                    
                    # Make payment button if loan is active
                    if loan['status'] == "Active":
                        payment_button = tk.Button(loan_frame, text="Make Payment", 
                                                command=lambda l=loan: self.show_loan_payment(l),
                                                bg=self.secondary_color, fg="white")
                        payment_button.grid(row=len(details), column=0, columnspan=2, pady=10)
                
                # Apply for new loan button
                apply_frame = tk.Frame(main_frame)
                apply_frame.pack(fill="x", pady=10)
                
                apply_button = tk.Button(apply_frame, text="Apply for New Loan", 
                                       command=self.show_loan_application,
                                       bg=self.secondary_color, fg="white", font=self.button_font)
                apply_button.pack()
            
            # Close button
            close_button = tk.Button(main_frame, text="Close", command=loan_window.destroy,
                                   bg=self.accent_color, fg="white", font=self.button_font)
            close_button.pack(pady=10)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch loan information: {e}")
            loan_window.destroy()
    
    def show_loan_application(self):
        # Create a new window
        app_window = tk.Toplevel(self.root)
        app_window.title("Apply for Loan")
        app_window.geometry("600x500")
        app_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(app_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Apply for New Loan", font=self.title_font).pack(pady=10)
        
        # Fetch customer's accounts
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.account_id, a.account_number, a.account_type, a.balance
                FROM accounts a
                WHERE a.customer_id = %s AND a.status = 'Active'
            """, (self.current_user['customer_id'],))
            accounts = cursor.fetchall()
            
            if not accounts:
                messagebox.showerror("Error", "You need an active account to apply for a loan")
                app_window.destroy()
                return
            
            # Fetch available loan schemes
            cursor.execute("SELECT * FROM loan_schemes ORDER BY loan_type, scheme_name")
            schemes = cursor.fetchall()
            
            if not schemes:
                messagebox.showerror("Error", "No loan schemes available at this time")
                app_window.destroy()
                return
            
            # Form frame
            form_frame = tk.Frame(main_frame)
            form_frame.pack(fill="both", expand=True, pady=10)
            
            # Account selection
            tk.Label(form_frame, text="Select Account:").grid(row=0, column=0, sticky="w", pady=5)
            account_var = tk.StringVar()
            account_menu = ttk.OptionMenu(form_frame, account_var, "", *[
                f"{a['account_number']} ({a['account_type']})" for a in accounts
            ])
            account_menu.grid(row=0, column=1, sticky="ew", pady=5)
            account_var.set(f"{accounts[0]['account_number']} ({accounts[0]['account_type']})")
            
            # Loan scheme selection
            tk.Label(form_frame, text="Loan Type:").grid(row=1, column=0, sticky="w", pady=5)
            scheme_var = tk.StringVar()
            scheme_menu = ttk.OptionMenu(form_frame, scheme_var, "", *[
                f"{s['scheme_name']} ({s['loan_type']})" for s in schemes
            ])
            scheme_menu.grid(row=1, column=1, sticky="ew", pady=5)
            scheme_var.set(f"{schemes[0]['scheme_name']} ({schemes[0]['loan_type']})")
            
            # Loan amount
            tk.Label(form_frame, text="Loan Amount:").grid(row=2, column=0, sticky="w", pady=5)
            amount_entry = tk.Entry(form_frame)
            amount_entry.grid(row=2, column=1, sticky="ew", pady=5)
            
            # Loan term
            tk.Label(form_frame, text="Loan Term (months):").grid(row=3, column=0, sticky="w", pady=5)
            term_entry = tk.Entry(form_frame)
            term_entry.grid(row=3, column=1, sticky="ew", pady=5)
            
            # Purpose
            tk.Label(form_frame, text="Purpose:").grid(row=4, column=0, sticky="w", pady=5)
            purpose_entry = tk.Entry(form_frame)
            purpose_entry.grid(row=4, column=1, sticky="ew", pady=5)
            
            # Calculation results
            calc_frame = tk.LabelFrame(form_frame, text="Loan Calculation", padx=10, pady=10)
            calc_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
            
            tk.Label(calc_frame, text="Interest Rate:").grid(row=0, column=0, sticky="w")
            interest_label = tk.Label(calc_frame, text="N/A")
            interest_label.grid(row=0, column=1, sticky="e")
            
            tk.Label(calc_frame, text="Monthly Payment:").grid(row=1, column=0, sticky="w")
            payment_label = tk.Label(calc_frame, text="N/A")
            payment_label.grid(row=1, column=1, sticky="e")
            
            tk.Label(calc_frame, text="Total Interest:").grid(row=2, column=0, sticky="w")
            total_interest_label = tk.Label(calc_frame, text="N/A")
            total_interest_label.grid(row=2, column=1, sticky="e")
            
            tk.Label(calc_frame, text="Total Payment:").grid(row=3, column=0, sticky="w")
            total_payment_label = tk.Label(calc_frame, text="N/A")
            total_payment_label.grid(row=3, column=1, sticky="e")
            
            def calculate_loan():
                try:
                    scheme_name = scheme_var.get().split(" (")[0]
                    amount = float(amount_entry.get())
                    term = int(term_entry.get())
                    
                    # Get scheme details
                    cursor.execute("SELECT * FROM loan_schemes WHERE scheme_name = %s", (scheme_name,))
                    scheme = cursor.fetchone()
                    
                    if not scheme:
                        messagebox.showerror("Error", "Selected loan scheme not found")
                        return
                    
                    # Validate amount and term
                    if amount < scheme['min_amount'] or amount > scheme['max_amount']:
                        messagebox.showerror("Error", 
                                          f"Loan amount must be between Rs{scheme['min_amount']:,.2f} "
                                          f"and Rs{scheme['max_amount']:,.2f}")
                        return
                    
                    if term < scheme['min_term_months'] or term > scheme['max_term_months']:
                        messagebox.showerror("Error", 
                                          f"Loan term must be between {scheme['min_term_months']} "
                                          f"and {scheme['max_term_months']} months")
                        return
                    
                    # Calculate loan details
                    interest_rate = scheme['interest_rate'] / 100 / 12  # Monthly rate
                    monthly_payment = (amount * interest_rate * (1 + interest_rate)**term) / \
                                    ((1 + interest_rate)**term - 1)
                    total_payment = monthly_payment * term
                    total_interest = total_payment - amount
                    
                    # Update labels
                    interest_label.config(text=f"{scheme['interest_rate']}%")
                    payment_label.config(text=f"Rs{monthly_payment:,.2f}")
                    total_interest_label.config(text=f"Rs{total_interest:,.2f}")
                    total_payment_label.config(text=f"Rs{total_payment:,.2f}")
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers for amount and term")
            
            calculate_button = tk.Button(form_frame, text="Calculate", command=calculate_loan,
                                      bg=self.secondary_color, fg="white")
            calculate_button.grid(row=6, column=0, columnspan=2, pady=10)
            
            def submit_application():
                if interest_label.cget("text") == "N/A":
                    messagebox.showwarning("Calculation Required", "Please calculate loan first")
                    return
                
                account_number = account_var.get().split(" ")[0]
                scheme_name = scheme_var.get().split(" (")[0]
                amount = float(amount_entry.get())
                term = int(term_entry.get())
                purpose = purpose_entry.get() or "Not specified"
                
                try:
                    # Get account and scheme details
                    cursor.execute("SELECT account_id FROM accounts WHERE account_number = %s", (account_number,))
                    account = cursor.fetchone()
                    
                    cursor.execute("SELECT * FROM loan_schemes WHERE scheme_name = %s", (scheme_name,))
                    scheme = cursor.fetchone()
                    
                    # Calculate loan details
                    interest_rate = scheme['interest_rate'] / 100 / 12  # Monthly rate
                    monthly_payment = (amount * interest_rate * (1 + interest_rate)**term) / \
                                    ((1 + interest_rate)**term - 1)
                    
                    # Create loan record
                    today = datetime.now().date()
                    due_date = today.replace(year=today.year + term // 12, month=today.month + term % 12)
                    
                    cursor.execute("""
                        INSERT INTO loans (customer_id, account_id, loan_type, loan_amount, interest_rate, 
                                         term_months, monthly_payment, remaining_balance, 
                                         start_date, due_date, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        self.current_user['customer_id'],
                        account['account_id'],
                        scheme['loan_type'],
                        amount,
                        scheme['interest_rate'],
                        term,
                        monthly_payment,
                        amount,  # Initial remaining balance is full loan amount
                        today,
                        due_date,
                        "Pending"  # In a real system, this would go through approval process
                    ))
                    
                    self.connection.commit()
                    
                    messagebox.showinfo("Success", "Loan application submitted successfully!")
                    app_window.destroy()
                    
                except Error as e:
                    self.connection.rollback()
                    messagebox.showerror("Database Error", f"Failed to submit loan application: {e}")
            
            # Button frame
            button_frame = tk.Frame(main_frame)
            button_frame.pack(pady=10)
            
            submit_button = tk.Button(button_frame, text="Submit Application", command=submit_application,
                                    bg=self.secondary_color, fg="white", font=self.button_font)
            submit_button.pack(side="left", padx=10)
            
            cancel_button = tk.Button(button_frame, text="Cancel", command=app_window.destroy,
                                    bg=self.accent_color, fg="white", font=self.button_font)
            cancel_button.pack(side="left", padx=10)
            
            # Configure grid weights
            form_frame.grid_columnconfigure(1, weight=1)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load loan application form: {e}")
            app_window.destroy()
    
    def show_loan_payment(self, loan):
        # Create a new window
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Make Loan Payment")
        payment_window.geometry("500x400")
        payment_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(payment_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text=f"Make Payment for {loan['loan_type']} Loan", 
               font=self.title_font).pack(pady=10)
        
        # Loan info
        tk.Label(main_frame, text=f"Loan ID: {loan['loan_id']}").pack(pady=5)
        tk.Label(main_frame, text=f"Remaining Balance: Rs{loan['remaining_balance']:,.2f}").pack(pady=5)
        tk.Label(main_frame, text=f"Monthly Payment: Rs{loan['monthly_payment']:,.2f}").pack(pady=5)
        tk.Label(main_frame, text=f"Due Date: {loan['due_date'].strftime('%Y-%m-%d')}").pack(pady=5)
        
        # Payment amount
        tk.Label(main_frame, text="Payment Amount:").pack(pady=10)
        amount_entry = tk.Entry(main_frame, font=("Helvetica", 14))
        amount_entry.pack(pady=5)
        amount_entry.insert(0, str(loan['monthly_payment']))
        
        # From account selection
        tk.Label(main_frame, text="Pay From Account:").pack(pady=10)
        
        # Fetch customer's accounts
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.account_id, a.account_number, a.account_type, a.balance
                FROM accounts a
                WHERE a.customer_id = %s AND a.status = 'Active'
            """, (self.current_user['customer_id'],))
            accounts = cursor.fetchall()
            
            if not accounts:
                messagebox.showerror("Error", "No active accounts found for payment")
                payment_window.destroy()
                return
            
            account_var = tk.StringVar()
            account_menu = ttk.OptionMenu(main_frame, account_var, "", *[
                f"{a['account_number']} ({a['account_type']} - Rs{a['balance']:,.2f})" for a in accounts
            ])
            account_menu.pack(pady=5)
            account_var.set(f"{accounts[0]['account_number']} ({accounts[0]['account_type']} - Rs{accounts[0]['balance']:,.2f})")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch accounts: {e}")
            payment_window.destroy()
            return
        
        def process_payment():
            try:
                amount = float(amount_entry.get())
                account_number = account_var.get().split(" ")[0]
                
                if amount <= 0:
                    messagebox.showerror("Error", "Payment amount must be positive")
                    return
                
                if amount > loan['remaining_balance']:
                    amount = loan['remaining_balance']
                    messagebox.showinfo("Notice", f"Payment adjusted to remaining balance: Rs{amount:,.2f}")
                
                # Check if account has sufficient funds
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
                account = cursor.fetchone()
                
                if not account:
                    messagebox.showerror("Error", "Selected account not found")
                    return
                
                if amount > account['balance']:
                    messagebox.showerror("Error", "Insufficient funds in selected account")
                    return
                
                # Process payment
                cursor = self.connection.cursor()
                
                # Deduct from account
                cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance - %s 
                    WHERE account_number = %s
                """, (amount, account_number))
                
                # Update loan balance
                cursor.execute("""
                    UPDATE loans 
                    SET remaining_balance = remaining_balance - %s 
                    WHERE loan_id = %s
                """, (amount, loan['loan_id']))
                
                # If loan is fully paid, update status
                if amount >= loan['remaining_balance']:
                    cursor.execute("""
                        UPDATE loans 
                        SET remaining_balance = 0, status = 'Paid' 
                        WHERE loan_id = %s
                    """, (loan['loan_id'],))
                
                # Record transaction for account
                cursor.execute("""
                    INSERT INTO transactions (account_id, transaction_type, amount, description, related_account)
                    VALUES ((SELECT account_id FROM accounts WHERE account_number = %s), 
                            'Loan Payment', %s, 'Payment for loan %s', %s)
                """, (account_number, amount, loan['loan_id'], loan['account_number']))
                
                self.connection.commit()
                
                messagebox.showinfo("Success", f"Payment of Rs{amount:,.2f} processed successfully")
                payment_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid payment amount")
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to process payment: {e}")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        pay_button = tk.Button(button_frame, text="Make Payment", command=process_payment,
                             bg=self.secondary_color, fg="white", font=self.button_font)
        pay_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=payment_window.destroy,
                                bg=self.accent_color, fg="white", font=self.button_font)
        cancel_button.pack(side="left", padx=10)
    
    def show_card_information(self):
        # Create a new window
        card_window = tk.Toplevel(self.root)
        card_window.title("Card Information")
        card_window.geometry("600x400")
        card_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(card_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Your Card Information", font=self.title_font).pack(pady=10)
        
        # Fetch card information
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.*, a.account_number
                FROM cards c
                JOIN accounts a ON c.account_id = a.account_id
                WHERE c.customer_id = %s
                ORDER BY c.card_type, c.status
            """, (self.current_user['customer_id'],))
            cards = cursor.fetchall()
            
            if not cards:
                tk.Label(main_frame, text="You don't have any cards issued").pack(pady=50)
                
                # Request new card button
                request_button = tk.Button(main_frame, text="Request New Card", 
                                        command=self.show_card_request,
                                        bg=self.secondary_color, fg="white", font=self.button_font)
                request_button.pack(pady=20)
                
            else:
                # Notebook for multiple cards
                notebook = ttk.Notebook(main_frame)
                notebook.pack(fill="both", expand=True)
                
                for card in cards:
                    # Create a tab for each card
                    card_frame = tk.Frame(notebook, padx=10, pady=10)
                    notebook.add(card_frame, text=card['card_type'])
                    
                    # Card details
                    details = [
                        ("Card ID:", card['card_id']),
                        ("Account Number:", card['account_number']),
                        ("Card Number:", f"**** **** **** {card['card_number'][-4:]}" if card['card_number'] else "N/A"),
                        ("Expiry Date:", card['expiry_date'].strftime("%m/%Y") if card['expiry_date'] else "N/A"),
                        ("Issued Date:", card['issued_date'].strftime("%Y-%m-%d") if card['issued_date'] else "N/A"),
                        ("Status:", card['status'])
                    ]
                    
                    for i, (label, value) in enumerate(details):
                        tk.Label(card_frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
                        tk.Label(card_frame, text=value).grid(row=i, column=1, sticky="w", pady=2)
                    
                    # Card actions
                    actions_frame = tk.Frame(card_frame)
                    actions_frame.grid(row=len(details), column=0, columnspan=2, pady=10)
                    
                    if card['status'] == "Active":
                        block_button = tk.Button(actions_frame, text="Block Card", 
                                               command=lambda c=card: self.block_card(c),
                                               bg=self.accent_color, fg="white")
                        block_button.pack(side="left", padx=5)
                    
                    elif card['status'] == "Blocked":
                        activate_button = tk.Button(actions_frame, text="Activate Card", 
                                                 command=lambda c=card: self.activate_card(c),
                                                 bg=self.secondary_color, fg="white")
                        activate_button.pack(side="left", padx=5)
                
                # Request new card button
                request_frame = tk.Frame(main_frame)
                request_frame.pack(fill="x", pady=10)
                
                request_button = tk.Button(request_frame, text="Request New Card", 
                                         command=self.show_card_request,
                                         bg=self.secondary_color, fg="white", font=self.button_font)
                request_button.pack()
            
            # Close button
            close_button = tk.Button(main_frame, text="Close", command=card_window.destroy,
                                   bg=self.accent_color, fg="white", font=self.button_font)
            close_button.pack(pady=10)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch card information: {e}")
            card_window.destroy()
    
    def show_card_request(self):
        # Create a new window
        request_window = tk.Toplevel(self.root)
        request_window.title("Request New Card")
        request_window.geometry("500x400")
        request_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(request_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Request New Card", font=self.title_font).pack(pady=10)
        
        # Fetch customer's accounts
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.account_id, a.account_number, a.account_type
                FROM accounts a
                WHERE a.customer_id = %s AND a.status = 'Active'
            """, (self.current_user['customer_id'],))
            accounts = cursor.fetchall()
            
            if not accounts:
                messagebox.showerror("Error", "You need an active account to request a card")
                request_window.destroy()
                return
            
            # Form frame
            form_frame = tk.Frame(main_frame)
            form_frame.pack(fill="both", expand=True, pady=10)
            
            # Account selection
            tk.Label(form_frame, text="Select Account:").grid(row=0, column=0, sticky="w", pady=5)
            account_var = tk.StringVar()
            account_menu = ttk.OptionMenu(form_frame, account_var, "", *[
                f"{a['account_number']} ({a['account_type']})" for a in accounts
            ])
            account_menu.grid(row=0, column=1, sticky="ew", pady=5)
            account_var.set(f"{accounts[0]['account_number']} ({accounts[0]['account_type']})")
            
            # Card type selection
            tk.Label(form_frame, text="Card Type:").grid(row=1, column=0, sticky="w", pady=5)
            card_type_var = tk.StringVar(value="Debit")
            tk.Radiobutton(form_frame, text="Debit Card", variable=card_type_var, value="Debit").grid(row=1, column=1, sticky="w")
            tk.Radiobutton(form_frame, text="Credit Card", variable=card_type_var, value="Credit").grid(row=2, column=1, sticky="w")
            
            # Card delivery address
            tk.Label(form_frame, text="Delivery Address:").grid(row=3, column=0, sticky="w", pady=5)
            address_entry = tk.Entry(form_frame)
            address_entry.grid(row=3, column=1, sticky="ew", pady=5)
            
            # Get customer's address as default
            cursor.execute("SELECT address FROM customers WHERE customer_id = %s", (self.current_user['customer_id'],))
            customer = cursor.fetchone()
            if customer and customer['address']:
                address_entry.insert(0, customer['address'])
            
            def submit_request():
                account_number = account_var.get().split(" ")[0]
                card_type = card_type_var.get()
                delivery_address = address_entry.get()
                
                if not delivery_address:
                    messagebox.showerror("Error", "Please enter a delivery address")
                    return
                
                try:
                    # Get account ID
                    cursor.execute("SELECT account_id FROM accounts WHERE account_number = %s", (account_number,))
                    account = cursor.fetchone()
                    
                    if not account:
                        messagebox.showerror("Error", "Selected account not found")
                        return
                    
                    # Generate card number (in real system, this would be done by card processor)
                    card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
                    
                    # Generate expiry date (3 years from now)
                    today = datetime.now().date()
                    expiry_date = today.replace(year=today.year + 3)
                    
                    # Create card record
                    cursor.execute("""
                        INSERT INTO cards (customer_id, account_id, card_type, card_number, 
                                         expiry_date, issued_date, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        self.current_user['customer_id'],
                        account['account_id'],
                        card_type,
                        card_number,
                        expiry_date,
                        today,
                        "Pending"  # In real system, this would go through approval process
                    ))
                    
                    self.connection.commit()
                    
                    messagebox.showinfo("Success", "Card request submitted successfully!")
                    request_window.destroy()
                    
                except Error as e:
                    self.connection.rollback()
                    messagebox.showerror("Database Error", f"Failed to submit card request: {e}")
            
            # Button frame
            button_frame = tk.Frame(main_frame)
            button_frame.pack(pady=10)
            
            submit_button = tk.Button(button_frame, text="Submit Request", command=submit_request,
                                    bg=self.secondary_color, fg="white", font=self.button_font)
            submit_button.pack(side="left", padx=10)
            
            cancel_button = tk.Button(button_frame, text="Cancel", command=request_window.destroy,
                                    bg=self.accent_color, fg="white", font=self.button_font)
            cancel_button.pack(side="left", padx=10)
            
            # Configure grid weights
            form_frame.grid_columnconfigure(1, weight=1)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load card request form: {e}")
            request_window.destroy()
    
    def block_card(self, card):
        confirm = messagebox.askyesno("Confirm Block", 
                                    f"Are you sure you want to block card ending with {card['card_number'][-4:]}")
        
        if confirm:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE cards 
                    SET status = 'Blocked' 
                    WHERE card_id = %s
                """, (card['card_id'],))
                
                self.connection.commit()
                
                messagebox.showinfo("Success", "Card blocked successfully")
                
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to block card: {e}")
    
    def activate_card(self, card):
        confirm = messagebox.askyesno("Confirm Activation", 
                                    f"Are you sure you want to activate card ending with {card['card_number'][-4:]}")
        
        if confirm:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE cards 
                    SET status = 'Active' 
                    WHERE card_id = %s
                """, (card['card_id'],))
                
                self.connection.commit()
                
                messagebox.showinfo("Success", "Card activated successfully")
                
            except Error as e:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to activate card: {e}")
    
    def download_passbook(self):
        # Create a new window
        passbook_window = tk.Toplevel(self.root)
        passbook_window.title("Download E-Passbook")
        passbook_window.geometry("500x300")
        passbook_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(passbook_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Download E-Passbook", font=self.title_font).pack(pady=10)
        
        # Date range
        date_frame = tk.Frame(main_frame)
        date_frame.pack(fill="x", pady=10)
        
        tk.Label(date_frame, text="From:").pack(side="left", padx=5)
        from_date_entry = tk.Entry(date_frame)
        from_date_entry.pack(side="left", padx=5)
        from_date_entry.insert(0, "YYYY-MM-DD")
        
        tk.Label(date_frame, text="To:").pack(side="left", padx=5)
        to_date_entry = tk.Entry(date_frame)
        to_date_entry.pack(side="left", padx=5)
        to_date_entry.insert(0, "YYYY-MM-DD")
        
        # Format selection
        format_frame = tk.Frame(main_frame)
        format_frame.pack(fill="x", pady=10)
        
        tk.Label(format_frame, text="Format:").pack(side="left", padx=5)
        format_var = tk.StringVar(value="pdf")
        tk.Radiobutton(format_frame, text="PDF", variable=format_var, value="pdf").pack(side="left", padx=5)
        tk.Radiobutton(format_frame, text="CSV", variable=format_var, value="csv").pack(side="left", padx=5)
        tk.Radiobutton(format_frame, text="Text", variable=format_var, value="txt").pack(side="left", padx=5)
        
        def generate_passbook():
            from_date = from_date_entry.get()
            to_date = to_date_entry.get()
            file_format = format_var.get()
            
            if from_date == "YYYY-MM-DD" or to_date == "YYYY-MM-DD":
                messagebox.showwarning("Date Required", "Please specify a date range")
                return
            
            try:
                cursor = self.connection.cursor(dictionary=True)
                
                # Get all accounts for the customer
                cursor.execute("""
                    SELECT a.account_id, a.account_number, a.account_type
                    FROM accounts a
                    WHERE a.customer_id = %s
                """, (self.current_user['customer_id'],))
                accounts = cursor.fetchall()
                
                if not accounts:
                    messagebox.showinfo("No Accounts", "You don't have any accounts")
                    return
                
                # Get transactions for each account
                all_transactions = []
                for account in accounts:
                    cursor.execute("""
                        SELECT t.transaction_date, t.transaction_type, t.amount, 
                               t.description, t.related_account
                        FROM transactions t
                        WHERE t.account_id = %s
                        AND t.transaction_date BETWEEN %s AND %s
                        ORDER BY t.transaction_date DESC
                    """, (account['account_id'], from_date, to_date))
                    transactions = cursor.fetchall()
                    
                    for trans in transactions:
                        all_transactions.append({
                            'account': f"{account['account_number']} ({account['account_type']})",
                            'date': trans['transaction_date'],
                            'type': trans['transaction_type'],
                            'amount': trans['amount'],
                            'description': trans['description'],
                            'related_account': trans['related_account'] or ""
                        })
                
                if not all_transactions:
                    messagebox.showinfo("No Transactions", "No transactions found in the selected date range")
                    return
                
                # Sort all transactions by date
                all_transactions.sort(key=lambda x: x['date'], reverse=True)
                
                # Prepare data for export
                headers = ["Date", "Account", "Type", "Amount", "Description", "Related Account"]
                data = []
                
                for trans in all_transactions:
                    amount = trans['amount']
                    if trans['type'] == 'Withdrawal' or \
                       (trans['type'] == 'Transfer' and not trans['related_account']):
                        amount = f"-{amount:,.2f}"
                    else:
                        amount = f"{amount:,.2f}"
                    
                    data.append([
                        trans['date'].strftime("%Y-%m-%d %H:%M:%S"),
                        trans['account'],
                        trans['type'],
                        amount,
                        trans['description'],
                        trans['related_account']
                    ])
                
                # Generate file based on selected format
                if file_format == "pdf":
                    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                           filetypes=[("PDF Files", "*.pdf")],
                                                           title="Save E-Passbook As",
                                                           initialfile=f"passbook_{from_date}_to_{to_date}.pdf")
                    
                    if file_path:
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 16)
                        pdf.cell(0, 10, f"E-Passbook ({from_date} to {to_date})", 0, 1, "C")
                        pdf.ln(10)
                        
                        pdf.set_font("Arial", "B", 12)
                        col_widths = [30, 40, 20, 20, 50, 30]  # Fixed widths for columns
                        
                        # Create header
                        pdf.set_fill_color(200, 220, 255)
                        for i, header in enumerate(headers):
                            pdf.cell(col_widths[i], 10, header, 1, 0, "C", 1)
                        pdf.ln()
                        
                        # Add data
                        pdf.set_font("Arial", "", 10)
                        fill = False
                        for row in data:
                            for i, item in enumerate(row):
                                pdf.cell(col_widths[i], 10, str(item), 1, 0, "L", fill)
                            pdf.ln()
                            fill = not fill
                        
                        pdf.output(file_path)
                        messagebox.showinfo("Success", f"E-Passbook saved to:\n{file_path}")
                
                elif file_format == "csv":
                    file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                           filetypes=[("CSV Files", "*.csv")],
                                                           title="Save E-Passbook As",
                                                           initialfile=f"passbook_{from_date}_to_{to_date}.csv")
                    
                    if file_path:
                        try:
                            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                                # Write header
                                csvfile.write(",".join(headers) + "\n")
                                
                                # Write data
                                for row in data:
                                    csvfile.write(",".join(str(item) for item in row) + "\n")
                            
                            messagebox.showinfo("Success", f"E-Passbook saved to:\n{file_path}")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to save CSV file: {e}")
                
                else:  # Text format
                    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                           filetypes=[("Text Files", "*.txt")],
                                                           title="Save E-Passbook As",
                                                           initialfile=f"passbook_{from_date}_to_{to_date}.txt")
                    
                    if file_path:
                        try:
                            with open(file_path, "w", encoding="utf-8") as txtfile:
                                # Write header
                                txtfile.write(f"E-Passbook ({from_date} to {to_date})\n\n")
                                txtfile.write("\t".join(headers) + "\n")
                                txtfile.write("-" * (sum(len(h) for h in headers) + len(headers) * 4) + "\n")
                                
                                # Write data
                                for row in data:
                                    txtfile.write("\t".join(str(item) for item in row) + "\n")
                            
                            messagebox.showinfo("Success", f"E-Passbook saved to:\n{file_path}")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to save text file: {e}")
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to generate passbook: {e}")
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        generate_button = tk.Button(button_frame, text="Generate Passbook", command=generate_passbook,
                                  bg=self.secondary_color, fg="white", font=self.button_font)
        generate_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=passbook_window.destroy,
                                bg=self.accent_color, fg="white", font=self.button_font)
        cancel_button.pack(side="left", padx=10)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystem(root)
    root.mainloop()
