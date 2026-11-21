# GretKart – E-Commerce Platform

**GretKart** is a modern Django-based e-commerce web application designed to provide users with a convenient and user-friendly online shopping experience.

The platform allows customers to explore different product categories, view product details, add products to their shopping cart, manage their wishlist, and proceed with the checkout process.

## Project Overview

GretKart is developed using Django and modern frontend technologies. It combines a responsive shopping interface with a Python-based backend and SQLite database to manage products, users, categories, carts, and orders.

The main goal is to develop a structured and user-friendly online shopping platform.

## Key Features

- Modern and responsive e-commerce interface
- User registration and authentication
- User login and logout functionality
- Product listing and product details
- Product category management
- Shopping cart functionality
- Add and remove products from the cart
- Wishlist functionality
- Checkout system
- Order management
- Django Admin Panel for managing application data
- Static files and media management

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| HTML5 | Web page structure |
| CSS3 | Styling and layout |
| JavaScript | Frontend interactions |
| Bootstrap | Responsive UI components |
| jQuery | Frontend functionality |
| SQLite | Database |
| Git & GitHub | Version control |

## Project Structure

```text
great-django/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── admin.py
│
├── carts/
│
├── category/
│   ├── models.py
│   ├── views.py
│   └── admin.py
│
├── orders/
│
├── store/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── gretkart/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── fonts/
│
├── templates/
│   ├── includes/
│   ├── store/
│   ├── base.html
│   └── home.html
│
├── manage.py
└── README.md
```

## Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/patidarharshita361-bit/great-django.git
```

### 2. Navigate to the Project Directory

```bash
cd great-django
```

### 3. Create a Virtual Environment

```bash
python -m venv env
```

### 4. Activate the Virtual Environment (Windows)

```powershell
.\env\Scripts\Activate.ps1
```

### 5. Install Django

```bash
pip install django
```

Install any additional dependencies required by the application.

### 6. Configure Django Secret Key

Set the Django secret key as an environment variable.

For Windows PowerShell:

```powershell
$env:DJANGO_SECRET_KEY="your-secret-key"
```

### 7. Apply Database Migrations

```bash
python manage.py migrate
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## Project Goals

- Develop a complete and user-friendly e-commerce website.
- Provide an organized product browsing experience.
- Implement product category management.
- Build user authentication and account management.
- Provide shopping cart and wishlist functionality.
- Implement checkout and order management.
- Improve backend development skills using Django.
- Develop a maintainable and scalable web application.

## GitHub Repository

**Project Link:**  
https://github.com/patidarharshita361-bit/great-django

## Developer

**Harshita Patidar**

B.Tech – Computer Science Engineering

GitHub: [@patidarharshita361-bit](https://github.com/patidarharshita361-bit)

## Project Status

Currently under development. New improvements and features are being added to enhance the shopping experience.

---

 Thank you for visiting GretKart!