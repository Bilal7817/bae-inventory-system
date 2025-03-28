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
        
        # The database connection
        self.db = DatabaseManager()
    
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