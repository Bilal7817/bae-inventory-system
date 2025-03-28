import tkinter as tk
from tkinter import ttk
import sqlite3
import csv
from PIL import Image, ImageT

class DatabaseManager:
    def __init__(self, db_file="inventory.db"):
        """Initialize database connection and create tables """
        self.db_file = db_file
        self.create_tables()
    
    def create_tables(self):
        """Create necessary tables """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create inventory table
            cursor.execute('''
                CREATE TABLE for inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    price REAL NOT NULL DEFAULT 0.0
                )
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def add_item(self, name, category, quantity, price):
        """Add a new item to the inventory"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO inventory (name, category, quantity, price) VALUES (?, ?, ?, ?)",
                (name, category, quantity, price)
            )
            
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_all_items(self):
        """Retrieve all inventory items"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM inventory ORDER BY name")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_item_by_id(self, item_id):
        """Retrieve an item by its ID"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM inventory WHERE id = ?", (item_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def update_item(self, item_id, name, category, quantity, price):
        """Update an existing item"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE inventory SET name = ?, category = ?, quantity = ?, price = ? WHERE id = ?",
                (name, category, quantity, price, item_id)
            )
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def delete_item(self, item_id):
        """Delete an item from the inventory"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def search_items(self, search_term):
        """Search for items by name or category"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            search_pattern = f"%{search_term}%"
            cursor.execute(
                "SELECT * FROM inventory WHERE name LIKE ? OR category LIKE ? ORDER BY name",
                (search_pattern, search_pattern)
            )
            
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def export_to_csv(self, filename):
        """Export inventory data to a CSV file"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM inventory ORDER BY name")
            items = cursor.fetchall()
            
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                # header
                writer.writerow(["ID", "Name", "Category", "Quantity", "Price"])
                # data
                writer.writerows(items)
            
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def import_from_csv(self, filename):
        """Import inventory data from a CSV file"""
        conn = None
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                # Skip header
                next(reader)
                
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                
                for row in reader:
                    if len(row) >= 4:  
                        name = row[1]
                        category = row[2]
                        quantity = int(row[3])
                        price = float(row[4])
                        
                        cursor.execute(
                            "INSERT INTO inventory (name, category, quantity, price) VALUES (?, ?, ?, ?)",
                            (name, category, quantity, price)
                        )
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Import error: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    print("Database Manager initialized")
    db = DatabaseManager()
    print("Database and tables created successfully")

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BAE Systems - Inventory Management")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set up the main frames
        self.setup_frames()

       # Create the inventory view
        self.create_inventory_view()
        
        # The database connection
        self.db = DatabaseManager()

        # Load intial inventory  
        self.load_inventory()

    def setup_frames(self):
        # header frame with BAE Systems branding
        self.header_frame = tk.Frame(self.root, bg="#C8102E")  
        self.header_frame.pack(fill=tk.X)
        
        # Application title
        title_label = tk.Label(
            self.header_frame, 
            text="Inventory Management System",
            font=("Arial", 16, "bold"),
            bg="#C8102E",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # The main content frame
        self.content_frame = ttk.Frame(self.root, padding=10)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root, 
            text="Ready", 
            relief=tk.SUNKEN, 
            anchor=tk.W, 
            padding=(5, 2)
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

    def create_inventory_view(self):
        # Frame for search
        search_frame = ttk.Frame(self.content_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Add search button
        ttk.Button(
            search_frame, 
            text="Search",
            command=self.search_inventory
        ).pack(side=tk.LEFT, padx=5)

        # Add clear button
        ttk.Button(
            search_frame, 
            text="Clear",
            command=self.clear_search
        ).pack(side=tk.LEFT, padx=5)
        
        # Create treeview for inventory display
        self.tree_frame = ttk.Frame(self.content_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.inventory_tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "name", "category", "quantity", "price", "total_value"),
            show="headings"
        )
        
        # Define columns
        self.inventory_tree.heading("id", text="ID")
        self.inventory_tree.heading("name", text="Item Name")
        self.inventory_tree.heading("category", text="Category")
        self.inventory_tree.heading("quantity", text="Quantity")
        self.inventory_tree.heading("price", text="Unit Price (£)")
        self.inventory_tree.heading("total_value", text="Total Value (£)")
        
        # Set column widths
        self.inventory_tree.column("id", width=50)
        self.inventory_tree.column("name", width=200)
        self.inventory_tree.column("category", width=150)
        self.inventory_tree.column("quantity", width=100)
        self.inventory_tree.column("price", width=100)
        self.inventory_tree.column("total_value", width=120)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=y_scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.inventory_tree.xview)
        self.inventory_tree.configure(xscrollcommand=x_scrollbar.set)
        
        # Place treeview and scrollbars
        self.inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def search_inventory(self):
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.load_inventory()
            return
    
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Get search results
        items = self.db.search_items(search_term)
        
        # Insert items into treeview
        for item in items:
            total_value = float(item[3]) * float(item[4])
            self.inventory_tree.insert(
                "",
                tk.END,
                values=(item[0], item[1], item[2], item[3], f"£{item[4]:.2f}", f"£{total_value:.2f}")
            )
        
        self.status_bar.config(text=f"Found {len(items)} items")

    def clear_search(self):
        self.search_var.set("")
        self.load_inventory()
    
    def load_inventory(self):
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
    
        items = self.db.get_all_items()
        
        # Insert items into treeview
        for item in items:
            total_value = float(item[3]) * float(item[4])
            self.inventory_tree.insert(
                "",
                tk.END,
                values=(item[0], item[1], item[2], item[3], f"£{item[4]:.2f}", f"£{total_value:.2f}")
            )
        
        self.status_bar.config(text=f"Loaded {len(items)} items")