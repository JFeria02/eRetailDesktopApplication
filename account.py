from database import Database


class Account:
    def __init__(self, username, password):
        """Sets the accounts username, password and basket"""
        self.username = username
        self.password = password
        self.basket = {}

    def get_basket(self):
        """Returns the basket list"""
        return self.basket

    def add_to_basket(self, product, quantity):
        """Adds an item to the basket"""
        if product.product_id not in self.basket:
            self.basket[product.product_id] = product, quantity  # Add product to basket
        else:
            for item in self.basket:
                if self.basket[item][0].product_id == product.product_id:
                    new_quantity = int(self.basket[item][1]) + 1
                    updated_entry = {item: (product, new_quantity)}
                    self.basket.update(updated_entry)

    def set_quantity(self, product, quantity):
        """Sets the quantity of a item in the basket"""
        updated_entry = {product: (self.basket[product][0], quantity)}
        self.basket.update(updated_entry)
        print(self.basket[product])

    def remove_from_basket(self, product_id):
        """Removes an item from the basket"""
        self.basket.pop(product_id)

    def total_cost(self):
        """Calculates the total cost of all of the items in the basket"""
        total_cost = 0
        for item in self.basket:
            item_cost = float(self.basket[item][0].price)
            item_quantity = int(self.basket[item][1])
            item_total_cost = item_cost * item_quantity
            total_cost += item_total_cost
        return total_cost

    def get_user_id(self):
        """Returns the username/UserID"""
        return self.username


def login_check(username, password):
    """Checks login details"""
    database = Database()
    verified, user_type = database.verify_login(username, password)
    if verified and (user_type == "CUSTOMER" or user_type == "ADMIN"):
        database.close_database()
        del database
        return True, user_type
    else:
        return False, "NONE"
