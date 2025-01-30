from django.db import models



class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=150)
    
    class Meta:
        verbose_name_plural="Categories"
    
    
    def __str__(self):
        return self.name
    


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="products")
    
    def __str__(self):
        return self.name
    



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')

    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.image.name
    
    
    