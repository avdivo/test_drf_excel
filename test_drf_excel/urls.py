"""test_drf_excel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import include, path
from rest_framework import routers
from myapi import views
from myapi.views import ClientAPIView, BillAPIView, TextAPIView, ExcelAPIView, ExcelToDbAPIView
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'file', views.FileUploadViewSet, basename='file')


urlpatterns = [
    path('admin/', admin.site.urls),
	path('upload/', include(router.urls)),
	path('api/v1/client', ClientAPIView.as_view()),
	path('api/v1/bills', BillAPIView.as_view()),
	path('api/v1/text', TextAPIView.as_view()),
	path('api/v1/excel', ExcelAPIView.as_view()),
	path('api/v1/excel_two', ExcelToDbAPIView.as_view()),

]