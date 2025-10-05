from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Category, Product, ProductSize, Color, Cart, CartItem, Order, OrderItem

def home(request):
    # Get categories from database
    categories = Category.objects.filter(is_active=True)
    
    # If no categories exist, create some default ones
    if not categories.exists():
        default_categories = [
            {'name': 'Sneakers', 'description': 'Casual & athletic footwear'},
            {'name': 'Sandals', 'description': 'Open & comfortable designs'},
            {'name': 'Boots', 'description': 'Durable & weather-ready'},
            {'name': 'Running', 'description': 'Performance footwear'},
            {'name': 'Basketball', 'description': 'Court-ready shoes'},
            {'name': 'Training', 'description': 'Gym & cross-training'},
            {'name': 'Skateboarding', 'description': 'Durable board shoes'},
            {'name': 'Flip Flops', 'description': 'Easy summer wear'},
            {'name': 'Hiking', 'description': 'Trail-ready footwear'},
            {'name': 'Lifestyle', 'description': 'Fashion-forward designs'},
            {'name': 'Beachwear', 'description': 'Water-friendly options'},
            {'name': 'Winter', 'description': 'Cold weather protection'},
        ]
        
        for cat_data in default_categories:
            Category.objects.create(
                name=cat_data['name'],
                description=cat_data['description']
            )
        
        categories = Category.objects.filter(is_active=True)
    
    # Create shoe_items for the grid layout
    shoe_items = []
    for category in categories:
        # Get product count for this category
        product_count = Product.objects.filter(category=category, is_active=True).count()
        
        # Define image URLs for each category
        image_urls = {
            'Sneakers': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
            'Sandals': 'https://images.pexels.com/photos/40737/sandals-flip-flops-footwear-beach-40737.jpeg',
            'Boots': 'https://images.pexels.com/photos/267309/pexels-photo-267309.jpeg',
            'Running': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
            'Basketball': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
            'Training': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
            'Skateboarding': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
            'Flip Flops': 'https://images.pexels.com/photos/40737/sandals-flip-flops-footwear-beach-40737.jpeg',
            'Hiking': 'https://images.pexels.com/photos/267309/pexels-photo-267309.jpeg',
            'Lifestyle': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
            'Beachwear': 'https://images.pexels.com/photos/40737/sandals-flip-flops-footwear-beach-40737.jpeg',
            'Winter': 'https://images.pexels.com/photos/267309/pexels-photo-267309.jpeg',
        }
        
        shoe_items.append({
            'name': category.name,
            'image_url': category.image.url if category.image else image_urls.get(category.name, 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg'),
            'count': product_count if product_count > 0 else 'New',
            'category_id': category.id
        })
    
    # If no items, provide fallback data
    if not shoe_items:
        shoe_items = [
            {
                'name': 'Sneakers',
                'image_url': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
                'count': 'New',
                'category_id': None
            },
            {
                'name': 'Sandals',
                'image_url': 'https://images.pexels.com/photos/40737/sandals-flip-flops-footwear-beach-40737.jpeg',
                'count': 'New',
                'category_id': None
            },
            {
                'name': 'Boots',
                'image_url': 'https://images.pexels.com/photos/267309/pexels-photo-267309.jpeg',
                'count': 'New',
                'category_id': None
            },
            {
                'name': 'Running',
                'image_url': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
                'count': 'New',
                'category_id': None
            },
            {
                'name': 'Basketball',
                'image_url': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
                'count': 'New',
                'category_id': None
            },
            {
                'name': 'Training',
                'image_url': 'https://images.pexels.com/photos/112285/pexels-photo-112285.jpeg',
                'count': 'New',
                'category_id': None
            }
        ]
    
    # Get cart for cart count
    cart = get_or_create_cart(request)
    
    context = {
        'categories': categories,
        'featured_categories': categories[:3],  # First 3 as featured
        'products': Product.objects.filter(is_active=True).prefetch_related(
            'product_sizes',
            'colors',
            'category'
        ),
        'shoe_items': shoe_items,
        'cart': cart
    }
    return render(request, "core/home.html", context)

def category_page(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    cart = get_or_create_cart(request)
    context = {
        'category': category,
        'products': products,
        'cart': cart
    }
    return render(request, 'core/category_page.html', context)

def cart_view(request):
    cart = get_or_create_cart(request)
    context = {'cart': cart, 'cart_items': cart.items.select_related('product', 'color').all()}
    return render(request, 'core/cart.html', context)

def checkout_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product', 'color').all()
    
    if not cart_items:
        return redirect('cart')
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'core/checkout.html', context)

def get_or_create_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        size = data.get('size')
        color_id = data.get('color_id')
        quantity = int(data.get('quantity', 1))
        
        if not product_id or not size:
            return JsonResponse({'success': False, 'error': 'Product ID and size are required'})
        
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color_id=color_id if color_id else None,
            defaults={'quantity': quantity, 'price_per_unit': product.base_price}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'cart_total': str(cart.total_amount)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def update_cart_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'})
        
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = quantity
        cart_item.save()
        
        cart = cart_item.cart
        
        return JsonResponse({
            'success': True,
            'item_total': str(cart_item.total_price),
            'cart_total': str(cart.total_amount),
            'cart_count': cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'cart_total': str(cart.total_amount),
            'cart_count': cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        
        # Get customer details
        customer_name = data.get('customer_name')
        customer_phone = data.get('customer_phone')
        customer_city = data.get('customer_city')
        customer_address = data.get('customer_address')
        
        if not all([customer_name, customer_phone, customer_city, customer_address]):
            return JsonResponse({'success': False, 'error': 'All customer details are required'})
        
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        
        if not cart_items:
            return JsonResponse({'success': False, 'error': 'Cart is empty'})
        
        # Create order
        order = Order.objects.create(
            customer_name=customer_name,
            phone_number=customer_phone,
            city=customer_city,
            address=customer_address,
            total_amount=cart.total_amount
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                size=cart_item.size,
                color=cart_item.color,
                quantity=cart_item.quantity,
                price_per_unit=cart_item.price_per_unit,
                total_price=cart_item.total_price
            )
        
        # Clear the cart
        cart_items.delete()
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'message': 'Order placed successfully!'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["GET"])
def get_product_sizes(request):
    try:
        product_id = request.GET.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'})
        
        product = get_object_or_404(Product, id=product_id)
        sizes = ProductSize.objects.filter(product=product)
        
        size_data = []
        for size in sizes:
            size_data.append({
                'size': size.size,
                'price': str(size.price)
            })
        
        return JsonResponse({'success': True, 'sizes': size_data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})