
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from django.views.generic import RedirectView # Import this

urlpatterns = [
    # Redirect the root URL to the API root
    path('', RedirectView.as_view(url='api/', permanent=True)),
    
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]