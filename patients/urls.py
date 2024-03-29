"""patients URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from app.views import PatientCreate

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('guanli/', admin.site.urls),
    path('new-patient/', PatientCreate.as_view(), name='new-patient'),
    path('', RedirectView.as_view(url='new-patient/', permanent=False), name='index'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('nested_admin/', include('nested_admin.urls'))
]
