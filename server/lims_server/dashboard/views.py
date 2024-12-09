from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import plotly.graph_objects as go
from plotly.io import to_json
from .models import HatchData, DeathRecord

@csrf_exempt
def upload_data(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            body = json.loads(request.body)

            # Loop through each date in the JSON
            for date_str, values in body.items():
                # Convert date string to a date object
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

                # Extract data for hatched and perished (if available)
                hatched = values["data"].get("hatched")
                perished = values["data"].get("perished")

                # Save hatched data if it exists
                if hatched is not None:
                    HatchData.objects.create(
                        quantity=hatched,
                        date=date
                    )

                # Save perished data if it exists
                if perished is not None:
                    DeathRecord.objects.create(
                        quantity=perished,
                        date=date
                    )

            return JsonResponse({"message": "Data saved successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

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