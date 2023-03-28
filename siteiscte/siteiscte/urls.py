from django.urls import include, path
from django.contrib import admin
urlpatterns = [
 path('votacao/', include('votacao.urls')),
 path('admin/', admin.site.urls),
]