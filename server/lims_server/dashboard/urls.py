from django.urls import path
from .views import upload_data, dashboard_view, income_view, expenses_view, care_view, get_hatch_data_chart, get_expenses_data, get_income_data, get_info_data, upload_stock

urlpatterns = [
    path('upload_data', upload_data, name='upload_data'),
    path('upload_stock', upload_stock, name='upload_stock'),
    path('', dashboard_view, name='info'),
    path('incomes', income_view, name='incomes'),
    path('expenses', expenses_view, name='expenses'),
    path('care', care_view, name='care'),
    path('get_hatch_data_chart/', get_hatch_data_chart, name='get_hatch_chart'),
    path('get_expenses_data/', get_expenses_data, name='get_expenses_data'),
    path('get_income_data/', get_income_data, name='get_income_data'),
    path('get_info_data/', get_info_data, name='get_info_data'),
]