# BAE Systems Inventory Management System

An inventory management application developed for BAE Systems to track inventory items, quantities, and values.

## Features

- Add, edit, and delete inventory items
- Search inventory by name or category
- Calculate total inventory value
- Export inventory data to CSV
- Import inventory data from CSV
- Data persistence using SQLite database
- Modern user interface with BAE Systems branding

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)
- SQLite3 (included with Python)
- Pillow library for image handling

## Installation

1. Clone the repository:
git clone https://github.com/Bilal7817/bae-inventory-system.git
cd bae-inventory-system

2. Create a virtual environment 
python -m venv venv
source venv/bin/activate  venv\Scripts\activate

3. Install required packages:
pip install -r requirements.txt

4. Run the application:

python main.py
## Usage

### Adding Items

1. Click the "Add Item" button
2. Enter item details in the dialog:
- Item name
- Category
- Quantity
- Unit price
3. Click "Save"

### Editing Items

1. Select an item from the list
2. Click the "Edit Item" button
3. Modify the details
4. Click "Save"

### Deleting Items

1. Select an item from the list
2. Click the "Delete Item" button
3. Confirm deletion

### Searching

1. Enter a search term in the search box
2. Click "Search"
3. Click "Clear" to return to the full inventory

### Importing/Exporting

- Click "Export CSV" to save the current inventory to a CSV file
- Click "Import CSV" to load inventory data from a CSV file

## Project Structure

- `main.py`: Main application file containing:
- `DatabaseManager`: Handles database operations
- `InventoryApp`: Main GUI application
- `ItemDialog`: Dialog for adding/editing items

- `test_inventory.py`: Unit tests for database operations

## Testing

To run the unit tests:
python -m unittest test_inventory.py
## Development

This project follows these software development practices:

- **Modular Design**: Separation of concerns between UI, business logic, and data access
- **Error Handling**: Robust error handling for database operations and user input
- **Version Control**: Git for tracking changes and feature branches
- **Testing**: Unit tests to ensure database operations work correctly

## Future Improvements

- User authentication
- Multiple inventory categories
- Advanced reporting
- Data visualization
- Support for barcode scanning