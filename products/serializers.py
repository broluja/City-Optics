from .models import Order, Product, Message, Reply

# Third party import
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product_name')

    class Meta:
        model = Order
        fields = ['customer', 'phone', 'is_shipped', 'message', 'discount_approved', 'product']

    @staticmethod
    def get_product_name(order):
        product = order.product.name
        price = order.product.price
        response = product + ' $' + str(price)
        return response


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = '__all__'
