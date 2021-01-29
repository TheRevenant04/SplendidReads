from Cart.utils import add_product_to_cart, get_cart_product, get_cart_products, get_cart_total_amount, remove_cart_product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView
from Products.utils import SKU_filter

@method_decorator(login_required, name='dispatch')
class CartAddView(RedirectView):
    """
    A view that extends Django's default RedirectView.
    This view is used to add a product to a user's cart.

    Attributes
    ----------
    pattern_name : str
        Represents the pattern URL that the view redirects to.

    Methods
    -------
    get_redirect_url(self, *args, **kwargs)
        Handles GET requests and constructs the target URL for redirection
        It adds products to the user's cart.

    """
    pattern_name = "Cart:cart_page"
    def get_redirect_url(self, *args, **kwargs):
        """
        A method that constructs the URL.
        It creates a new Cart object if an object with the specified user and Product are not present.

        Parameters
        ----------
        *args
            Optional unnamed arguments.
        **kwargs
            Optional named arguments.
        """
        product = SKU_filter(kwargs['pk'])
        existing_cart_product = get_cart_product(self.request.user, product)
        if existing_cart_product is None:
            add_product_to_cart(self.request.user, product)
        return super().get_redirect_url()

@method_decorator(login_required, name='dispatch')
class CartPageView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render a user's cart.

    Attributes
    ----------
    template_name : str
        Represents the template that the view redirects to.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests and returns a dictionary representing the template context.
        Retrieves a user's cart objects from the Cart model.
    """
    template_name = "Cart/cart.html"

    def get_context_data(self, **kwargs):
        """
        Creates a new Cart object if it is not present in the Cart model.

        Parameters
        ----------
        **kwargs
            Optional named arguments.

        Returns
        -------
        A cart page.
        """
        context = super(CartPageView, self).get_context_data(**kwargs)
        existing_cart_products = get_cart_products(self.request.user)
        context['cart'] = existing_cart_products
        context['cart_total_amount'] = get_cart_total_amount(existing_cart_products)
        context['message'] = "Your cart is currently empty"
        return context

@method_decorator(login_required, name='dispatch')
class CartRemoveView(RedirectView):
    """
    A view that extends Django's default RedirectView.
    This view is used to remove a product from a user's cart.

    Attributes
    ----------
    pattern_name : str
        Represents the url that the view redirects to.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests and redirects to the specified view.
        Deletes the specified object from the Cart model.
    """
    pattern_name = "Cart:cart_page"
    def get_redirect_url(self, *args, **kwargs):
        """
        A method that constructs the URL.
        It removes a Cart object if an object with the specified user and Product are present.

        Parameters
        ----------
        **kwargs
            Optional named arguments.
        """
        product = SKU_filter(kwargs['pk'])
        remove_cart_product(self.request.user, product)
        return super().get_redirect_url()
