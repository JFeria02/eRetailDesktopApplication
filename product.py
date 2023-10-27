class Product:

    def __init__(self, product_id, name, price, stock, description, details, image, category, location):
        """Sets products details"""
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock
        self._description = description
        self._details = details
        self._image = image
        self._category = category
        self._location = location

    # Getters and Setters

    # id
    @property
    def product_id(self):
        return self._product_id

    # name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    # price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    # stock
    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock):
        self._stock = stock

    # description
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    # details
    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, details):
        self._details = details

    # image
    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image

    # category
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    # location in the warehouse
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location
