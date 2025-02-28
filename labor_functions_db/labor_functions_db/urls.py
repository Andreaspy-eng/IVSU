"""
URL configuration for labor_functions_db project.

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

from django.contrib import admin
from django.urls import path
from professions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profession/<int:profession_id>/', views.profession_detail, name='profession_detail'),
    path('', views.index, name='index'),
    path('add-profession/', views.add_profession, name='add_profession'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('profession/<int:profession_id>/add-details/', views.add_details, name='add_details'),
    path('profession/<int:profession_id>/delete/', views.delete_profession, name='delete_profession'),
    path('profession/<int:profession_id>/edit/', views.edit_profession, name='edit_profession'),
    path('labor-function/<int:labor_function_id>/edit/', views.edit_labor_function, name='edit_labor_function'),
]
