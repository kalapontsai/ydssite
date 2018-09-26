"""ydssite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.contrib import admin
from django.urls import path
from index import views as index_views
from ate import views as ate_views

urlpatterns = [
	path('', index_views.index),
    path('admin/', admin.site.urls),
    path('ate/', ate_views.index),
    path('ate/test_item_list', ate_views.test_item_list),
    path('ate/device_yield', ate_views.device_yield),
    path('ate/spcc_xr', ate_views.spcc_xr),
]
