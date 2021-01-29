from django.conf import settings
from django.db import models
from django.utils import timezone

class Product(models.Model):
    """
    A class that extends Django's Model class.
    It is used to model a product.

    Attributes
    ----------
    SKU : str
        Represents the stock keeping unit of a product.
    Title : str
        Represents the title of the product.
    Author : str
        Represents the author's name of the product.
    Genre : str
        Represents the category of the product.
    Price : int
        Represents the price of the product.
    Image_URL : str
        Represents the url of the product image.

    Methods
    -------
    str(self)
        Returns the string value of a Product.
    """
    SKU = models.CharField(max_length=100, primary_key=True)
    Title = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)
    Genre = models.CharField(max_length=100)
    Price = models.IntegerField()
    Image_URL = models.URLField(unique=True)

    def __str__(self):
        """
        Returns
        -------
        The Title of the product.
        """
        return self.Title

class ProductReviews(models.Model):
    """
    A class that extends Django's Model class.
    It is used to model a product's reviews.

    Attributes
    ----------
    customer : User
        Represents the site's user.
    product : Product
        It represents a product.
        It is a foreign key to the 'Product' model.
    rating : int
        Represents a user's rating for a product.
    comment : str
        Represents a user's comment on a product.
    published_date : datetime.date
        Represents the time a user reviewed a product.
    """
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

class AvgProductRatings(models.Model):
    """
    A class that extends Django's Model class.
    It is used to model average product ratings.

    Attributes
    ----------
    product : Product
        It represents a product.
        It has a one-to-one relationship with the 'Product' model.
    no_of_ratings : int
        Represents the number of ratings of a product.
    avg_rating : float
        Represents the average rating of a product.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    no_of_ratings = models.IntegerField()
    avg_rating = models.FloatField()

class ProductSales(models.Model):
    """
    A class that extends Django's Model class.
    It models a product sales stats.

    Attributes
    ----------
    product : Product
        It represents a product.
        It has a one-to-one relationship with the 'Product' model.
    copies_sold : int
        Represents the number of copies sold of a product.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    copies_sold = models.IntegerField()
