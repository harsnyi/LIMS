from django.db import models


class ConsumeRecord(models.Model):
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Consumed {self.quantity} on {self.date}"


class DeathRecord(models.Model):
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.quantity} deaths on {self.date}"


class EggSale(models.Model):
    quantity = models.PositiveIntegerField()
    price = models.BigIntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.quantity} eggs sold on {self.date} for {self.price} currency units"


class FeedData(models.Model):
    FOOD_TYPE_CHOICES = [
        (1, 'Gabona'),
        (2, 'Táp'),
    ]

    quantity = models.PositiveIntegerField()
    food_type = models.PositiveSmallIntegerField(
        choices=FOOD_TYPE_CHOICES
    )
    date = models.DateField()
    
    total_price = models.BigIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Feeding on {self.date}: {self.quantity} buckets of {'Gabona' if self.food_type == 1 else 'Táp'}"


class HatchData(models.Model):
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Hatch on {self.date}: {self.quantity} animals added."


class OtherExpenses(models.Model):
    EXPENSE_CHOICES = [
        (1, 'Vitamin'),
        (2, 'Gyógyszer'),
        (3, 'Premix'),
        (4, 'Szelidgesztenye por'),
        (5, 'Takarmányszén'),
    ]

    expense_type = models.PositiveSmallIntegerField(
        choices=EXPENSE_CHOICES
    )
    date = models.DateField()
    price = models.BigIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_expense_type_display()} on {self.date}: {self.price} Ft"


class Sales(models.Model):
    date = models.DateField()
    quantity = models.PositiveIntegerField()
    price = models.BigIntegerField()
    kilograms = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Sale on {self.date}: {self.quantity} items, {self.kilograms} kg for {self.price} Ft"
