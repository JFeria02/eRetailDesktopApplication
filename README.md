# e-Retail desktop application project

Application for a e-retail system developed using Python 3.8 and SQL
• Created GUIs for administrators and customers that displayed product data retrieved from the
database.
• A SQL database stores data on all products in the system and can be updated by administrators
through the GUI. Customers can search products in the system using keywords or product
categories

## Features
### Administration Features
1. Login with a User ID and password
   -  Check if the entered credentials are correct
   -  Prompt the user with an error message if the User ID does not exist or the User ID and password do not match
2. Maintain a list of product categories
   -  Add a category
     *  Can enter a category ID and name to be added to the database
     *  Prompt the user if the category already exists or if the category ID is already in use
   -  Edit a category
     *  Can select a category, edit its name and update the database
   -  Delete a category
     *  Can select a category and delete it from the database
3. Maintain products
   -  Add a new product
   -  Edit a product
   -  Delete a product
4. Perform stock taking

### Customer Features
1. Browse the product catalogue
   - Display a list of all available products, showing the product name, image and price
   - Display "Out of Stock" for products with no stock and display "Low Stock" for products with less that 20 items in stock
2. Search for a product or category
   - Can enter a search keyword and display all products that match the keyword
   - Can select a product category and display all products within the selected category
3. View a product description/specification
   - Can select a product from the list of producs given by the catalogue or search
   - Displays the product description and full details
   - Displays a button to add the product to the shopping basket
   - Displays a button to display the reviews of the product
4. View and write a product review
   - Displays all existing product reviews
   - Allows the user to write a new review, which will be stored in the database

### Order Processing
1. Shopping basket
   -  Add produts to the shopping basket
   -  Update the shopping basket
     *  Can remove products
     *  Can change the quantity of the product in the shopping basket
     *  Total price is displayed

## Video

https://github.com/JFeria02/eRetailDesktopApplication/assets/78926685/ea41b9d1-f0ba-4977-a748-80941c1f43f9


### Usernames and passwords:
#### ADMINS:
**UserID:** 1  | **Password:** pass1

#### CUSTOMERS:
**UserID:** 2  | **Password:** pass2

**UserID:** 3  | **Password:** pass3

**UserID:** 4  | **Password:** pass4
