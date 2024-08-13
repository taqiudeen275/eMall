from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from .admin import BusinessAdminSite

business_admin_site = BusinessAdminSite(name='business_admin')

urlpatterns = [
    path('', include('products.urls')),
    path('admin/', admin.site.urls),
    path('business-admin/', business_admin_site.urls),
    path('account/', include('accounts.urls')),
    path('', include('ads.urls')),
    path('cart/', include('cart.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('orders/', include('orders.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    