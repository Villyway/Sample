"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from base.views import Login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', never_cache(Login.as_view()), name="login"),
    path('', include('base.urls', namespace='base')),
    path('vendors/', include('vendors.urls', namespace='vendors')),
    path('products/',include('products.urls', namespace='products')),
    path('utils/', include('utils.urls', namespace='utils')),
    path('inventry/', include('inventry.urls', namespace='inventry')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('customers/', include('customers.urls', namespace='customers')),
    
]

# Static files Setup
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
