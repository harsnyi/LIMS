import json
from datetime import datetime

import pandas as pd
from django.db import transaction
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from dashboard.visualization import (
    get_consume_death_hatch_distribution_pie,
    get_death_figure,
    get_feeding_figure,
    get_feedings_boxplot,
    get_grain_nutrition_distribution_pie,
    get_hatch_figure,
    get_other_expenses_distribution_pie,
    get_income_heatmap,
    get_sells_figure,
    get_sell_quantity_histogram,
    get_income_chart,
    get_expenditure_chart,
    get_stock_chart,
)

from .models import (
    ConsumeRecord,
    DeathRecord,
    EggSale,
    FeedData,
    HatchData,
    OtherExpenses,
    Sales,
    Stock,
)

STATIC_IP = "192.168.1.10"


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
        "transforms": {"food_type": lambda value: 1 if value.lower() == "grain" else 2},
    },
    "other_expenses": {
        "model": OtherExpenses,
        "fields": ["date", "expense_type", "price"],
        "transforms": {"expense_type": get_expense_type},
    },
    "hatched": {"model": HatchData, "fields": ["date", "quantity"]},
    "consumed": {"model": ConsumeRecord, "fields": ["date", "quantity"]},
    "sales": {"model": Sales, "fields": ["date", "quantity", "price", "kilograms"]},
    "saled_eggs": {"model": EggSale, "fields": ["date", "quantity", "price"]},
    "perished": {"model": DeathRecord, "fields": ["date", "quantity"]},
}


@csrf_exempt
def upload_stock(request):
    if request.method == "POST":
        body = json.loads(request.body)
        data = body.get("count")
        count = data.get("data")
        today = datetime.now().date()

        stock, created = Stock.objects.get_or_create(
            date=today, defaults={"quantity": count}
        )

        if not created:
            stock.quantity = count
            stock.save()

            return JsonResponse(
                {"message": "Állomány sikeresen frissítve!"}, status=200
            )

        return JsonResponse({"message": "Állomány sikeresen létrehozva!"}, status=201)

    return JsonResponse({"error": "Hibás lekérdezés!"}, status=405)


