"""SplendidReads URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    #The admin site URL.
    path('admin/', admin.site.urls),
    #Includes the 'Products' app URLs.
    path('',include('Products.urls')),
    #Includes the 'Accounts' app URLs.
    path('',include('Accounts.urls')),
    #Includes the 'Cart' app URLs.
    path('',include('Cart.urls')),
    #Includes the 'Payments' app URLs.
    path('',include('Payments.urls')),
    #Includes the 'Ebooks' app URLs.
    path('',include('Ebooks.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
