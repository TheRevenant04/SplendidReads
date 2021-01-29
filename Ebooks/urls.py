from django.urls import path
from Ebooks import views

#Namespace for the Ebooks app.
app_name = "Ebooks"

urlpatterns = [
    #A URL mapped to the MyEbooksView that renders a user's ebooks.
    path('myebooks/', views.MyEbooksView.as_view(), name='my_ebooks'),
]