@csrf_exempt
def upload_data(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            with transaction.atomic():
                for _, content in body.items():
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
                            if field in transforms:
                                value = transforms[field](value)
                            data[field] = value

                        model_class.objects.create(**data)

            return JsonResponse({"message": "Sikeresen mentett adatok!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Hibás lekérdezés"}, status=405)


@csrf_exempt
def dashboard_view(request):
    years = get_available_years()

    return render(
        request,
        "dashboard/dashboard.html",
        {"years": years, "static_ip": STATIC_IP, "page_title": "Harsányi Farm"},
    )


@csrf_exempt
def expenses_view(request):
    years = get_available_years()
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    return render(
        request,
        "dashboard/expenses.html",
        {
            "years": years,
            "months": months,
            "static_ip": STATIC_IP,
            "page_title": "Kiadások",
        },
    )


@csrf_exempt
def income_view(request):
    years = get_available_years()
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    return render(
        request,
        "dashboard/incomes.html",
        {
            "years": years,
            "months": months,
            "static_ip": STATIC_IP,
            "page_title": "Bevételek",
        },
    )


@csrf_exempt
def care_view(request):
    years = get_available_years()
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    return render(
        request,
        "dashboard/care.html",
        {
            "years": years,
            "months": months,
            "static_ip": STATIC_IP,
            "page_title": "Gondozás",
        },
    )


@csrf_exempt
def get_hatch_data_chart(request):
    body = json.loads(request.body)
    years = body.get("years", [])
    months = body.get("months", [])

    hatch_data = (
        HatchData.objects.filter(date__year__in=years, date__month__in=months)
        .values("date", "quantity")
        .annotate(year=ExtractYear("date"))
        .order_by("date")
    )

    death_data = (
        DeathRecord.objects.filter(date__year__in=years, date__month__in=months)
        .values("date", "quantity")
        .annotate(year=ExtractYear("date"))
        .order_by("date")
    )

    consume_data = (
        ConsumeRecord.objects.filter(date__year__in=years, date__month__in=months)
        .values("date", "quantity")
        .annotate(year=ExtractYear("date"))
        .order_by("date")
    )

    hatch_dates = [record["date"] for record in hatch_data]
    hatch_quantities = [record["quantity"] for record in hatch_data]

    death_dates = [record["date"] for record in death_data]
    death_quantities = [record["quantity"] for record in death_data]

    consume_dates = [record["date"] for record in consume_data]
    consume_quantities = [record["quantity"] for record in consume_data]

    total_hatches = sum(hatch_quantities)
    total_deaths = sum(death_quantities)
    total_consumes = sum(consume_quantities)

    response_data = {
        "hatch_chart": get_hatch_figure(hatch_dates, hatch_quantities).to_dict(),
        "death_chart": get_death_figure(
            death_dates, death_quantities, consume_dates, consume_quantities
        ).to_dict(),
        "pie_chart": get_consume_death_hatch_distribution_pie(
            total_hatches, total_deaths, total_consumes
        ).to_dict(),
        "total_hatches": total_hatches,
        "total_deaths": total_deaths,
        "total_consumes": total_consumes,
    }

    return JsonResponse(response_data)


@csrf_exempt
def get_expenses_data(request):
    body = json.loads(request.body)
    years = body.get("years", [])
    months = body.get("months", [])

    feed_data = (
        FeedData.objects.filter(date__year__in=years, date__month__in=months)
        .values("date", "quantity", "food_type", "total_price")
        .annotate(year=ExtractYear("date"))
        .order_by("date")
    )

    other_expenses_data = OtherExpenses.objects.filter(
        date__year__in=years, date__month__in=months
    ).values("expense_type", "price")

    expense_totals = {}
    for record in other_expenses_data:
        expense_type = record["expense_type"]
        price = record["price"]
        expense_totals[expense_type] = expense_totals.get(expense_type, 0) + price

    expense_labels = [
        dict(OtherExpenses.EXPENSE_CHOICES).get(
            expense_type, f"Unknown ({expense_type})"
        )
        for expense_type in expense_totals.keys()
    ]

    expense_values = list(expense_totals.values())

    feed_dates = [record["date"] for record in feed_data]
    feed_quantities = [record["quantity"] for record in feed_data]
    feed_total_price = [record["total_price"] for record in feed_data]
    feed_food_types = [record["food_type"] for record in feed_data]

    grain_quantity = 0
    nutrition_quantity = 0
    for food_type, quantity in zip(feed_food_types, feed_quantities):
        if food_type == 1:
            grain_quantity += quantity
        elif food_type == 2:
            nutrition_quantity += quantity

    grain_dates = [
        date for date, food_type in zip(feed_dates, feed_food_types) if food_type == 1
    ]
    grain_prices = [
        price
        for price, food_type in zip(feed_total_price, feed_food_types)
        if food_type == 1
    ]

    nutrition_dates = [
        date for date, food_type in zip(feed_dates, feed_food_types) if food_type == 2
    ]
    nutrition_prices = [
        price
        for price, food_type in zip(feed_total_price, feed_food_types)
        if food_type == 2
    ]

    response_data = {
        "feed_chart": get_feeding_figure(
            grain_dates, grain_prices, nutrition_dates, nutrition_prices
        ).to_dict(),
        "pie_chart_feed": get_grain_nutrition_distribution_pie(
            grain_quantity, nutrition_quantity
        ).to_dict(),
        "heatmap_chart": get_feedings_boxplot(feed_total_price).to_dict(),
        "pie_chart_expenses": get_other_expenses_distribution_pie(
            expense_labels, expense_values
        ).to_dict(),
        "total_price": sum(feed_total_price),
        "total_expenses": sum(expense_values),
        "total_grain": sum(grain_prices),
        "total_nutrition": sum(nutrition_prices),
        "total_quantity": sum(feed_quantities),
    }
    if feed_data:
        response_data["average_price"] = response_data["total_price"] / len(feed_data)
    return JsonResponse(response_data)


@csrf_exempt
def get_income_data(request):
    body = json.loads(request.body)
    years = body.get("years", [])
    months = body.get("months", [])

    sell_data = (
        Sales.objects.filter(date__year__in=years, date__month__in=months)
        .values("date", "quantity", "price", "kilograms")
        .annotate(year=ExtractYear("date"))
        .order_by("date")
    )

    egg_sale_data = (
        EggSale.objects.filter(date__year__in=years, date__month__in=months)
        .values("date", "quantity", "price")
        .annotate(year=ExtractYear("date"))
        .order_by("date")
    )

    sell_dates = [record["date"] for record in sell_data]
    sell_quantities = [record["quantity"] for record in sell_data]
    sell_prices = [record["price"] for record in sell_data]
    sell_kilos = [record["kilograms"] for record in sell_data]

    egg_sale_prices = [record["price"] for record in egg_sale_data]
    egg_sale_dates = [record["date"] for record in egg_sale_data]

    all_dates = sell_dates + egg_sale_dates
    all_prices = sell_prices + egg_sale_prices

    df = pd.DataFrame({"date": all_dates, "price": all_prices})

    df["date"] = pd.to_datetime(df["date"])

    df["week"] = df["date"].dt.to_period("W").dt.start_time
    heatmap_data = df.groupby("week")["price"].sum().reset_index()

    heatmap_data = heatmap_data.sort_values("week")
    start_date = pd.to_datetime(f"{years[0]}-01-01")
    end_date = pd.to_datetime(f"{years[-1]}-12-31")
    all_weeks = pd.date_range(start=start_date, end=end_date, freq="W-MON")

    all_weeks_df = pd.DataFrame({"week": all_weeks, "price": [None] * len(all_weeks)})

    heatmap_data = pd.merge(all_weeks_df, heatmap_data, how="left", on="week")

    heatmap_data["price"] = heatmap_data["price_y"].fillna(0)

    x_weeks = heatmap_data["week"].dt.strftime("%Y-%m-%d").tolist()
    y_prices = heatmap_data["price"].tolist()

    response_data = {
        "sell_chart": get_sells_figure(
            sell_dates, sell_prices, egg_sale_dates, egg_sale_prices
        ).to_dict(),
        "heatmap_chart": get_income_heatmap(x_weeks, y_prices).to_dict(),
        "sell_hist_chart": get_sell_quantity_histogram(sell_quantities).to_dict(),
        "total_price": sum(sell_prices) + sum(egg_sale_prices),
        "total_quantity": sum(sell_quantities),
        "total_kilos": sum(sell_kilos),
    }

    return JsonResponse(response_data)


@csrf_exempt
def get_info_data(request):
    body = json.loads(request.body)
    years = body.get("years", [])

    if not years:
        return JsonResponse({"error": "No years selected"}, status=400)

    sell_data = (
        Sales.objects.filter(
            date__year__in=years,
        )
        .values("date", "price")
        .annotate(year=ExtractYear("date"), month=ExtractMonth("date"))
        .order_by("date")
    )

    egg_sell_data = (
        EggSale.objects.filter(
            date__year__in=years,
        )
        .values("date", "price")
        .annotate(year=ExtractYear("date"), month=ExtractMonth("date"))
        .order_by("date")
    )

    sell_df = pd.DataFrame(list(sell_data))
    if sell_df.empty:
        sell_df = pd.DataFrame(columns=["date", "price", "year", "month"])
    sell_df["date"] = pd.to_datetime(sell_df["date"])
    sell_df_monthly_data = (
        sell_df.groupby(["year", "month"])["price"].sum().reset_index()
    )

    egg_sell_df = pd.DataFrame(list(egg_sell_data))
    if egg_sell_df.empty:
        egg_sell_df = pd.DataFrame(columns=["date", "price", "year", "month"])
    egg_sell_df["date"] = pd.to_datetime(egg_sell_df["date"])
    egg_sell_data_monthly = (
        egg_sell_df.groupby(["year", "month"])["price"].sum().reset_index()
    )

    income_monthly_data = pd.concat(
        [sell_df_monthly_data, egg_sell_data_monthly], ignore_index=True
    )
    income_monthly_data = (
        income_monthly_data.groupby(["year", "month"]).sum().reset_index()
    )

    feed_data = (
        FeedData.objects.filter(
            date__year__in=years,
        )
        .values("date", "total_price")
        .annotate(year=ExtractYear("date"), month=ExtractMonth("date"))
        .order_by("date")
    )

    stock_data = (
        Stock.objects.filter(
            date__year__in=years,
        )
        .values("date", "quantity")
        .annotate(
            year=ExtractYear("date"),
        )
        .order_by("date")
    )

    other_expenses = (
        OtherExpenses.objects.filter(
            date__year__in=years,
        )
        .values("date", "price")
        .annotate(year=ExtractYear("date"), month=ExtractMonth("date"))
        .order_by("date")
    )

    feed_df = pd.DataFrame(list(feed_data))
    if feed_df.empty:
        feed_df = pd.DataFrame(columns=["date", "total_price", "year", "month"])

    feed_df["date"] = pd.to_datetime(feed_df["date"])
    feed_df["price"] = feed_df["total_price"]
    feed_df = feed_df.drop(columns=["total_price"])

    feed_monthly_data = feed_df.groupby(["year", "month"])["price"].sum().reset_index()

    other_expenses_df = pd.DataFrame(list(other_expenses))
    if other_expenses_df.empty:
        other_expenses_df = pd.DataFrame(columns=["date", "price", "year", "month"])

    other_expenses_df["date"] = pd.to_datetime(other_expenses_df["date"])
    other_expenses_monthly_data = (
        other_expenses_df.groupby(["year", "month"])["price"].sum().reset_index()
    )

    expenditure_monthly_data = pd.concat(
        [feed_monthly_data, other_expenses_monthly_data], ignore_index=True
    )

    expenditure_monthly_data = (
        expenditure_monthly_data.groupby(["year", "month"]).sum().reset_index()
    )
    all_months = pd.DataFrame(
        [{"year": year, "month": month} for year in years for month in range(1, 13)]
    )
    all_months["year"] = all_months["year"].astype(int)
    all_months["month"] = all_months["month"].astype(int)

    income_monthly_data = pd.merge(
        all_months, income_monthly_data, on=["year", "month"], how="left"
    ).fillna(0)
    income_monthly_data["price"] = income_monthly_data["price"].astype(float)

    expenditure_monthly_data = pd.merge(
        all_months, expenditure_monthly_data, on=["year", "month"], how="left"
    ).fillna(0)
    expenditure_monthly_data["price"] = expenditure_monthly_data["price"].astype(float)

    total_income = income_monthly_data["price"].sum()
    total_expenditure = expenditure_monthly_data["price"].sum()

    response_data = {
        "income_chart": get_income_chart(income_monthly_data).to_dict(),
        "expenditure_chart": get_expenditure_chart(expenditure_monthly_data).to_dict(),
        "total_income": total_income,
        "total_expenditure": total_expenditure,
        "total_profit": total_income - total_expenditure,
        "stock_chart": get_stock_chart(stock_data).to_dict(),
    }

    return JsonResponse(response_data)


def get_available_years():
    years = set()
    models = [
        ConsumeRecord,
        DeathRecord,
        EggSale,
        FeedData,
        HatchData,
        OtherExpenses,
        Sales,
    ]

    for model in models:
        years.update(
            model.objects.annotate(year=ExtractYear("date"))
            .values_list("year", flat=True)
            .distinct()
        )

    return sorted(years, reverse=True)
