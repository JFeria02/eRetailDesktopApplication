import io
import sqlite3
from sqlite3 import Error
import PIL

from category import Category
from product import Product
from review import Review


class Database:
    def __init__(self):
        """Opens the database and sets the cursor"""
        try:
            self.connection = sqlite3.connect("SystemDatabase.db")
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)

    def verify_login(self, username, password):
        """Checks login details"""
        rows = self.cursor.execute("SELECT UserID, Password, Type FROM users").fetchall()
        for row in rows:
            if username in row and password in row:
                return True, row[2]
        return False, False

    def get_catalogue(self):
        """Returns a list of all of the products in the database"""
        rows = self.cursor.execute("SELECT ProductID, ProductName, ProductPrice, ProductStock, ProductDescription,"
                                   "ProductDetails, ProductImage, ProductCategory, LocationID FROM products")
        product_list = []
        for row in rows:
            product_id = row[0]
            product_name = row[1]
            product_price = row[2]
            product_stock = row[3]
            product_description = row[4]
            product_details = row[5]
            product_image = row[6]
            try:
                image_file = io.BytesIO(product_image)
            except TypeError:
                image_file = product_image
            product_category = row[7]
            warehouse_location = row[8]
            product = Product(product_id, product_name, product_price, product_stock, product_description,
                              product_details, image_file, product_category, warehouse_location)
            product_list.append(product)

        return product_list

    def get_categories(self):
        """Returns a list of all of the categories in the database"""
        rows = self.cursor.execute("SELECT CategoryID, CategoryName FROM categories")

        category_list = []
        for row in rows:
            category_id = row[0]
            category_name = row[1]
            category = Category(category_id, category_name)
            category_list.append(category)

        return category_list

    def open_image(self, path):
        """Returns image data from an image at the given path"""
        with open(path, "rb") as reader:
            image_data = reader.read()
        return image_data

    def create_product(self, product_id, name, price, stock, description, details, image, category, warehouse_location):
        """Adds a new product record to the database"""
        image = self.open_image(image)
        self.cursor.execute("INSERT INTO products (ProductID, ProductName, ProductPrice, ProductStock, "
                            "ProductDescription, ProductDetails, ProductImage, ProductCategory, LocationID)"
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(product_id), str(name), float(price),
                                                                   int(stock), str(description), str(details), image,
                                                                   int(category), int(warehouse_location)))
        self.connection.commit()

    def update_product(self, product_id, name, price, stock, description, details, image, category, warehouse_location):
        """Updates a product record in the database"""
        if type(image) == io.BytesIO:
            self.cursor.execute("UPDATE products SET ProductName = ?, ProductPrice = ?, ProductStock = ?,"
                                "ProductDescription = ?, ProductDetails = ?, ProductCategory = ?,"
                                "LocationID = ? WHERE ProductID = ?", (str(name), float(price), int(stock),
                                                                       str(description), str(details),
                                                                       int(category), int(warehouse_location),
                                                                       int(product_id)))
            self.connection.commit()
        else:
            self.cursor.execute("UPDATE products SET ProductName = ?, ProductPrice = ?, ProductStock = ?,"
                                "ProductDescription = ?, ProductDetails = ?, ProductImage = ?, ProductCategory = ?,"
                                "LocationID = ? WHERE ProductID = ?", (str(name), float(price), int(stock),
                                                                       str(description), str(details), image,
                                                                       int(category), int(warehouse_location),
                                                                       int(product_id)))
            self.connection.commit()

    def delete_product(self, product_id):
        """Deletes the given product from the database"""
        self.cursor.execute(f"DELETE FROM products WHERE ProductID = {int(product_id)}")
        self.connection.commit()

    def create_category(self, category_id, category_name):
        """Adds a new category record to the database"""
        print(category_id)
        print(category_name)
        self.cursor.execute(f"INSERT INTO categories VALUES ({int(category_id)}, '{category_name}')")
        self.connection.commit()

    def update_category(self, category_id, new_name):
        """Updates a category record in the database"""
        self.cursor.execute(f"UPDATE categories SET CategoryName = '{new_name}' WHERE CategoryID = {int(category_id)}")
        self.connection.commit()

    def delete_category(self, category_id):
        """Deletes the given cateogry from the database"""
        self.cursor.execute(f"DELETE FROM categories WHERE CategoryID = {int(category_id)}")
        self.connection.commit()

    def get_product_reviews(self, product_id):
        """Returns a list of all of the reviews for the given product"""
        rows = self.cursor.execute(f"SELECT ReviewID, CustomerID, Rating, ReviewText FROM reviews WHERE "
                                   f"ProductID = '{int(product_id)}'")

        review_list = []
        for row in rows:
            review_id = row[0]
            customer_id = row[1]
            rating = row[2]
            review_text = row[3]
            review = Review(review_id, product_id, customer_id, rating, review_text)
            review_list.append(review)

        return review_list

    def write_product_review(self, product_id, customer_id, rating, review_text):
        """Adds a review record to the database"""
        self.cursor.execute(f"INSERT INTO reviews (ProductID, CustomerID, Rating, ReviewText) VALUES (?, ?, ?, ?)",
                            (int(product_id), int(customer_id), int(rating), review_text))
        self.connection.commit()

    def close_database(self):
        """Closes the cursor and connection to the database"""
        self.cursor.close()
        self.connection.close()
        del self
