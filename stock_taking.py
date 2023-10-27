from database import Database


class StockTaking:
    def __init__(self):
        """Retrieve a list of products from the database"""
        database = Database()
        self.product_list = database.get_catalogue()
        database.close_database()

    def record_products(self, save_location):
        """Writes all products to a file"""
        if save_location == "":
            return
        with open(save_location, "w") as writer:
            for product in self.product_list:  # Write each product on their own line
                writer.write(f"ID: {product.product_id}, NAME: {product.name}, PRICE: {product.price}, "
                             f"STOCK: {product.stock}\n")

    def stock_alert(self):
        """Returns a list of products low in stock"""
        low_stock_products = []
        for product in self.product_list:
            if product.stock < 20:  # Add products will less than 20 in stock to the list
                low_stock_products.append(product)
        return low_stock_products


def record_stock_alert(low_stock_products, save_location):
    """Write products low in stock a file"""
    if save_location == "":
        return
    with open(save_location, "w") as writer:
        for product in low_stock_products:  # Write each product low on stock on their own line
            writer.write(f"ID: {product.product_id}, NAME: {product.name}, PRICE: {product.price}, "
                         f"STOCK: {product.stock}\n")
