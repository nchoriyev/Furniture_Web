from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('furnitures.urls')),
    path('auth/', include('users.urls')),
    path('order/', include('orders.urls')),
    path('delivery/', include('delivery.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
