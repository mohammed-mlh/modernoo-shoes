from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Category, Product, ProductSize, Color

class Command(BaseCommand):
    help = 'Populate database with sample products, categories, sizes, and colors'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Creating sample data...')
            
            # Create categories
            categories_data = [
                {'name': 'Running', 'description': 'Performance footwear for runners'},
                {'name': 'Basketball', 'description': 'Court-ready basketball shoes'},
                {'name': 'Training', 'description': 'Gym & cross-training shoes'},
                {'name': 'Casual', 'description': 'Everyday comfortable shoes'},
                {'name': 'Boots', 'description': 'Durable & weather-ready boots'},
                {'name': 'Sandals', 'description': 'Open & comfortable sandals'},
            ]
            
            categories = {}
            for cat_data in categories_data:
                category, created = Category.objects.get_or_create(
                    name=cat_data['name'],
                    defaults={'description': cat_data['description']}
                )
                categories[cat_data['name']] = category
                if created:
                    self.stdout.write(f'Created category: {cat_data["name"]}')
            
            # Create products with different pricing for sizes
            products_data = [
                {
                    'name': 'Premium Running Shoes',
                    'description': 'Lightweight design with maximum cushioning',
                    'category': 'Running',
                    'video_url': 'https://videos.pexels.com/video-files/5896379/5896379-uhd_1440_2560_24fps.mp4',
                    'sizes_prices': {
                        '38': 124.99, '39': 129.99, '40': 134.99, '41': 139.99, '42': 144.99
                    },
                    'colors': [
                        {'name': 'Navy Blue', 'hex_code': '#2c3e50'},
                        {'name': 'Red', 'hex_code': '#e74c3c'},
                        {'name': 'White', 'hex_code': '#ecf0f1'},
                    ]
                },
                {
                    'name': 'Classic Leather Boots',
                    'description': 'Handcrafted premium leather boots',
                    'category': 'Boots',
                    'video_url': 'https://videos.pexels.com/video-files/10451732/10451732-hd_1440_2560_30fps.mp4',
                    'sizes_prices': {
                        '39': 184.99, '40': 189.99, '41': 194.99, '42': 199.99, '43': 204.99
                    },
                    'colors': [
                        {'name': 'Brown', 'hex_code': '#8B4513'},
                        {'name': 'Black', 'hex_code': '#000000'},
                        {'name': 'Sienna', 'hex_code': '#A0522D'},
                    ]
                },
                {
                    'name': 'Summer Sandals',
                    'description': 'Breathable and comfortable sandals',
                    'category': 'Sandals',
                    'video_url': 'https://videos.pexels.com/video-files/4448895/4448895-hd_1080_1920_30fps.mp4',
                    'sizes_prices': {
                        '36': 74.99, '37': 79.99, '38': 84.99, '39': 89.99
                    },
                    'colors': [
                        {'name': 'Blue', 'hex_code': '#3498db'},
                        {'name': 'Red', 'hex_code': '#e74c3c'},
                        {'name': 'Green', 'hex_code': '#2ecc71'},
                    ]
                },
                {
                    'name': 'Basketball Sneakers',
                    'description': 'High-performance court shoes',
                    'category': 'Basketball',
                    'video_url': 'https://videos.pexels.com/video-files/3201763/3201763-hd_1080_1920_30fps.mp4',
                    'sizes_prices': {
                        '40': 144.99, '41': 149.99, '42': 154.99, '43': 159.99
                    },
                    'colors': [
                        {'name': 'Black', 'hex_code': '#000000'},
                        {'name': 'Red', 'hex_code': '#c0392b'},
                    ]
                },
                {
                    'name': 'Training Shoes',
                    'description': 'Versatile gym footwear',
                    'category': 'Training',
                    'video_url': 'https://videos.pexels.com/video-files/4066283/4066283-hd_1080_1920_25fps.mp4',
                    'sizes_prices': {
                        '38': 104.99, '39': 109.99, '40': 114.99, '41': 119.99
                    },
                    'colors': [
                        {'name': 'Teal', 'hex_code': '#16a085'},
                        {'name': 'Navy', 'hex_code': '#2c3e50'},
                    ]
                },
                {
                    'name': 'Casual Loafers',
                    'description': 'Comfortable everyday wear',
                    'category': 'Casual',
                    'video_url': 'https://videos.pexels.com/video-files/3196478/3196478-hd_1080_1920_25fps.mp4',
                    'sizes_prices': {
                        '39': 114.99, '40': 119.99, '41': 124.99, '42': 129.99
                    },
                    'colors': [
                        {'name': 'Brown', 'hex_code': '#8B4513'},
                        {'name': 'Black', 'hex_code': '#000000'},
                    ]
                },
            ]
            
            for product_data in products_data:
                # Create product
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'description': product_data['description'],
                        'category': categories[product_data['category']],
                        'video_url': product_data['video_url']
                    }
                )
                
                if created:
                    self.stdout.write(f'Created product: {product_data["name"]}')
                
                # Create product sizes with different prices
                for size_str, price in product_data['sizes_prices'].items():
                    product_size, created = ProductSize.objects.get_or_create(
                        product=product,
                        size=size_str,
                        defaults={
                            'price': price,
                            'stock_quantity': 10,
                            'is_available': True
                        }
                    )
                    if created:
                        self.stdout.write(f'  - Size {size_str}: ${price}')
                
                # Create colors
                for color_data in product_data['colors']:
                    color, created = Color.objects.get_or_create(
                        name=color_data['name'],
                        product=product,
                        defaults={'hex_code': color_data['hex_code']}
                    )
                    if created:
                        self.stdout.write(f'  - Color: {color_data["name"]}')
            
            self.stdout.write(
                self.style.SUCCESS('Successfully populated database with sample data!')
            ) 