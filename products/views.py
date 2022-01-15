from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Coupon

from .models import Message, Product, Order
from accounts.models import Testimony
from .forms import ProductForm
from .serializers import ProductSerializer, OrderSerializer, MessageSerializer

# Third party imports
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAdminUser


# Defining function that covers Permission
def prove_credentials(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


def index(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        phone = request.POST['phone']
        context = {
            "name": name,
            "email": email,
            "message": message,
            "phone": phone,
            "object": "Contact",
        }
        return render(request, 'home.html', context)
    else:
        testimonials = Testimony.objects.filter(approved=True)
        context = {'testimonials': testimonials}
        return render(request, 'index.html', context)


def home_products(request):
    products = Product.objects.filter(present=True).order_by('price')[:4]
    context = {'products': products, 'object': 'Products'}
    return render(request, 'products/products.html', context)


@prove_credentials(login_url='/admin/')
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()
        return render(request, 'products/product_form.html', {'form': form})


class ProductListView(ListView):
    model = Product
    template_name = 'products/all_products.html'
    context_object_name = 'products'
    ordering = ['name']

    # When you want to add extra context, override this function
    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context.update({'object': 'All Products'})
        return context


def order(request):
    if request.method == "POST":
        try:
            products = Product.objects.all()
            product = request.POST['product'].split(":")[0]
            phone = request.POST['phone']
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            code = request.POST['coupon']
            customer = None
            if request.user.is_authenticated:
                customer = request.user.customer

            context = {
                "product": product,
                "name": name,
                "email": email,
                "phone": phone,
                "message": message,
                "object": "Order",
                "products": products,
            }
            ordered_product = Product.objects.get(name=product)
            new_order = Order(product=ordered_product, name=name, phone=phone, email=email, message=message,
                              customer=customer)

            if code == "":
                new_order.save()
                return render(request, 'products/order.html', context)
            else:
                if request.user.is_authenticated and str(request.user.customer.code) == code:
                    try:
                        Coupon.objects.create(code=code, user=request.user.customer)
                        new_order.discount_approved = True
                        new_order.save()
                        request.user.customer.discount_used = True
                        request.user.customer.save()
                        messages.success(request, 'Your coupon was accepted. 5% discount applied')
                        return render(request, 'products/order.html', context)
                    except:
                        messages.warning(request, 'Your coupon was already used. Order is rejected.')
                        return redirect('city-optics')

                messages.warning(request, 'Your coupon code does not exist. Order is rejected.')
                return redirect('city-optics')

        except ObjectDoesNotExist:
            products = Product.objects.all()
            get_context = {"products": products, "object": "Unavailable Product - Check our Products"}
            return render(request, 'products/order.html', get_context)
    else:
        products = Product.objects.all()
        get_context = {"products": products, "object": "Order"}
        return render(request, 'products/order.html', get_context)


def get_message(request):
    if request.method != "POST":
        return render(request, 'index.html')
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    phone = request.POST['phone']
    context = {
        "name": name,
        "email": email,
        "message": message,
        "phone": phone,
        "object": "Contact",
    }
    new_message = Message(name=name, mail=email, phone=phone, text_message=message)
    new_message.save()
    return render(request, 'home.html', context)


def details(request, pk):
    try:
        product = Product.objects.get(id=pk)
        context = {'product': product, 'object': 'Details'}
        return render(request, 'products/product_details.html', context)
    except ObjectDoesNotExist:
        raise Http404


def order_specific(request, pk):
    specific_product = Product.objects.get(id=pk)
    context = {'specific_product': specific_product, 'object': 'Order'}
    return render(request, 'products/order.html', context)


def city_optics(request):
    if request.method == "POST":
        searched_item = request.POST["searcher"]
        search_result = Product.objects.search(searched_item)
        context = {'results': search_result, 'object': 'Search Results', 'searched_item': searched_item}
        return render(request, 'products/site_index.html', context)
    return render(request, 'products/site_index.html', {'object': 'City Optics Main'})


# API Views

class ProductAPIView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object():
        try:
            return Product.objects.filter(present=True).order_by('price')
        except Product.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request):
        queryset = self.get_object()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class OrderAPIView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object():
        try:
            return Order.objects.filter()
        except Order.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request):
        queryset = self.get_object()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageAPIView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object():
        try:
            return Message.objects.all()
        except Message.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request):
        queryset = self.get_object()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
