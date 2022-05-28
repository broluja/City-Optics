from django.db import models
from django.db.models import Q
from accounts.models import Customer


class ProductManager(models.Manager):

    def search(self, query):
        if query is None or query == "":
            return self.get_queryset().none()
        lookups = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = self.filter(lookups)
        return queryset


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    present = models.BooleanField(default=False)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='products_pics')

    # Don`t forget enctype='multipart/form-data' in your form tag for upload of image!!

    def __str__(self):
        return f"{self.name}: ${self.price}"

    def get_absolute_url(self):
        return f"/products/product-detail/{self.id}"

    objects = ProductManager()


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=33)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True, max_length=555)
    is_shipped = models.BooleanField(default=False)
    discount_approved = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    objects = models.Manager()

    def __str__(self):
        return f"{self.product}"

    def new_price(self):
        if self.discount_approved:
            new_price = self.product.price * 0.95
            return new_price
        return self.product.price


class Message(models.Model):
    name = models.CharField(max_length=50)
    mail = models.EmailField()
    phone = models.CharField(max_length=33, blank=True, null=True)
    text_message = models.TextField(max_length=555)
    sent_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name} wrote on {self.sent_on.strftime("%A, %d. %B %Y %I:%M%p")}'


class Reply(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reply')
    title = models.CharField(max_length=99, blank=True, null=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


