from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

@csrf_exempt
def upload_data(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)

            for date_str, values in body.items():
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

                hatched = values["data"]["hatched"]
                perished = values["data"]["perished"]

                
            return JsonResponse({"message": "Data saved successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def dashboard_view(request):
    grid_items = list(range(1, 129))
    return render(request, 'dashboard/dashboard.html', {'grid_items': grid_items})