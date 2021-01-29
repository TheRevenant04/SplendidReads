from django.urls import path
from Payments import views

#Namespace for the 'Payments' app.
app_name = "Payments"

urlpatterns = [
    #A URL mapped to the 'PaymentHistoryView' that renders a user's payment history.
    path('my_payments/',views.PaymentHistoryView.as_view(), name='my_payments'),
    #A URL mapped to the 'CreateCartOrderView' that creates an order for a user's cart products.
    path('product_cart_order/', views.CreateCartOrderView.as_view(), name='create_cart_order'),
    #A URL mapped to the 'CreateQuickOrderView' that creates an order for a product.
    path('product_quick_order/<pk>/', views.CreateQuickOrderView.as_view(), name='create_quick_order'),
    #A URL mapped to the 'CartPaymentStatusView' that renders the payment status of a cart order.
    path('payment_status/', views.CartPaymentStatusView.as_view(), name='cart_payment_status'),
    #A URL mapped to the 'QuickPaymentStatusView' that renders the payment status of an individual product order.
    path('quick_payment_status/<pk>/', views.QuickPaymentStatusView.as_view(), name='quick_payment_status'),
]
