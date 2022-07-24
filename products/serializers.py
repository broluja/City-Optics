from .models import Order, Product, Message, Reply

# Third party import
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product_name')
    customer = serializers.SerializerMethodField('get_customer_name')

    class Meta:
        model = Order
        fields = ['customer', 'phone', 'is_shipped', 'message', 'discount_approved', 'product']

    @staticmethod
    def get_product_name(order):
        product = order.product.name
        price = order.product.price
        response = product + ' $' + str(price)
        return response

    @staticmethod
    def get_customer_name(order):
        customer = order.customer.user
        response = f"Customer`s name: {customer}"
        return response


class MessageSerializer(serializers.ModelSerializer):
    sent_on = serializers.SerializerMethodField('get_clear_date')

    class Meta:
        model = Message
        fields = ('id', 'name', 'mail', 'phone', 'text_message', 'sent_on')

    @staticmethod
    def get_clear_date(message):
        date = message.sent_on
        clean_date = date.strftime("%d/%m/%Y at %H:%Mh")
        return clean_date


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = '__all__'
