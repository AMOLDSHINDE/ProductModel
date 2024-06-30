# Product Management API

This is a Django-based project for managing products, including creating new products and searching for existing products. The project includes a simple RESTful API to perform these operations.

## Features

- Create a new product
- Search for products by name
- Store product data in a JSON file (dummy_data.json)

## Requirements

- Python 3.7+
- Django 3.2+
- Django REST framework

## Setup

1. *Clone the repository:*

    sh
    git clone https://github.com/AMOLDSHINDE/ProductModel.git
    cd product-management-api
    

2. *Create a virtual environment:*

    sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    

3. *Install the dependencies:*

    sh
    pip install -r requirements.txt
    

4. *Run database migrations:*

    sh
    python manage.py migrate
    

5. *Create a superuser (optional, for admin access):*

    sh
    python manage.py createsuperuser
    

6. *Run the development server:*

    sh
    python manage.py runserver
    

## Usage

### Creating a Product

Send a POST request to /create_product/ with the product data in JSON format.

- *URL:* /create_product/
- *Method:* POST
- *Payload Example:*

    json
    {
        "name": "Test Product",
        "price": 100,
        "retailer_name": "Test Retailer"
    }
    

### Searching for Products

Send a GET request to /search_product/<name>/ with the product name as a URL parameter.

- *URL:* /search_product/<name>/
- *Method:* GET
- *Response Example:*

    json
    [
        {
            "name": "Test Product",
            "price": 100,
            "retailer_name": "Test Retailer"
        }
    ]
    

## Running Tests

To run the test suite, execute the following command:

```sh
python manage.py test
