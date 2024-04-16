from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from generator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate-token/', views.generate_token),
    path('receive-data/', views.receive_data),
    path('', TemplateView.as_view(template_name='generate_token.html'), name='token-generator'),
    path('item/', views.item, name='item'),
]

