from django.contrib import admin
from django.urls import path

from generator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate-token/', views.generate_token),
    path('receive-data/', views.receive_data),
]

