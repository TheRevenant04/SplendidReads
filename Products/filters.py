class Filters:
    """
    A class used to model product filters.

    Attributes
    ----------
    lowest_price_first : str
        Represents a price filter option.
    highest_price_first : str
        Represents a price filter option.
    bestsellers : str
        Represents the best selling products filter option.
    latest : str
        Represents the latest products filter option.
    top_rated : str
        Represents the top rated products filter option.
    FILTER_CHOICES : list
        Contains tuples of model representation and user representation.

    Methods
    -------
    get_filter_model_value(self)
        A method that returns a dictionary of filter choices.
    get_product_filters(self)
        A method that returns a tuple of filter choices.
    """
    lowest_price_first = 'l2h'
    highest_price_first = 'h2l'
    bestsellers = 'bestsellers'
    latest = 'latest'
    top_rated = 'top_rated'

    FILTER_CHOICES = [
          (None,'Choose a filter'),
          (lowest_price_first, 'Price - Low to High'),
          (highest_price_first, 'Price - High to Low'),
          (bestsellers, 'Bestsellers'),
          (latest, 'Latest'),
          (top_rated, 'Top Rated')
    ]

    def get_filter_model_value(self):
        """
        Returns
        -------
            A dictionary of filter choices.
        """
        return {'low2high':self.lowest_price_first, 'high2low':self.highest_price_first, 'bestsellers':self.bestsellers, 'latest':self.latest, 'top_rated':self.top_rated}

    def get_product_filters(self):
        """
        Returns
        -------
            A tuple of filter choices.
        """
        return self.FILTER_CHOICES
