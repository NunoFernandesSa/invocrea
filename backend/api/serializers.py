from rest_framework import serializers
from .models import Client, Quote, Invoice, LineItem
from datetime import datetime


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = ["id", "description", "quantity", "unit_price", "total"]
        read_only_fields = ["total"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "company",
            "name",
            "email",
            "phone",
            "address",
            "siret",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class QuoteSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True, required=False)

    class Meta:
        model = Quote
        fields = ["id", "client", "date", "reference", "valid_until", "line_items"]
        read_only_fields = ["date", "reference"]

    def create(self, validated_data):
        line_items_data = validated_data.pop("line_items", [])

        # Generate reference number
        year = datetime.now().year
        last_quote = (
            Quote.objects.filter(reference__contains=f"NF-Q-{year}")
            .order_by("reference")
            .last()
        )

        if last_quote:
            last_number = int(last_quote.reference.split("-")[-1])
            new_number = str(last_number + 1).zfill(5)
        else:
            new_number = "00001"

        validated_data["reference"] = f"NF-D-{year}-{new_number}"

        quote = Quote.objects.create(**validated_data)
        for item_data in line_items_data:
            LineItem.objects.create(quote=quote, **item_data)
        return quote

    def update(self, instance, validated_data):
        line_items_data = validated_data.pop("line_items", None)
        validated_data.pop("reference", None)  # Prevent reference from being updated

        instance.client = validated_data.get("client", instance.client)
        instance.valid_until = validated_data.get("valid_until", instance.valid_until)
        instance.save()

        if line_items_data is not None:
            instance.line_items.all().delete()  # Clear existing line items
            for item_data in line_items_data:
                LineItem.objects.create(quote=instance, **item_data)

        return instance


class InvoiceSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = ["id", "client", "date", "reference", "linked_quote", "line_items"]
        read_only_fields = ["date"]

    def create(self, validated_data):
        line_items_data = validated_data.pop("line_items", [])
        invoice = Invoice.objects.create(**validated_data)
        for item_data in line_items_data:
            LineItem.objects.create(invoice=invoice, **item_data)
        return invoice

    def update(self, instance, validated_data):
        line_items_data = validated_data.pop("line_items", None)

        instance.client = validated_data.get("client", instance.client)
        instance.reference = validated_data.get("reference", instance.reference)
        instance.linked_quote = validated_data.get(
            "linked_quote", instance.linked_quote
        )
        instance.save()

        if line_items_data is not None:
            instance.line_items.all().delete()  # Clear existing line items
            for item_data in line_items_data:
                LineItem.objects.create(invoice=instance, **item_data)

        return instance


class ClientSerializer(serializers.ModelSerializer):
    quotes = QuoteSerializer(many=True, read_only=True)
    invoices = InvoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            "siret",
            "created_at",
            "quotes",
            "invoices",
        ]
