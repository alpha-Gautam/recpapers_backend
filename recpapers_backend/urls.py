"""
URL configuration for recpapers_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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



# Routers provide an easy way of automatically determining the URL conf.
from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to RecPapers Backend API.\n Please use the /api/ or /chatApi/ endpoints for accessing the APIs.")

urlpatterns = [
    path('', index, name='index'),
    
    path('admin/', admin.site.urls),
    path('api/', include('recpaper_app.api.urls')),
    path('chatApi/', include('chat_app.api.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    # path('account/',include('authentication_app.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    