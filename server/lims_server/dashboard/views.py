from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import plotly.graph_objects as go
from plotly.io import to_json
from django.db import transaction
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Q
import plotly.express as px
from collections import defaultdict
import pandas as pd
from datetime import datetime

from .models import (
    FeedData,
    Sales,
    HatchData,
    DeathRecord,
    OtherExpenses,
    ConsumeRecord,
    EggSale,
    Stock
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
def upload_stock(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        data = body.get("count")
        count = data.get("data")
        
        # Get today's date without the time part
        today = datetime.now().date()
        
        # Check if a stock record exists for today
        stock, created = Stock.objects.get_or_create(
            date=today,
            defaults={'quantity': count}
        )
        
        if not created:
            # If a record exists, update its quantity
            stock.quantity = count  # Adjust this logic if you want to replace instead of increment
            stock.save()

            return JsonResponse({"message": "Stock updated successfully!"}, status=200)
        
        return JsonResponse({"message": "Stock created successfully!"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


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
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    return render(request, 'dashboard/expenses.html', {'years': years, 'months': months})

def income_view(request):
    years = get_available_years()
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    return render(request, 'dashboard/incomes.html', {'years': years, 'months': months})

def care_view(request):
    years = get_available_years()
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    
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
    fig_hatch.add_trace(go.Bar(x=hatch_dates, y=hatch_quantities, name='Hatches', marker=dict(color='#FF9B71')))

    fig_hatch.update_layout(
        title="Hatches Over Selected Years and Months",
        xaxis_title="Date",
        yaxis_title="Quantity",
        template="plotly",
        barmode='relative'
    )
    
    fig_death = go.Figure()

    fig_death.add_trace(go.Bar(x=death_dates, y=death_quantities, name='Deaths', marker=dict(color='#F45B69')))
    fig_death.add_trace(go.Bar(x=consume_dates, y=consume_quantities, name='Consumes', marker=dict(color='#42BFDD')))

    fig_death.update_layout(
        title="Halálozások és saját felhasználás az adott időszakban",
        xaxis_title="Date",
        yaxis_title="Quantity",
        template="plotly",
        barmode='relative'  # Group bars side by side
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
        hoverinfo='label+value',
        marker=dict(colors=['#FF9B71', '#F45B69', '#42BFDD']),
        hole=.3
    ))

    fig_pie.update_layout(
        title="Proportions of Hatches, Deaths, and Consumes",
        template="plotly",
    )

    # Prepare response
    response_data = {
        "hatch_chart": fig_hatch.to_dict(),
        "death_chart": fig_death.to_dict(),
        "pie_chart": fig_pie.to_dict(),
        "total_hatches": total_hatches,
        "total_deaths": total_deaths,
        "total_consumes": total_consumes
    }

    return JsonResponse(response_data)


@csrf_exempt
def get_expenses_data(request):
    body = json.loads(request.body)
    years = body.get('years', [])
    months = body.get('months', [])

    # Feed data processing
    feed_data = (
        FeedData.objects.filter(
            date__year__in=years,
            date__month__in=months
        )
        .values('date', 'quantity', 'food_type', 'total_price')
        .annotate(year=ExtractYear('date'))
        .order_by('date')
    )
    
    other_expenses_data = (
        OtherExpenses.objects.filter(
            date__year__in=years,
            date__month__in=months
        )
        .values('expense_type', 'price')
    )

    expense_totals = {}
    for record in other_expenses_data:
        expense_type = record['expense_type']
        price = record['price']
        expense_totals[expense_type] = expense_totals.get(expense_type, 0) + price

    expense_labels = [
        dict(OtherExpenses.EXPENSE_CHOICES).get(expense_type, f"Unknown ({expense_type})")
        for expense_type in expense_totals.keys()
    ]

    expense_values = list(expense_totals.values())

    feed_dates = [record['date'] for record in feed_data]
    feed_quantities = [record['quantity'] for record in feed_data]
    feed_total_price = [record['total_price'] for record in feed_data]
    feed_food_types = [record['food_type'] for record in feed_data]

    grain_quantity = 0
    nutrition_quantity = 0
    for food_type, quantity in zip(feed_food_types, feed_quantities):
        if food_type == 1:
            grain_quantity += quantity
        elif food_type == 2:
            nutrition_quantity += quantity
    
    grain_dates = [date for date, food_type in zip(feed_dates, feed_food_types) if food_type == 1]
    grain_prices = [price for price, food_type in zip(feed_total_price, feed_food_types) if food_type == 1]

    nutrition_dates = [date for date, food_type in zip(feed_dates, feed_food_types) if food_type == 2]
    nutrition_prices = [price for price, food_type in zip(feed_total_price, feed_food_types) if food_type == 2]

    fig_feeding = go.Figure()
    fig_feeding.add_trace(go.Bar(
        x=grain_dates,
        y=grain_prices,
        name='Gabona',
        marker=dict(color='#FF9B71')
    ))
    fig_feeding.add_trace(go.Bar(
        x=nutrition_dates,
        y=nutrition_prices,
        name='Táp',
        marker=dict(color='#42BFDD')
    ))
    fig_feeding.update_layout(
        title="Etetések az adott időszakban",
        xaxis_title="Dátum",
        yaxis_title="Ár",
        template="plotly",
        barmode='relative'
    )

    fig_pie_feed = go.Figure()
    fig_pie_feed.add_trace(go.Pie(
        labels=['Gabona', 'Táp'],
        values=[grain_quantity, nutrition_quantity],
        textinfo='label+percent',
        hoverinfo='label+value',
        marker=dict(colors=['#FF9B71', '#42BFDD']),
        hole=.3
    ))
    fig_pie_feed.update_layout(
        title="Gabona és táp aránya",
        template="plotly",
    )

    fig_pie_expenses = go.Figure()
    fig_pie_expenses.add_trace(go.Pie(
        labels=expense_labels,
        values=expense_values,
        textinfo='label+percent',
        hoverinfo='label+value',
        marker=dict(colors=px.colors.qualitative.Set3),
        hole=.3
    ))
    fig_pie_expenses.update_layout(
        title="Költségtípusok aránya",
        template="plotly",
    )
    
    
    # Create a boxplot figure
    fig_boxplot = go.Figure(data=go.Box(
        y=feed_quantities,
        boxpoints='all',  
        marker=dict(color='#FF9B71'),
    ))

    fig_boxplot.update_layout(
        title="Quantity Distribution Boxplot vs Date",
        xaxis_title="Date",
        yaxis_title="Quantity",
        template="plotly",
    )
    
    response_data = {
        "feed_chart": fig_feeding.to_dict(),
        "pie_chart_feed": fig_pie_feed.to_dict(),
        "heatmap_chart": fig_boxplot.to_dict(),
        "pie_chart_expenses": fig_pie_expenses.to_dict(),
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
    years = body.get('years', [])
    months = body.get('months', [])
    
    sell_data = (
        Sales.objects.filter(
            date__year__in=years,
            date__month__in=months
        )
        .values('date', 'quantity', 'price', 'kilograms')
        .annotate(year=ExtractYear('date'))
        .order_by('date')
    )
    
    egg_sale_data = (
        EggSale.objects.filter(
            date__year__in=years,
            date__month__in=months
        )
        .values('date', 'quantity', 'price')
        .annotate(year=ExtractYear('date'))
        .order_by('date')
    )
    
    sell_dates = [record['date'] for record in sell_data]
    sell_quantities = [record['quantity'] for record in sell_data]
    sell_prices = [record['price'] for record in sell_data]
    sell_kilos = [record['kilograms'] for record in sell_data]
    
    egg_sale_prices = [record['price'] for record in egg_sale_data]
    egg_sale_dates = [record['date'] for record in egg_sale_data]
    
    # Combine sell and egg_sale data into a single list for plotting
    all_dates = sell_dates + egg_sale_dates
    all_prices = sell_prices + egg_sale_prices
    
    df = pd.DataFrame({
        'date': all_dates,
        'price': all_prices
    })
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Group by week and calculate total price for each week
    df['week'] = df['date'].dt.to_period('W').dt.start_time  # Group by week, using the start date of the week
    heatmap_data = df.groupby('week')['price'].sum().reset_index()  # Change from mean to sum
    
    # Sort data by week
    heatmap_data = heatmap_data.sort_values('week')
    
    # Generate all weeks for the selected years
    start_date = pd.to_datetime(f'{years[0]}-01-01')
    end_date = pd.to_datetime(f'{years[-1]}-12-31')
    all_weeks = pd.date_range(start=start_date, end=end_date, freq='W-MON')
    
    # Create a DataFrame with all weeks and merge with the heatmap data
    all_weeks_df = pd.DataFrame({
        'week': all_weeks,
        'price': [None] * len(all_weeks)  # Placeholder for missing prices
    })
    
    heatmap_data = pd.merge(all_weeks_df, heatmap_data, how='left', on='week')
    
    heatmap_data['price'] = heatmap_data['price_y'].fillna(0)
 
    x_weeks = heatmap_data['week'].dt.strftime('%Y-%m-%d').tolist()
    y_prices = heatmap_data['price'].tolist()
    fig_heatmap = go.Figure(data=go.Heatmap(
        x=x_weeks, 
        y=[1]*len(x_weeks),
        z=y_prices,
        colorscale='Sunset',
        colorbar=dict(title='Price'),
        hovertemplate='Week: %{x}<br>Total Price: %{z}<extra></extra>'
    ))
    
    fig_heatmap.update_layout(
        title="Heti eladások hőtérképe",
        xaxis_title="Hét",
        yaxis=dict(
            showticklabels=False
        ),
        template="plotly",
        showlegend=False
    )
    
    fig_sell = go.Figure()
    fig_sell.add_trace(go.Bar(x=sell_dates, y=sell_prices, name='Eladás', marker=dict(color='#FF9B71')))
    fig_sell.add_trace(go.Bar(x=egg_sale_dates, y=egg_sale_prices, name='Tojás eladás', marker=dict(color='#42BFDD')))
    
    fig_sell.update_layout(
        title="Eladások az adott időszakban",
        xaxis_title="Dátum",
        yaxis_title="Ár",
        template="plotly",
        barmode='relative'
    )
    
    fig_sell_hist = go.Figure()
    fig_sell_hist.add_trace(go.Histogram(
        x=sell_quantities,
        name='Sell Quantities',
        marker=dict(color='#F45B69'),
        nbinsx=30
    ))

    fig_sell_hist.update_layout(
        title="Eladások mennyiségi eloszlása",
        xaxis_title="Quantity",
        yaxis_title="Count",
        template="plotly",
        bargap=0.2
    )
    
    response_data = {
        "sell_chart": fig_sell.to_dict(),
        "heatmap_chart": fig_heatmap.to_dict(),
        "sell_hist_chart": fig_sell_hist.to_dict(),
        "total_price": sum(sell_prices) + sum(egg_sale_prices),
        "total_quantity": sum(sell_quantities),
        "total_kilos": sum(sell_kilos)
    }
    
    return JsonResponse(response_data)

@csrf_exempt
def get_info_data(request):
    body = json.loads(request.body)
    years = body.get('years', [])
    
    if not years:
        return JsonResponse({"error": "No years selected"}, status=400)

    # Fetch sales data for income
    sell_data = (
        Sales.objects.filter(
            date__year__in=years,
        )
        .values('date', 'price')
        .annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        )
        .order_by('date')
    )
    
    # Create a DataFrame for income data
    income_df = pd.DataFrame(list(sell_data))
    income_df['date'] = pd.to_datetime(income_df['date'])
    income_monthly_data = income_df.groupby(['year', 'month'])['price'].sum().reset_index()

    # Fetch expenditure data
    feed_data = (
        FeedData.objects.filter(
            date__year__in=years,
        )
        .values('date', 'total_price')
        .annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        )
        .order_by('date')
    )
    
    stock_data = (
        Stock.objects.filter(
            date__year__in=years,
        )
        .values('date', 'quantity')
        .annotate(
            year=ExtractYear('date'),
        )
        .order_by('date')
    )
    

    other_expenses = (
        OtherExpenses.objects.filter(
            date__year__in=years,
        )
        .values('date', 'price')
        .annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        )
        .order_by('date')
    )
    
    # Create DataFrames for expenditure data
    feed_df = pd.DataFrame(list(feed_data))
    feed_df['date'] = pd.to_datetime(feed_df['date'])
    feed_df["price"] = feed_df["total_price"]
    feed_df = feed_df.drop(columns=["total_price"])
    
    feed_monthly_data = feed_df.groupby(['year', 'month'])['price'].sum().reset_index()
    
    other_expenses_df = pd.DataFrame(list(other_expenses))
    other_expenses_df['date'] = pd.to_datetime(other_expenses_df['date'])
    other_expenses_monthly_data = other_expenses_df.groupby(['year', 'month'])['price'].sum().reset_index()

    expenditure_monthly_data = pd.concat([feed_monthly_data, other_expenses_monthly_data], ignore_index=True)
    
    
    expenditure_monthly_data = expenditure_monthly_data.groupby(['year', 'month']).sum().reset_index()
    print(expenditure_monthly_data)
    all_months = pd.DataFrame([
        {'year': year, 'month': month} 
        for year in years 
        for month in range(1, 13)
    ])
    all_months['year'] = all_months['year'].astype(int)
    all_months['month'] = all_months['month'].astype(int)

    # Merge with income and expenditure data
    income_monthly_data = pd.merge(all_months, income_monthly_data, on=['year', 'month'], how='left').fillna(0)
    income_monthly_data['price'] = income_monthly_data['price'].astype(float)

    expenditure_monthly_data = pd.merge(all_months, expenditure_monthly_data, on=['year', 'month'], how='left').fillna(0)
    expenditure_monthly_data['price'] = expenditure_monthly_data['price'].astype(float)

    total_income = income_monthly_data['price'].sum()
    total_expenditure = expenditure_monthly_data['price'].sum()
    
    # Create income chart
    fig_income = go.Figure()
    for year in sorted(income_monthly_data['year'].unique()):
        year_data = income_monthly_data[income_monthly_data['year'] == year]
        months = year_data['month'].tolist()
        prices = year_data['price'].tolist()
        
        fig_income.add_trace(go.Scatter(
            x=months, 
            y=prices, 
            mode='lines+markers',
            name=str(year),
            line=dict(width=2),
            marker=dict(size=8)
        ))
    fig_income.update_layout(
        title="Havi Bevétel",
        xaxis=dict(
            title="Hónap",
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis_title="Bevétel (Ft)",
        template="plotly",
    )

    # Create expenditure chart
    fig_expenditure = go.Figure()
    for year in sorted(expenditure_monthly_data['year'].unique()):
        year_data = expenditure_monthly_data[expenditure_monthly_data['year'] == year]
        months = year_data['month'].tolist()
        prices = year_data['price'].tolist()
        
        fig_expenditure.add_trace(go.Scatter(
            x=months, 
            y=prices, 
            mode='lines+markers',
            name=str(year),
            line=dict(width=2),
            marker=dict(size=8)
        ))
    fig_expenditure.update_layout(
        title="Havi Kiadás",
        xaxis=dict(
            title="Hónap",
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis_title="Kiadás (Ft)",
        template="plotly",
    )
    
    fig_stock = go.Figure()
    stock_dates = [record['date'] for record in stock_data]
    stock_quantities = [record['quantity'] for record in stock_data]
    fig_stock.add_trace(go.Scatter(
            x=stock_dates, 
            y=stock_quantities, 
            mode='lines+markers',
            line=dict(width=2, color='#FF9B71'),  # Set the line color
            marker=dict(size=8, color='#FF9B71')  # Set the marker color
        ))
    
    response_data = {
        "income_chart": fig_income.to_dict(),
        "expenditure_chart": fig_expenditure.to_dict(),
        "total_income": total_income,
        "total_expenditure": total_expenditure,
        "total_profit": total_income - total_expenditure,
        "stock_chart": fig_stock.to_dict()
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