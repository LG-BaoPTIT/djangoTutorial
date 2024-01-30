"""
URL configuration for ecomstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from preview.views import home
from django.views.static import serve
from catalog.views import index, show_category, show_product
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    path('cart/',  include('cart.urls')),
    path('',  include('catalog.urls')),

    # Add other URL patterns as needed
]

handler404 = 'ecomstore.views.file_not_found_404' 


