from django.db import models
from account.models import CustomUser
from shop.models import Product


class State(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class District(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="districts")
    
    def __str__(self):
        return self.name
    
    
class Municipality(models.Model):
    name = models.CharField(max_length=200)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="municipalities")

    class Meta:
        verbose_name_plural = "Municipalities"
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)    
    products = models.ManyToManyField(Product, through="CartProduct", related_name="cart")
    
    def __str__(self):  
        return f"Cart for {self.user.email}"
    
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    #flag
    ordered = models.BooleanField(default=False)
    
    @property
    def get_total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.email}'s cart"


class DeliveryAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="delivery_adresses")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name="delivery_adresses")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name="delivery_adresses")
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True, related_name="delivery_adresses")
    local_address = models.TextField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.email}-> {self.state.name} -> {self.district.name} -> {self.municipality.name}"


PAYMENT_METHODS = [
    ('cod', 'Cash on Delivery'),
    ('khalti', 'Khalti'),
]


class Order(models.Model):
    product = models.OneToOneField(CartProduct, on_delete=models.CASCADE, related_name="order")
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.DO_NOTHING, null=True)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=50, default="cod")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.product.name} ordered by {self.delivery_address}"  


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_details = models.TextField(max_length=500)
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for {self.order.product.product.name} by {self.order.delivery_address.user.email}"
