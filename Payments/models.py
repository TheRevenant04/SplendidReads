from django.conf import settings
from django.db import models

class Payment(models.Model):
    """
    A class that extends Django's default Model class.
    It models the apps payments.

    Attributes
    ----------
    customer : User
        Represents the site's users.
        It is a foreign key to the User model.
    status : str
        Represents a payment status.
    order_id : str
        Represents a unique order ID.
    payment_id : str
        Represents a payment uniquely.
    payment_signature : str
        Used to verify whether a payment is authentic.
    payment_time : str
        Represents the time a payment was done.
    """
    customer =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="Payment Failed")
    order_id =  models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    payment_signature = models.CharField(max_length=100)
    payment_time = models.DateTimeField(auto_now_add=True)
