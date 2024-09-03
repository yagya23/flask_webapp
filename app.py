from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# In-memory product list
products = [
    {"id": 1, "title": "Laptop", "price": 1200, "description": "A powerful laptop", "category": "electronics"},
    {"id": 2, "title": "Headphones", "price": 100, "description": "Noise-cancelling headphones", "category": "electronics"}
]

# Helper function to find a product by ID
def find_product(product_id):
    return next((product for product in products if product["id"] == product_id), None)

# 1. GET all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

# 2. GET a product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = find_product(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

# 3. POST - Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    new_product = request.json
    new_product["id"] = max([product["id"] for product in products]) + 1 if products else 1
    products.append(new_product)
    return jsonify(new_product), 201

# 4. PUT - Update a product by ID
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = find_product(product_id)
    if product:
        data = request.json
        product.update(data)
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

# 5. DELETE - Delete a product by ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = find_product(product_id)
    if product:
        products.remove(product)
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404

# Serve the frontend HTML file
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
