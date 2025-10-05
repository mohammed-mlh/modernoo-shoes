# Modernoo Shoes - E-commerce Platform

A modern Django-based e-commerce platform for shoes with dynamic pricing based on sizes and categories.

## Features

- **Dynamic Pricing**: Each size has its own price
- **Category Management**: Organize products by categories
- **Color Options**: Multiple color choices per product
- **Video Product Showcase**: Full-screen video presentations
- **Responsive Design**: Mobile-first approach
- **Order Management**: Complete order tracking system

## Models Structure

### Core Models

#### Category
- `name`: Category name (e.g., "Running", "Basketball")
- `description`: Category description
- `image`: Optional category image
- `is_active`: Whether the category is active
- `created_at`, `updated_at`: Timestamps

#### Product
- `name`: Product name
- `description`: Product description
- `category`: ForeignKey to Category
- `gender`: Choices (Men, Women, Unisex)
- `video_url`: URL for product video
- `image`: Optional product image
- `is_active`: Whether the product is active
- `created_at`, `updated_at`: Timestamps

#### Size
- `size`: Size number (36-46)
- Predefined size choices

#### ProductSize
- `product`: ForeignKey to Product
- `size`: ForeignKey to Size
- `price`: Decimal field for size-specific pricing
- `stock_quantity`: Available stock
- `is_available`: Whether this size is available

#### Color
- `name`: Color name (e.g., "Navy Blue")
- `hex_code`: Color hex code (e.g., "#2c3e50")
- `product`: ForeignKey to Product

#### Order
- `order_id`: UUID for unique order identification
- `customer_name`: Customer's full name
- `phone_number`: Contact phone
- `city`: Customer's city
- `address`: Full address
- `total_amount`: Order total
- `status`: Order status (pending, confirmed, shipped, delivered, cancelled)
- `created_at`, `updated_at`: Timestamps

#### OrderItem
- `order`: ForeignKey to Order
- `product`: ForeignKey to Product
- `size`: ForeignKey to Size
- `color`: Optional ForeignKey to Color
- `quantity`: Number of items
- `price_per_unit`: Price per unit
- `total_price`: Total price for this item

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Populate Sample Data
```bash
python manage.py populate_sample_data
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## Dynamic Pricing System

The system implements size-based pricing where each size can have a different price:

### Example Pricing Structure
```python
# Premium Running Shoes
'sizes_prices': {
    '38': 124.99,
    '39': 129.99,
    '40': 134.99,
    '41': 139.99,
    '42': 144.99
}

# Classic Leather Boots
'sizes_prices': {
    '39': 184.99,
    '40': 189.99,
    '41': 194.99,
    '42': 199.99,
    '43': 204.99
}
```

### Price Calculation
- Base price is automatically calculated as the lowest available size price
- When a user selects a different size, the price updates dynamically
- Quantity changes also update the total price in real-time

## Admin Interface

The Django admin interface provides comprehensive management for:

- **Categories**: Create and manage product categories
- **Products**: Add products with videos, descriptions, and categories
- **Product Sizes**: Set individual prices for each size
- **Colors**: Manage color options for each product
- **Orders**: Track order status and customer information
- **Order Items**: View detailed order breakdowns

## API Endpoints

### Create Order
```
POST /api/create-order/
```
Creates a new order with customer information and product details.

### Get Product Sizes
```
GET /api/product/<product_id>/sizes/
```
Returns available sizes and prices for a specific product.

## Frontend Features

### Home Page (`/`)
- Displays all products in a scrollable video format
- Dynamic size selection with price updates
- Color selection
- Quantity controls
- Purchase modal with customer information form

### Category Page (`/category/`)
- Shows products filtered by category
- Same interactive features as home page
- Category-specific product listings

### Interactive Elements
- **Size Selection**: Click to select size, price updates automatically
- **Color Selection**: Click to select color
- **Quantity Controls**: +/- buttons and direct input
- **Real-time Price Updates**: Price changes based on size and quantity
- **Purchase Flow**: Modal form for customer information

## Database Relationships

```
Category (1) ←→ (N) Product
Product (1) ←→ (N) ProductSize
Product (1) ←→ (N) Color
Size (1) ←→ (N) ProductSize
Order (1) ←→ (N) OrderItem
Product (1) ←→ (N) OrderItem
```

## Customization

### Adding New Products
1. Go to Django Admin → Products
2. Create a new product with name, description, category, and video URL
3. Add ProductSize entries for each available size with specific prices
4. Add Color entries for available color options

### Modifying Prices
1. Go to Django Admin → Product Sizes
2. Find the product and size combination
3. Update the price field
4. Save changes

### Adding New Categories
1. Go to Django Admin → Categories
2. Create a new category with name and description
3. Assign products to the new category

## File Structure

```
modernoo-shoes/
├── core/
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── admin.py           # Admin interface
│   ├── urls.py            # URL routing
│   ├── management/        # Management commands
│   └── templates/core/    # HTML templates
├── cms/                   # Django settings
├── requirements.txt       # Python dependencies
└── manage.py             # Django management
```

## Technologies Used

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Video**: HTML5 Video API
- **Admin**: Django Admin Interface

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 