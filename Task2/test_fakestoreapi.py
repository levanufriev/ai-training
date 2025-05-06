import requests
import pytest

# API endpoint
API_URL = "https://fakestoreapi.com/products"

def test_api_response_code():
    """Verify server response code is 200"""
    response = requests.get(API_URL)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def test_products_data_structure():
    """Verify the basic structure of the products data"""
    response = requests.get(API_URL)
    products = response.json()
    
    assert isinstance(products, list), "Expected a list of products"
    assert len(products) > 0, "Expected at least one product in the response"
    
    # Check each product has the required fields
    required_fields = ['id', 'title', 'price', 'description', 'category', 'image', 'rating']
    for product in products:
        for field in required_fields:
            assert field in product, f"Missing required field: {field} in product {product.get('id', 'unknown')}"

def test_product_attributes():
    """Verify specific attributes of each product"""
    response = requests.get(API_URL)
    products = response.json()
    defective_products = []
    
    for product in products:
        defects = []
        
        # Check title is not empty
        if not product.get('title', '').strip():
            defects.append("Empty title")
        
        # Check price is not negative
        if 'price' in product and product['price'] < 0:
            defects.append(f"Negative price: {product['price']}")
        
        # Check rating.rate doesn't exceed 5
        rating = product.get('rating', {})
        if 'rate' in rating and rating['rate'] > 5:
            defects.append(f"Rating exceeds 5: {rating['rate']}")
        
        if defects:
            defective_products.append({
                'product_id': product.get('id', 'unknown'),
                'defects': defects,
                'product_data': product
            })
    
    # Print defective products for visibility
    if defective_products:
        print("\nDefective Products Found:")
        for defective in defective_products:
            print(f"\nProduct ID: {defective['product_id']}")
            for defect in defective['defects']:
                print(f"- {defect}")
    
    # Assert no defective products found (or customize as needed)
    assert not defective_products, f"Found {len(defective_products)} defective products"