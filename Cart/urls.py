from Cart import views
from django.urls import path

#Namespace for the Cart app.
app_name = "Cart"

urlpatterns = [
    #A URL mapped to CartPageView view that renders a user's cart on the cart page.
    path('cart/', views.CartPageView.as_view(), name='cart_page'),
    #A URL mapped to CartAddView view that adds a product to a user's cart.
    path('cart/add/<pk>/', views.CartAddView.as_view(), name='add_to_cart'),
    #A URL mapped to CartRemoveView view that removes a product from a user's cart.
    path('cart/remove/<pk>', views.CartRemoveView.as_view(), name='remove_from_cart'),
]
