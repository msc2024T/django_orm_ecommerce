from django.db import models
from django.contrib.postgres.fields import ArrayField


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return f" name:{self.name} email: {self.email}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"product name : {self.name}"


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderItems')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orderItems')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f'order item id: #{self.id} order id: #{self.order.id} product name: {self.product.name}'


class Review(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='review')
    Customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='review')
    data = models.JSONField()

    def __str__(self):

        return f' review #{self.id} about {self.product.name} from {Customer.name}'


class Tag(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="tags")
    keywords = ArrayField(models.CharField(max_length=50))
