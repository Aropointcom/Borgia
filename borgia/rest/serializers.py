from users.models import User
from shops.models import Product, Shop
from sales.models import SaleProduct, Sale
from finances.models import Transfert, ExceptionnalMovement
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email', 'surname', 'family', 'balance', 'year', 'campus', 'phone']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'is_manual', 'manual_price', 'correcting_factor', 'is_active', 'is_removed', 'shop_id']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'description', 'color']


class SaleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = ['id', 'quantity', 'price', 'product_id', 'sale_id']


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'datetime', 'module_id', 'sender_id', 'shop_id']


class TransfertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfert
        fields = ['id', 'datetime', 'justification', 'amount', 'recipient_id', 'sender_id']


class ExceptionnalMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceptionnalMovement
        fields = ['id', 'datetime', 'justification', 'amount', 'is_credit', 'operator_id', 'recipient_id']