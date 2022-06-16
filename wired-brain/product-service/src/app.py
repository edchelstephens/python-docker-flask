from flask import Flask, jsonify, request
from db import db
from product import Product

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:password@db/products"
db.init_app(app)


@app.route("/")
def index():
    """App index, return all products.

    curl -v http://localhost:8000/
    """
    products = [product.json for product in Product.find_all()]
    return jsonify(products)


@app.route("/products")
def get_products():
    """Get products endpoint.

    curl -v http://localhost:8000/products
    """
    products = [product.json for product in Product.find_all()]
    return jsonify(products)


@app.route("/product/<int:id>")
def get_product(id):
    """Get product endpoint.

    curl -v http://localhost:8000/product/1
    """
    product = Product.find_by_id(id)
    if product:
        return jsonify(product.json)
    return "Product with id {} not found".format(id), 404


@app.route("/product", methods=["POST"])
def post_product():
    """Post a new product.

    curl --header "Content-Type: application/json" --request POST --data '{"name": "Product 3"}' -v http://localhost:8000/product
    """
    data = request.json
    product = Product(None, data["name"])
    product.save_to_db()

    return jsonify(product.json), 201


@app.route("/product/<int:id>", methods=["PUT"])
def put_product(id):
    """Update  product.

    curl --header "Content-Type: application/json" --request PUT --data '{"name": "Updated Product 2"}' -v http://localhost:8000/product/2
    """
    data = request.json
    product = Product.find_by_id(id)
    if product:
        product.name = data["name"]
        product.save_to_db()
        return jsonify(product), 200

    return "Product with id {} not found".format(id), 404


@app.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    """Delete product.

    curl --request DELETE -v http://localhost:8000/product/2
    """
    product = Product.find_by_id(id)
    if product:
        product.delete_from_db()
        response = {"message": "Product with id {} deleted".format(id)}
        return jsonify(response), 200

    return "Product with id {} not found".format(id), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
