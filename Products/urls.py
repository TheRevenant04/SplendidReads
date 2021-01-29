from django.urls import path, include
from Products  import views

#Namespace for the 'Products' app.
app_name = "Products"

urlpatterns = [
    #A URL mapped to the 'HomePageView' that renders the home page.
    path('',views.HomePageView.as_view(), name='home_page'),
    #A URL mapped to the 'GenrePageView' that renders the genre page.
    path('genres/',views.GenrePageView.as_view(), name='genres'),
    #A URL mapped to the 'ViewAllView' that renders all products of a selected type.
    path('products/<product_filter>/', views.ViewAllView.as_view(), name='product_filter'),
    #A URL mapped to the 'ProductsView' that renders products of a specific genre.
    path('products/<genre>',views.ProductsView.as_view(), name='products'),
    #A URL mapped to the 'ProductPageView' that renders a product's details.
    path('product_page/<pk>/', views.ProductPageView.as_view(), name='product_page'),
    #A URL mapped to the 'RatingsPageView' that renders a product's ratings.
    path('product_reviews/<pk>/', views.RatingsPageView.as_view(), name='all_product_ratings'),
    #A URL mapped to the 'AutoCompleteView' that is used for autocompletion in the search bar.
    path('search_products_autocomplete/', views.AutoCompleteView.as_view(), name='search_products_autocomplete'),
    #A URL mapped to the 'ProductSearchView' that renders search results.
    path('search_products', views.ProductSearchView.as_view(), name='search_products'),
]
