
class Search:
    def __init__(self, product_list, category_list, search_term, category_filter):
        """Searches a product list for items that meet search criteria"""
        self.product_list = product_list
        self.category_list = category_list
        self.search_term = search_term
        self.category_filter = category_filter

        self.result = self.search()

    def search(self):
        """Returns a list of products that match the search term and category"""
        if self.category_filter == "None":  # If there is no category filter, search all products
            product_list = self.product_list
        else:  # If there is a category filter, only search items that are in that category
            product_list = self.category_search(self.category_filter)

        matching_items = []
        for item in product_list:
            if self.search_term.lower() in item.name.lower():  # If the search term is found in the product name
                matching_items.append(item)
        return matching_items

    def category_search(self, category_selected):
        """Returns a list of products that are in the selected category"""
        for category in self.category_list:
            if category.name == category_selected:
                category_selected = category.category_id
                break

        category_items = []
        for item in self.product_list:
            if item.category == category_selected:
                category_items.append(item)  # Add products to list that are part of the category
        return category_items
