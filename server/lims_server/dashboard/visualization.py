import plotly.express as px
import plotly.graph_objects as go

COLOR_MAP = {
    "ORANGE": "#FF9B71",
    "RED": "#F45B69",
    "BLUE": "#42BFDD",
}


def get_hatch_figure(hatch_dates, hatch_quantities):
    fig_hatch = go.Figure()
    fig_hatch.add_trace(
        go.Bar(
            x=hatch_dates,
            y=hatch_quantities,
            name="Keltetések",
            marker=dict(color=COLOR_MAP["ORANGE"]),
        )
    )

    fig_hatch.update_layout(
        title="Keltetések az adott időszakban",
        xaxis_title="Dátum",
        yaxis_title="Darabszám",
        template="plotly",
        barmode="relative",
    )

    return fig_hatch


def get_death_figure(death_dates, death_quantities, consume_dates, consume_quantities):
    fig_death = go.Figure()
    fig_death.add_trace(
        go.Bar(
            x=death_dates,
            y=death_quantities,
            name="Halálozások",
            marker=dict(color=COLOR_MAP["RED"]),
        )
    )
    fig_death.add_trace(
        go.Bar(
            x=consume_dates,
            y=consume_quantities,
            name="Felhasználás",
            marker=dict(color=COLOR_MAP["BLUE"]),
        )
    )

    fig_death.update_layout(
        title="Halálozások és saját felhasználás az adott időszakban",
        xaxis_title="Dátum",
        yaxis_title="Darabszám",
        template="plotly",
        barmode="relative",
    )

    return fig_death


def get_consume_death_hatch_distribution_pie(
    total_hatches, total_deaths, total_consumes
):
    fig_pie = go.Figure()
    fig_pie.add_trace(
        go.Pie(
            labels=["Keltetés", "Halálozás", "Felhasználás"],
            values=[total_hatches, total_deaths, total_consumes],
            textinfo="label+percent",
            hoverinfo="label+value",
            marker=dict(
                colors=[COLOR_MAP["ORANGE"], COLOR_MAP["RED"], COLOR_MAP["BLUE"]],
                line=dict(color="#000000", width=1.5),
            ),
            hole=0.3,
        )
    )

    fig_pie.update_layout(
        title="Keltetés, halálozás, felhasználás aránya",
        template="plotly",
    )

    return fig_pie


def get_feeding_figure(grain_dates, grain_prices, nutrition_dates, nutrition_prices):
    fig_feeding = go.Figure()
    fig_feeding.add_trace(
        go.Bar(
            x=grain_dates,
            y=grain_prices,
            name="Gabona",
            marker=dict(color=COLOR_MAP["ORANGE"]),
        )
    )
    fig_feeding.add_trace(
        go.Bar(
            x=nutrition_dates,
            y=nutrition_prices,
            name="Táp",
            marker=dict(color=COLOR_MAP["BLUE"]),
        )
    )
    fig_feeding.update_layout(
        title="Etetések az adott időszakban",
        xaxis_title="Dátum",
        yaxis_title="Ár",
        template="plotly",
        barmode="relative",
    )
    return fig_feeding


def get_grain_nutrition_distribution_pie(grain_quantity, nutrition_quantity):
    fig_pie_feed = go.Figure()
    fig_pie_feed.add_trace(
        go.Pie(
            labels=["Gabona", "Táp"],
            values=[grain_quantity, nutrition_quantity],
            textinfo="label+percent",
            hoverinfo="label+value",
            marker=dict(
                colors=[COLOR_MAP["ORANGE"], COLOR_MAP["BLUE"]],
                line=dict(color="#000000", width=1.5),
            ),
            hole=0.3,
        )
    )
    fig_pie_feed.update_layout(
        title="Gabona és táp aránya",
        template="plotly",
    )

    return fig_pie_feed


def get_other_expenses_distribution_pie(expense_labels, expense_values):
    fig_pie_expenses = go.Figure()
    fig_pie_expenses.add_trace(
        go.Pie(
            labels=expense_labels,
            values=expense_values,
            textinfo="label+percent",
            hoverinfo="label+value",
            marker=dict(
                colors=px.colors.qualitative.Set3, line=dict(color="#000000", width=1.5)
            ),
            hole=0.3,
        )
    )
    fig_pie_expenses.update_layout(
        title="Költségtípusok aránya",
        template="plotly",
    )

    return fig_pie_expenses


