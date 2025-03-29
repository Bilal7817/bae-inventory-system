import unittest
import os
import sqlite3
from tempfile import NamedTemporaryFile

# Import your database manager class
from main import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.temp_db = NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        # Delete the temporary database file
        os.unlink(self.temp_db.name)
    
    def test_add_item(self):
        # Test adding an item
        item_id = self.db_manager.add_item("Test Item", "Test Category", 10, 5.99)
        self.assertIsNotNone(item_id)
        
        # Verify the item was added correctly
        item = self.db_manager.get_item_by_id(item_id)
        self.assertEqual(item[1], "Test Item")
        self.assertEqual(item[2], "Test Category")
        self.assertEqual(item[3], 10)
        self.assertEqual(item[4], 5.99)
    
    def test_update_item(self):
        # Add an item first
        item_id = self.db_manager.add_item("Original Item", "Original Category", 5, 9.99)
        
        # Update the item
        result = self.db_manager.update_item(item_id, "Updated Item", "Updated Category", 8, 19.99)
        self.assertTrue(result)
        
        # Verify the update worked
        item = self.db_manager.get_item_by_id(item_id)
        self.assertEqual(item[1], "Updated Item")
        self.assertEqual(item[2], "Updated Category")
        self.assertEqual(item[3], 8)
        self.assertEqual(item[4], 19.99)
    
    def test_delete_item(self):
        # Add an item first
        item_id = self.db_manager.add_item("Item to Delete", "Test Category", 3, 4.99)
        
        # Delete the item
        result = self.db_manager.delete_item(item_id)
        self.assertTrue(result)
        
        # Verify it was deleted
        item = self.db_manager.get_item_by_id(item_id)
        self.assertIsNone(item)
    
    def test_search_items(self):
        # Add some test items
        self.db_manager.add_item("Laptop", "Electronics", 5, 899.99)
        self.db_manager.add_item("Desktop", "Electronics", 3, 1299.99)
        self.db_manager.add_item("Pencil", "Office Supplies", 100, 0.99)
        
        # Search for electronics
        results = self.db_manager.search_items("electron")
        self.assertEqual(len(results), 2)
        
        # Search for Office items
        results = self.db_manager.search_items("office")
        self.assertEqual(len(results), 1)
        
        # Search for a specific item
        results = self.db_manager.search_items("laptop")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Laptop")

if __name__ == "__main__":
    unittest.main()