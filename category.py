
class Category:
    def __init__(self, category_id, name):
        """Sets category id and name"""
        self._category_id = category_id
        self._name = name

    # Getters and Setters

    # category_id
    @property
    def category_id(self):
        return self._category_id

    # name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self.name = name
