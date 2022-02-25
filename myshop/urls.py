
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/',include('base.api.urls')) ,# kazdy url ktory bedzie sie zaczynal 'api', bedzie przekierowywal do api
     ]