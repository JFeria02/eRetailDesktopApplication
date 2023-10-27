class Review:
    def __init__(self, review_id, product_id, customer_id, rating, review_text):
        """Sets review details"""
        self._review_id = review_id
        self._product_id = product_id
        self._customer_id = customer_id
        self._rating = rating
        self._review_text = review_text

    # Getters and setters

    # Review ID
    @property
    def review_id(self):
        return self._review_id

    # Product ID
    @property
    def product_id(self):
        return self._product_id

    # Customer ID
    @property
    def customer_id(self):
        return self._customer_id

    # Rating
    @property
    def rating(self):
        return self._rating

    # Review Text
    @property
    def review_text(self):
        return self._review_text
