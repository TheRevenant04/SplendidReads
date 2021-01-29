from Cart.models import Cart
from Products.models import Product

def add_product_to_cart(customer, product):
    """
    A method that adds a product to a user's shopping cart.
    A new Cart instance is created and added to Cart.

    Parameters
    ----------
    customer : User
        Represents a user object. It is a User model instance.
    product : Product
        Reprsents a product in the Product model.

    """
    Cart.objects.create(customer=customer, product=product)

def get_cart_product(customer, product):
    """
    A method that retrieves a product from a user's shopping cart.

    Parameters
    ----------
    customer : User
        Represents a user object. It is a User model instance.
    product : Product
        Reprsents a product in the Product model.

    Returns
    -------
    existing_cart_product : Cart
        Returns a Cart object if it exists, otherwise None.
    """
    try:
        existing_cart_product = Cart.objects.get(customer=customer, product=product)
        return existing_cart_product
    except:
        return None

def get_cart_products(customer):
    """
    A method that retrieves all products from a user's shopping cart.

    Parameters
    ----------
    customer : User
        Represents a user object. It is a User model instance.

    Returns
    -------
    existing_cart_products : Cart
        Returns a list of Cart objects if they exist, otherwise None.
    """
    try:
        existing_cart_products = Cart.objects.filter(customer=customer)
        return existing_cart_products
    except:
        return None

def get_cart_total_amount(products):
    """
    A method that computes the total amount for products in a user's shopping cart.

    Parameters
    ----------
    products : Product
        Represents products in the Product model.

    Returns
    -------
    total_amount : int
        Returns a user's total payable amount for cart products.
    """
    total_amount = 0
    for product in products:
        total_amount = total_amount + product.product.Price
    return total_amount

def remove_cart_product(customer, product):
    """
    A method that removes a product from a user's shopping cart.

    Parameters
    ----------
    customer : User
        Represents a user object. It is a User model instance.
    product : Product
        Represents a product in the Product model.
    """
    Cart.objects.get(customer=customer, product=product).delete()

def remove_cart_products(customer):
    """
    A method removes all products from a user's shopping cart.

    Parameters
    ----------
    customer : User
        Represents a user object. It is a User model instance.
    """
    Cart.objects.filter(customer=customer).delete()
