from django.db import models
from django.db.models import Q
from PIL import Image


class ProductManager(models.Manager):

    def search(self, query):
        if query is None or query == "":
            return self.get_queryset().none()
        lookups = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = self.filter(lookups)
        return queryset


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField()
    present = models.BooleanField(default=False)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='products_pics')

    # Don`t forget enctype='multipart/form-data' in your form tag for upload of image!!

    def __str__(self):
        return f"{self.name}: ${self.price}"

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 1000 or img.width > 800:
            output_size = (800, 1000)
            img.thumbnail(output_size)
            img.save()

    def get_absolute_url(self):
        return f"/product/{self.id}"

    objects = ProductManager()


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=33)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True, max_length=555)
    is_shipped = models.BooleanField(default=False)
    discount_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product}"


class Message(models.Model):
    name = models.CharField(max_length=50)
    mail = models.EmailField()
    phone = models.CharField(max_length=33, blank=True, null=True)
    text_message = models.TextField(max_length=555)
    is_for_front_page = models.BooleanField(default=False)
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} wrote on {self.sent_on}"
