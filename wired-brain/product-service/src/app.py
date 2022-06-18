import logging, logging.config
import configparser

from flask import Flask, jsonify, request
from sqlalchemy import exc as AlchemyExceptions

from db import db
from product import Product

logging.config.fileConfig("/config/logging.ini", disable_existing_loggers=False)
log = logging.getLogger(__name__)


def get_database_url() -> str:
    """Get database url string."""
    config = configparser.ConfigParser()
    config.read("/config/db.ini")

    database_config = config["mysql"]

    host = database_config["host"]
    username = database_config["username"]
    database = database_config["database"]

    with open("/run/secrets/db_password") as db_password_file:
        password = db_password_file.read()

    database_url = f"mysql://{username}:{password}@{host}/{database}"
    log.info(f"Connecting to database: {database_url}")

    return database_url


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_url()
db.init_app(app)


@app.route("/")
def index():
    """App index, return all products.

    curl -v http://localhost:8000/
    """
    try:
        log.debug("GET /products")
        products = [product.json for product in Product.find_all()]
        return jsonify(products)
    except AlchemyExceptions.SQLAlchemyError:
        message = "An exception has occured while retrieving products"
        log.exception(message)
        return message, 500


@app.route("/products")
def get_products():
    """Get products endpoint.

    curl -v http://localhost:8000/products
    """
    try:
        log.debug("GET /products")
        products = [product.json for product in Product.find_all()]
        return jsonify(products)
    except AlchemyExceptions.SQLAlchemyError:
        message = "An exception has occured while retrieving products"
        log.exception(message)
        return message, 500


@app.route("/product/<int:id>")
def get_product(id):
    """Get product endpoint.

    curl -v http://localhost:8000/product/1
    """
    try:
        log.debug("GET /product/{}".format(id))
        product = Product.find_by_id(id)
        if product:
            return jsonify(product.json)
        log.warngin("GET /production/{}: Product not found".format(id))
        return "Product with id {} not found".format(id), 404
    except AlchemyExceptions.SQLAlchemyError:
        message = "An exception has occured while retrieving product {}".format(id)
        log.exception(message)
        return message, 500


@app.route("/product", methods=["POST"])
def post_product():
    """Post a new product.

    curl --header "Content-Type: application/json" --request POST --data '{"name": "Product 3"}' -v http://localhost:8000/product
    """
    try:
        data = request.json
        log.debug("POST /product with product:{}".format(data))
        product = Product(None, data["name"])
        product.save_to_db()

        return jsonify(product.json), 201
    except AlchemyExceptions.SQLAlchemyError:
        message = "An exception has occured while creating product {}".format(
            product.name
        )
        log.exception(message)
        return message, 500


@app.route("/product/<int:id>", methods=["PUT"])
def put_product(id):
    """Update  product.

    curl --header "Content-Type: application/json" --request PUT --data '{"name": "Updated Product 2"}' -v http://localhost:8000/product/2
    """
    try:
        log.debug("PUT /product/{}".format(id))
        data = request.json
        product = Product.find_by_id(id)
        if product:
            product.name = data["name"]
            product.save_to_db()
            return jsonify(product.json), 200

        log.warning("PUT /product/{}: Product not found".format(id))
        return "Product with id {} not found".format(id), 404
    except AlchemyExceptions.SQLAlchemyError:
        message = "An exception has occured while trying to update product with product name: {}".format(
            product.name
        )
        log.exception(message)
        return message, 500


@app.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    """Delete product.

    curl --request DELETE -v http://localhost:8000/product/2
    """
    try:
        log.debug("DELETE /product/{}".format(id))
        product = Product.find_by_id(id)
        if product:
            product.delete_from_db()
            response = {"message": "Product with id {} deleted".format(id)}
            return jsonify(response), 200

        log.warning("DELETE /product/{}: Product not found".format(id))
        return "Product with id {} not found".format(id), 404
    except AlchemyExceptions.SQLAlchemyError:
        message = "An exception has occured while trying to delete product {}".format(
            id
        )
        log.exception(message)
        return message, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