def get_feedings_boxplot(feed_quantities):
    fig_boxplot = go.Figure(
        data=go.Box(
            y=feed_quantities,
            marker=dict(color=COLOR_MAP["ORANGE"]),
        )
    )

    fig_boxplot.update_layout(
        title="Etetések eloszlása",
        template="ggplot2",
    )

    return fig_boxplot


def get_income_heatmap(x_weeks, y_prices):
    fig_heatmap = go.Figure(
        data=go.Heatmap(
            x=x_weeks,
            y=[1] * len(x_weeks),
            z=y_prices,
            colorscale="Sunset",
            colorbar=dict(title="Ár"),
            hovertemplate="Hét: %{x}<br>Teljes ár: %{z} Ft<extra></extra>",
        )
    )

    fig_heatmap.update_layout(
        title="Heti eladások hőtérképe",
        xaxis_title="Hét",
        yaxis=dict(showticklabels=False),
        template="plotly",
        showlegend=False,
    )

    return fig_heatmap


def get_sells_figure(sell_dates, sell_prices, egg_sale_dates, egg_sale_prices):
    fig_sell = go.Figure()
    fig_sell.add_trace(
        go.Bar(x=sell_dates, y=sell_prices, name="Eladás", marker=dict(color="#FF9B71"))
    )
    fig_sell.add_trace(
        go.Bar(
            x=egg_sale_dates,
            y=egg_sale_prices,
            name="Tojás eladás",
            marker=dict(color="#42BFDD"),
        )
    )

    fig_sell.update_layout(
        title="Eladások az adott időszakban",
        xaxis_title="Dátum",
        template="plotly",
        barmode="relative",
    )

    return fig_sell


def get_sell_quantity_histogram(sell_quantities):
    fig_sell_hist = go.Figure()
    fig_sell_hist.add_trace(
        go.Histogram(
            x=sell_quantities,
            name="Eladási eloszlás",
            marker=dict(color="#F45B69"),
            nbinsx=30,
        )
    )

    fig_sell_hist.update_layout(
        title="Eladások mennyiségi eloszlása",
        xaxis_title="Darabszám",
        yaxis_title="Eladások száma",
        template="plotly",
        bargap=0.2,
    )

    return fig_sell_hist


def get_income_chart(income_monthly_data):
    fig_income = go.Figure()
    for year in sorted(income_monthly_data["year"].unique()):
        year_data = income_monthly_data[income_monthly_data["year"] == year]
        months = year_data["month"].tolist()
        prices = year_data["price"].tolist()

        fig_income.add_trace(
            go.Scatter(
                x=months,
                y=prices,
                mode="lines+markers",
                name=str(year),
                line=dict(width=2),
                marker=dict(size=8),
            )
        )
    fig_income.update_layout(
        title="Havi Bevétel",
        xaxis=dict(
            title="Hónap",
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=[
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
        ),
        yaxis_title="Bevétel (Ft)",
        template="plotly",
    )

    return fig_income


def get_expenditure_chart(expenditure_monthly_data):
    fig_expenditure = go.Figure()
    for year in sorted(expenditure_monthly_data["year"].unique()):
        year_data = expenditure_monthly_data[expenditure_monthly_data["year"] == year]
        months = year_data["month"].tolist()
        prices = year_data["price"].tolist()

        fig_expenditure.add_trace(
            go.Scatter(
                x=months,
                y=prices,
                mode="lines+markers",
                name=str(year),
                line=dict(width=2),
                marker=dict(size=8),
            )
        )
    fig_expenditure.update_layout(
        title="Havi Kiadás",
        xaxis=dict(
            title="Hónap",
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=[
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
        ),
        yaxis_title="Kiadás (Ft)",
        template="plotly",
    )

    return fig_expenditure


def get_stock_chart(stock_data):
    fig_stock = go.Figure()
    stock_dates = [record["date"] for record in stock_data]
    stock_quantities = [record["quantity"] for record in stock_data]
    fig_stock.add_trace(
        go.Scatter(
            x=stock_dates,
            y=stock_quantities,
            mode="lines+markers",
            line=dict(width=2),
            marker=dict(size=8),
        )
    )
    fig_stock.update_layout(
        title="Állomány számának alakulása",
    )

    return fig_stock
