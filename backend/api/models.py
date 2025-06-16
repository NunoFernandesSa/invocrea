from django.db import models


# ===================
# ===== Company =====
# ===================
class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    siret = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==================
# ===== Client =====
# ==================
class Client(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


# Quote
class Quote(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes"
    )
    date = models.DateField(auto_now_add=True)
    reference = models.CharField(max_length=100, unique=True)
    valid_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Quote {self.reference} - {self.client}"


# Invoice
class Invoice(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices",
    )
    date = models.DateField(auto_now_add=True)
    reference = models.CharField(max_length=100, unique=True)
    linked_quote = models.OneToOneField(
        Quote, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Invoice {self.reference} - {self.client.name}"


# Line items (shared between quotes and invoices)
class LineItem(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quote = models.ForeignKey(
        Quote,
        on_delete=models.CASCADE,
        related_name="line_items",
        null=True,
        blank=True,
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="line_items",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.description} ({self.quantity} x {self.unit_price}€)"

    def total(self):
        return self.quantity * self.unit_price
