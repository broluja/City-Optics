from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('products/', include('products.urls')),
    path('appointments/', include('appointments.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/appointments/', include('appointments.api_urls')),
    path('api/products/', include('products.api_urls')),
    path('api/accounts/', include('accounts.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'CityOptics Administration'
admin.site.index_title = 'Overview'
