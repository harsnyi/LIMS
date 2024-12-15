from django.urls import path
from .views import upload_data, dashboard_view, income_view, expenses_view, care_view, get_hatch_data_chart

urlpatterns = [
    path('upload_data', upload_data, name='upload_data'),
    path('', dashboard_view, name='info'),
    path('incomes', income_view, name='incomes'),
    path('expenses', expenses_view, name='expenses'),
    path('care', care_view, name='care'),
    path('get-hatch-chart/', get_hatch_data_chart, name='get_hatch_chart'),
]