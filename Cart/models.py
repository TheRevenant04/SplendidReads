from django.conf import settings
from django.db import models
from Products.models import Product

class Cart(models.Model):
    """
    A class that extends Django's Model class.
    It is used to model a user's shopping cart.

    Attributes
    ----------
    customer : User
        Represents the User to whom the Cart object belongs.
        It is a foreign key to the default User model.
    product : Product
        Represents a product in the Product model.
        It represents a product in a user's cart.
        It is a foreign key to the Product model.

    Methods
    -------
    __str__
        Returns a string representation of the Diary object.
    """
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.Title
