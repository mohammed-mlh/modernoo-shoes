from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('F', 'Women'),
        ('U', 'Unisex'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.category.name}"
    
    @property
    def base_price(self):
        """Get the base price (lowest size price)"""
        sizes = self.product_sizes.all()
        if sizes.exists():
            return min(size.price for size in sizes)
        return 0
    
    @property
    def available_sizes(self):
        """Get all available sizes for this product"""
        return self.product_sizes.filter(is_available=True)

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7)  # e.g., #FF0000
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    
    def __str__(self):
        return f"{self.name} - {self.product.name}"

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sizes')
    size = models.CharField(max_length=10)  # Flexible size field (e.g., "39", "XL", "10.5")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['product', 'size']
        ordering = ['size']
    
    def __str__(self):
        return f"{self.product.name} - Size {self.size} - ${self.price}"

class Cart(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.session_id}"
    
    @property
    def total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_amount(self):
        """Get total amount of cart"""
        return sum(item.total_price for item in self.items.all())
    
    def get_or_create_cart_item(self, product, size, color=None):
        """Get existing cart item or create new one"""
        item, created = self.items.get_or_create(
            product=product,
            size=size,
            color=color,
            defaults={'quantity': 0}
        )
        return item

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['cart', 'product', 'size', 'color']
    
    def __str__(self):
        return f"{self.product.name} - Size {self.size} x{self.quantity}"
    
    @property
    def total_price(self):
        """Calculate total price for this item"""
        return self.quantity * self.price_per_unit
    
    def update_quantity(self, new_quantity):
        """Update quantity and recalculate price"""
        self.quantity = max(1, new_quantity)
        # Get the current price for this size
        try:
            product_size = self.product.product_sizes.get(size=self.size)
            self.price_per_unit = product_size.price
        except ProductSize.DoesNotExist:
            pass
        self.save()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)  # Direct size string
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order.order_id} - {self.product.name} x{self.quantity}"
