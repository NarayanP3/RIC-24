"""RC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from . import views

admin.site.site_header = "RIC Admin"
admin.site.site_title = "RIC Admin Portal"
admin.site.index_title = "Welcome to RIC ADMIN PORTAL"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('microsoft-login/', views.microsoft_login.as_view(), name='microsoft_login'),
    path('', include('home.urls')),
    path('rc/', include('prev_edition.urls')),
    path('profile/', include('members.urls')),
    path('event/', include('event.urls')),
    path('team/', include('team.urls')),
    path('faq/', include('faq.urls')),
    path('sponsor/', include('sponsor.urls')),
    path('schedule/', include('schedule.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
