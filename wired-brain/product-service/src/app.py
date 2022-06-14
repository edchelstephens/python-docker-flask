from flask import Flask, jsonify, request


products = [
    {
        "id": 1,
        "name": "Product 1",
    },
    {
        "id": 2,
        "name": "Product 2",
    },
]

app = Flask(__name__)


@app.route("/products")
def get_products():
    """Get products endpoint.

    curl -v http://localhost:5000/products
    """
    return jsonify(products)


@app.route("/product/<int:id>")
def get_product(id):
    """Get product endpoint.

    curl -v http://localhost:5000/product/1
    """
    product_list = [product for product in products if product["id"] == id]
    if len(product_list) == 0:
        return "Product with id {} not found".format(id), 404
    return product_list[0]


@app.route("/product", methods=["POST"])
def post_product():
    """Post a new product.

    curl --header "Content-Type: application/json" --request POST --data '{"name": "Product 3"}' -v http://localhost:5000/product
    """
    data = request.json
    new_id = max([product["id"] for product in products]) + 1

    new_product = {"id": new_id, "name": data["name"]}

    products.append(new_product)

    return jsonify(new_product), 201


@app.route("/product/<int:id>", methods=["PUT"])
def put_product(id):
    """Update  product.

    curl --header "Content-Type: application/json" --request PUT --data '{"name": "Updated Product 2"}' -v http://localhost:5000/product/2
    """
    data = request.json
    for product in products:
        if product["id"] == id:
            product["name"] = data["name"]
            return jsonify(product), 201

    return "Product with id {} not found".format(id), 404


@app.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    """Delete product.

    curl --request DELETE -v http://localhost:5000/product/2
    """
    product_list = [product for product in products if product["id"] == id]
    if len(product_list) == 1:
        products.remove(product_list[0])
        return "Product with id {} deleted".format(id), 200

    return "Product with id {} not found".format(id), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
