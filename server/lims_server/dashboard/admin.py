from django.contrib import admin
from .models import ConsumeRecord, DeathRecord, EggSale, FeedData, HatchData, OtherExpenses, Sales

@admin.register(ConsumeRecord)
class ConsumeRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'quantity', 'created_at', 'updated_at')
    list_filter = ('date',)
    search_fields = ('quantity',)

@admin.register(DeathRecord)
class DeathRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'quantity', 'created_at', 'updated_at')
    list_filter = ('date',)
    search_fields = ('quantity',)

@admin.register(EggSale)
class EggSaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'quantity', 'price', 'created_at', 'updated_at')
    list_filter = ('date',)
    search_fields = ('quantity', 'price')

@admin.register(FeedData)
class FeedDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'quantity', 'food_type', 'total_price', 'created_at', 'updated_at')
    list_filter = ('date', 'food_type')
    search_fields = ('quantity', 'total_price')

@admin.register(HatchData)
class HatchDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'quantity', 'created_at', 'updated_at')
    list_filter = ('date',)
    search_fields = ('quantity',)

@admin.register(OtherExpenses)
class OtherExpensesAdmin(admin.ModelAdmin):
    list_display = ('date', 'get_other_expense_display', 'price', 'created_at', 'updated_at')
    list_filter = ('date', 'other_expense')
    search_fields = ('price',)

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('date', 'quantity', 'kilograms', 'price', 'created_at', 'updated_at')
    list_filter = ('date',)
    search_fields = ('quantity', 'price')
