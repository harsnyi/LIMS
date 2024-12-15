from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import plotly.graph_objects as go
from plotly.io import to_json
from django.db import transaction
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Q

from .models import (
    FeedData,
    Sales,
    HatchData,
    DeathRecord,
    OtherExpenses,
    ConsumeRecord,
    EggSale
)
def get_expense_type(value):
    value = value.lower()
    if value == "vitamin":
        return 1
    elif value == "gyogyszer":
        return 2
    elif value == "premix":
        return 3
    elif value == "szelidgesztenye_por":
        return 4
    elif value == "takarmanyszen":
        return 5
    
MODEL_MAPPING = {
    "feed_data": {
        "model": FeedData,
        "fields": ["date", "quantity", "total_price", "food_type"],
        "transforms": {
            "food_type": lambda value: 1 if value.lower() == "grain" else 2
        }
    },
    "other_expenses": {
        "model": OtherExpenses,
        "fields": ["date", "expense_type", "price"],
        "transforms": {
            "expense_type": get_expense_type
        }
    },
    "hatched": {
        "model": HatchData,
        "fields": ["date", "quantity"]
    },
    "consumed": {
        "model": ConsumeRecord,
        "fields": ["date", "quantity"]
    },
    "sales": {
        "model": Sales,
        "fields": ["date", "quantity", "price", "kilograms"]
    },
    "saled_eggs": {
        "model": EggSale,
        "fields": ["date", "quantity", "price"]
    },
    "perished": {
        "model": DeathRecord,
        "fields": ["date", "quantity"]
    },
}

@csrf_exempt
def upload_data(request):
    if request.method == 'POST':
        #try:
            body = json.loads(request.body)

            # Begin a transaction to ensure atomicity
            with transaction.atomic():
                for item_id, content in body.items():
                    data_dict = content.get("data")
                    
                    if not data_dict:
                        continue

                    for key, values in data_dict.items():
                        model_info = MODEL_MAPPING.get(key)
                        
                        if not model_info:
                            continue

                        model_class = model_info["model"]
                        fields = model_info["fields"]
                        transforms = model_info.get("transforms", {})

                        data = {}
                        for field in fields:
                            value = values.get(field)
                            # Apply transformation if specified
                            if field in transforms:
                                value = transforms[field](value)
                            data[field] = value
                        
                        model_class.objects.create(**data)

            return JsonResponse({"message": "Data saved successfully!"}, status=201)

        #except Exception as e:
        #    return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def dashboard_view(request):
    years = get_available_years()
    
    return render(request, 'dashboard/dashboard.html', {'years': years})
    
    
def expenses_view(request):
    years = get_available_years()
    
    return render(request, 'dashboard/expenses.html', {'years': years})

def income_view(request):
    years = get_available_years()
    
    return render(request, 'dashboard/incomes.html', {'years': years})

def care_view(request):
    years = get_available_years()
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    print(f"available months {months}")
    
    return render(request, 'dashboard/care.html', {'years': years, 'months': months})

@csrf_exempt
def get_hatch_data_chart(request):
    body = json.loads(request.body)
    years = body.get('years', [])
    months = body.get('months', [])

    # Filter data by years and months
    hatch_data = (
        HatchData.objects.filter(
            date__year__in=years,
            date__month__in=months
        )
        .values('date', 'quantity')
        .annotate(year=ExtractYear('date'))
        .order_by('date')
    )
    
    # Query DeathRecord
    death_data = (
        DeathRecord.objects.filter(
            date__year__in=years,
            date__month__in=months
        )
        .values('date', 'quantity')
        .annotate(year=ExtractYear('date'))
        .order_by('date')
    )
    
    consume_data = (
        ConsumeRecord.objects.filter(
            date__year__in=years,
            date__month__in=months
        )
        .values('date', 'quantity')
        .annotate(year=ExtractYear('date'))
        .order_by('date')
    )
    

    hatch_dates = [record['date'] for record in hatch_data]
    hatch_quantities = [record['quantity'] for record in hatch_data]

    death_dates = [record['date'] for record in death_data]
    death_quantities = [record['quantity'] for record in death_data]
    
    consume_dates = [record['date'] for record in consume_data]
    consume_quantities = [record['quantity'] for record in consume_data]

    fig_hatch = go.Figure()
    fig_hatch.add_trace(go.Scatter(x=hatch_dates, y=hatch_quantities, mode='lines+markers', name='Hatches'))

    fig_hatch.update_layout(
        title="Hatches Over Selected Years and Months",
        xaxis_title="Date",
        yaxis_title="Quantity",
        template="plotly",
    )
    
    fig_death = go.Figure()
    fig_death.add_trace(go.Scatter(x=death_dates, y=death_quantities, mode='lines+markers', name='Deaths'))
    fig_death.add_trace(go.Scatter(x=consume_dates, y=consume_quantities, mode='lines+markers', name='Consumes'))
    
    fig_death.update_layout(
        title="Halálozások és saját felhasználás az adott időszakban",
        xaxis_title="Date",
        yaxis_title="Quantity",
        template="plotly",
    )

    total_hatches = sum(hatch_quantities)
    total_deaths = sum(death_quantities)
    total_consumes = sum(consume_quantities)

    # Create pie chart
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=['Hatches', 'Deaths', 'Consumes'],
        values=[total_hatches, total_deaths, total_consumes],
        textinfo='label+percent',
        hoverinfo='label+value'
    ))

    fig_pie.update_layout(
        title="Proportions of Hatches, Deaths, and Consumes",
        template="plotly",
    )

    # Prepare response
    response_data = {
        "hatch_chart": fig_hatch.to_dict(),
        "death_chart": fig_death.to_dict(),
        "pie_chart": fig_pie.to_dict()
    }

    return JsonResponse(response_data)



def get_available_years():
    years = set()

    models = [ConsumeRecord, DeathRecord, EggSale, FeedData, HatchData, OtherExpenses, Sales]

    for model in models:
        years.update(
            model.objects.annotate(year=ExtractYear('date')).values_list('year', flat=True).distinct()
        )

    return sorted(years, reverse=True)