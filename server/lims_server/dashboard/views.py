from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import plotly.graph_objects as go
from plotly.io import to_json
from django.db import transaction

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
    grid_items = list(range(1, 129))
    # Create a simple Plotly figure
    fig = go.Figure(data=go.Bar(y=[2, 3, 1, 5], x=["A", "B", "C", "D"]))
    plotly_figure = to_json(fig)  # Serialize Plotly figure to JSON

    return render(request, 'dashboard/dashboard.html', {
        'grid_items': grid_items,
        'plotly_figure': plotly_figure
    })