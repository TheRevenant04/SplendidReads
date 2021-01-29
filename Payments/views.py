from Cart.utils import get_cart_products, get_cart_total_amount, remove_cart_products
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from Ebooks.utils import add_new_customer_ebook, get_ebook
from Payments.models import Payment
from Payments.utils import create_payment, get_customer_payments
from Products.utils import get_product, set_product_sale_count
import random
import razorpay

client = razorpay.Client(auth=("Your KEY ID", "Your KEY SECRET"))

@method_decorator(login_required, name='dispatch')
class CartPaymentStatusView(View):
    """
    A class that extends Django's View class.
    It is used for rendering a user's cart products payment status.

    Methods
    -------
    post(self, request, *args, **kwargs)
        Handles POST requests.

    """
    def post(self, request, *args, **kwargs):
        """
        Renders the payment status page.
        On payment success, a new 'MyEbooks' object is created,'ProductSales' data is updated, a user's cart is emptied.
        All these operations are atomic.

        Parameters
        ----------
        request : HttpRequest
            Contains HttpRequest parameters.
        *args
            Optional unnamed arguments.
        **kwargs
            Optional named arguments.

        Returns
        -------
        Payment status of an order.
        """
        payment_details = {
            'razorpay_payment_id' : request.POST.get('razorpay_payment_id'),
            'razorpay_order_id' : request.POST.get('razorpay_order_id'),
            'razorpay_signature' : request.POST.get('razorpay_signature')
        }
        context = {
            'payment_id' : payment_details['razorpay_payment_id'],
            'order_id' : payment_details['razorpay_order_id'],
        }

        try:
            status = client.utility.verify_payment_signature(payment_details)
            context['status'] = 'Payment Successful'
            payment = create_payment(self.request.user, payment_details['razorpay_order_id'], payment_details['razorpay_payment_id'], payment_details['razorpay_signature'])
            context['payment_time'] = payment.payment_time
            with transaction.atomic():
                existing_cart_products = get_cart_products(self.request.user)
                if existing_cart_products is not None:
                    for cart_object in existing_cart_products:
                        ebook = get_ebook(cart_object.product)
                        add_new_customer_ebook(self.request.user, ebook)
                        set_product_sale_count(cart_object.product)
                remove_cart_products(self.request.user)
            payment.status = context['status']
            payment.save()
            return render(request, 'Payments/payment_status.html', context)
        except :
            context['status'] = 'Payment Failed'
            return render(request, 'Payments/payment_status.html', context)


@method_decorator(login_required, name='dispatch')
class CreateCartOrderView(View):
    """
    A class that extends Django's View class.
    It is used to create a cart order.

    Methods
    -------
    post(self, request, *args, **kwargs)
        Handles POST requests.
    """
    def post(self, request, *args, **kwargs):
        """
        Renders the checkout page.
        Creates a order using the Razorpay API.

        Parameters
        ----------
        request : HttpRequest
            Contains HttpRequest parameters.
        *args
            Optional unnamed arguments.
        **kwargs
            Optional named arguments.

        Returns
        -------
        Checkout page if an order is created otherwise, error message.
        """
        existing_cart_products = get_cart_products(self.request.user)
        order_amount = get_cart_total_amount(existing_cart_products)
        order_amount_paise = order_amount * 100
        order_currency = 'INR'
        order_response = client.order.create(dict(amount=order_amount_paise, currency=order_currency))
        order_id = order_response['id']
        order_status = order_response['status']
        context = {}
        if order_status=='created':
            context['amount_paise'] = order_amount_paise
            context['cart'] = existing_cart_products
            context['total_amount'] = order_amount
            context['order_id'] = order_id
            return render(request, 'Payments/checkout_page.html', context)
        return HttpResponse('Error')


@method_decorator(login_required, name='dispatch')
class CreateQuickOrderView(View):
    """
    A class that extends Django's View class.
    It is used to create a quick order.

    Methods
    -------
    post(self, request, *args, **kwargs)
        Handles POST requests.
    """
    def post(self, request, *args, **kwargs):
        """
        Renders the checkout page.
        Creates a order using the Razorpay API.

        Parameters
        ----------
        request : HttpRequest
            Contains HttpRequest parameters.
        *args
            Optional unnamed arguments.
        **kwargs
            Optional named arguments.

        Returns
        -------
        Checkout page if an order is created otherwise, error message.
        """
        product = get_product(kwargs['pk'])
        order_amount = product.Price
        order_amount_paise = order_amount * 100
        order_currency = 'INR'
        order_response = client.order.create(dict(amount=order_amount_paise, currency=order_currency))
        order_id = order_response['id']
        order_status = order_response['status']
        context = {}
        if order_status=='created':
            context['amount_paise'] = order_amount_paise
            context['product'] = product
            context['total_amount'] = order_amount
            context['order_id'] = order_id
            context['pk'] = kwargs['pk']
            return render(request, 'Payments/checkout_page.html', context)
        return HttpResponse('<h1>Error</h1>')


@method_decorator(login_required, name='dispatch')
class PaymentHistoryView(TemplateView):
    """
    A class that extends Django's TemplateView class.
    It is used to retrieve a user's payment history.

    Attributes
    ----------
    template_name : str
        Specifies the template to render.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests.
    """
    template_name = 'Payments/payment_history_page.html'

    def get_context_data(self, **kwargs):
        """
        Renders the customer's payment history page.

        Parameters
        ----------
        **kwargs
            Optional named arguments.

        Returns
        -------
        A customer's payment history.
        """
        context = super(PaymentHistoryView, self).get_context_data(**kwargs)
        context['payments'] = get_customer_payments(self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class QuickPaymentStatusView(View):
    """
    A class that extends Django's View class.
    It is used to retrieve a user's payment history.

    Attributes
    ----------
    template_name : str
        Specifies the template to render.

    Methods
    -------
    post(self, request, *args, **kwargs)
        Handles POST requests.
    """
    def post(self, request, *args, **kwargs):
        """
        Renders the payment status page.
        On payment success, a new 'MyEbooks' object is created,'ProductSales' data is updated.
        All these operations are atomic.

        Parameters
        ----------
        request : HttpRequest
            Contains HttpRequest parameters.
        *args
            Optional unnamed arguments.
        **kwargs
            Optional named arguments.

        Returns
        -------
        Payment status of an order.
        """
        payment_details = {
            'razorpay_payment_id' : request.POST.get('razorpay_payment_id'),
            'razorpay_order_id' : request.POST.get('razorpay_order_id'),
            'razorpay_signature' : request.POST.get('razorpay_signature')
        }
        context = {
            'payment_id' : payment_details['razorpay_payment_id'],
            'order_id' : payment_details['razorpay_order_id'],
        }

        try:
            status = client.utility.verify_payment_signature(payment_details)
            context['status'] = 'Payment Successful'
            payment = create_payment(self.request.user, payment_details['razorpay_order_id'], payment_details['razorpay_payment_id'], payment_details['razorpay_signature'])
            context['payment_time'] = payment.payment_time
            with transaction.atomic():
                product = get_product(kwargs['pk'])
                ebook = get_ebook(product)
                add_new_customer_ebook(self.request.user, ebook)
                set_product_sale_count(product)
            payment.status = context['status']
            payment.save()
            return render(request, 'Payments/payment_status.html', context)
        except:
            context['status'] = 'Payment Failure'
            return render(request, 'Payments/payment_status.html', context)
