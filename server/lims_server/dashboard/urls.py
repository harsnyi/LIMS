from django.urls import path
from .views import upload_data, dashboard_view

urlpatterns = [
    path('upload_data', upload_data, name='upload_data'),
    path('', dashboard_view, name='dashboard'),
]