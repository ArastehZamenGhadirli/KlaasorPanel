from rest_framework import serializers
from .models import Invoice, Payment, OfflinePaymentDetail


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['user', 'title', 'amount', 'description', 'is_paid', 'created_at']
        read_only_fields = [ 'created_at', 'is_paid', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [ 'user', 'invoice', 'amount', 'method', 'is_verified', 'created_at']
        read_only_fields = ['created_at', 'is_verified', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OfflinePaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflinePaymentDetail
        fields = [ 'payment', 'tracking_code', 'receipt_image']



