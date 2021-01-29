from Payments.models import Payment

def create_payment(customer, order_id, payment_id, payment_signature):
    """
    A function that creates a new 'Payment' object.
    It creates a new payment.

    Parameters
    ----------
    customer : User
        Represents a site user.
    order_id : str
        Represents a unique order ID.
    payment_id : str
        Represents an order's payment ID.
    payment_signature : str
        Represents a payment signature to verify the authenticity of a payment.

    Returns
    -------
    A 'Payment' object.
    """
    payment = Payment.objects.create(customer=customer, order_id=order_id, payment_id=payment_id, payment_signature=payment_signature)
    return payment

def get_customer_payments(customer):
    """
    A function that retrieves 'Payment' objects.
    It retrieves a customer's payment history.

    Parameters
    ----------
    payments : Payment
        Represents a 'Payment' object.

    Returns
    -------
    A customer's payments.
    """
    payments = Payment.objects.filter(customer=customer).order_by('-payment_time')
    return payments
