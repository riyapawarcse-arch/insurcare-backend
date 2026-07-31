from flask import Blueprint
from controllers.customer_controller import (
    get_customers,
    get_customer,
    create_customer,
    edit_customer,
    remove_customer
)

customer_bp = Blueprint("customer", __name__)

# GET all customers
@customer_bp.route("/customers", methods=["GET"])
def customers():
    return get_customers()

# GET customer by ID
@customer_bp.route("/customers/<int:customer_id>", methods=["GET"])
def customer(customer_id):
    return get_customer(customer_id)

# POST customer
@customer_bp.route("/customers", methods=["POST"])
def add_customer():
    return create_customer()

# PUT customer
@customer_bp.route("/customers/<int:customer_id>", methods=["PUT"])
def update(customer_id):
    return edit_customer(customer_id)

# DELETE customer
@customer_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete(customer_id):
    return remove_customer(customer_id)
