from Ebooks.models import Ebook, MyEbooks

def get_ebook(product):
    """
    A function that retrieves an Ebook object from the 'Ebook' model.

    Parameters
    ----------
    product : Product
        A Product object.

    Returns
    -------
    Returns an ebook if it exists, otherwise None.
    """
    try:
        ebook = Ebook.objects.get(product=product)
        return ebook
    except:
        return None

def add_new_customer_ebook(customer, ebook):
    """
    A function that creates a new 'MyEbooks' object.
    It is used to add an ebook to a customer's collection.

    Parameters
    ----------
    customer : User
        Represents a site user.
    ebook : Ebook
        Represents an 'Ebook' object.
    """
    MyEbooks.objects.create(customer=customer, ebook=ebook)

def get_customer_ebook(customer, ebook):
    """
    A function that retrieves a MyEbooks object from the 'MyEbooks' model.
    It retrieves the specified ebook belonging to a customer.

    Parameters
    ----------
    customer : User
        Represents the a site user.
    ebook : Ebook
        Represents an 'Ebook' object.
    Returns
    -------
    Returns an ebook if it exists, otherwise None.
    """
    try:
        customer_ebook = MyEbooks.objects.get(customer=customer, ebook=ebook)
        return customer_ebook
    except:
        return None

def get_customer_ebooks(customer):
    """
    A function that retrieves MyEbooks objects from the 'MyEbooks' model.
    It retrieves all the ebooks belonging to a customer.

    Parameters
    ----------
    customer : User
        Represents the a site user.
    Returns
    -------
    Returns ebooks if they exist, otherwise None.
    """
    customer_ebooks = MyEbooks.objects.filter(customer=customer)
    return customer_ebooks

def is_purchased(customer, ebook):
    """
    A function that checks whether a MyEbooks object exists or not.
    It checks whether an ebook has been purchased by a user or not.

    Parameters
    ----------
    customer : User
        Represents the a site user.
    ebook : Ebook
        Represents an 'Ebook' object.
    Returns
    -------
    Returns True if a MyEbooks object exists, otherwise False.
    """
    product = get_customer_ebook(customer, ebook)
    if product is None:
        return False
    return True
