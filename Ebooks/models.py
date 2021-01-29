from django.conf import settings
from django.db import models
from Products.models import Product

class Ebook(models.Model):
    """
    A class that extends Django's Model class.
    It is used to model Ebooks of the existing Products.

    Attributes
    ----------
    product : Product
        Represents existing Product objects.
        It is a foreign key to the 'Product' model.
    product_file : str
        Stores the path to the ebook file location.

    Methods
    -------
    __str(self)__
        Returns the string representation of the model object.
    """
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_file = models.FileField(upload_to='ebooks/', default='settings.MEDIA_ROOT/ebooks/ebook.epub')

    def __str__(self):
        """
        Returns
        -------
        The product title of the ebook.
        """
        return self.product.Title

class MyEbooks(models.Model):
    """
    A class that extends Django's Model class.
    It is used to model the relationship between ebooks and users that own them.

    Attributes
    ----------
    customer : User
        Represents users modeled by the User model.
        It is a foreign key to the 'User' model.
    ebook : Ebook
        Represents an Ebook.
        It is a foreign key to the 'Ebook' model.
    """
    class Meta:
        """
        An inner class that specifies the meta data of the Model class.
        In this case the model's default field configurations have been Overrided.

        Attributes
        ----------
        unique_together : list
            Contains constraints to be applied on the model.
            In this case a composite unique key is defined on 'customer' and 'ebook' fields.
        """
        unique_together = [['customer', 'ebook']]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
