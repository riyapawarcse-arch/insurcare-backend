from flask import jsonify, request

from services.customer_service import (
    get_all_customers,
    get_customer_by_id,
    add_customer,
    update_customer,
    delete_customer
)


def get_customers():
    customers = get_all_customers()
    return jsonify([customer.to_dict() for customer in customers])


def get_customer(customer_id):
    customer = get_customer_by_id(customer_id)

    if customer:
        return jsonify(customer.to_dict())

    return jsonify({"message": "Customer not found"}), 404


def create_customer():
    data = request.get_json()

    customer = add_customer(data)

    return jsonify(customer.to_dict()), 201


def edit_customer(customer_id):
    data = request.get_json()

    customer = update_customer(customer_id, data)

    if customer:
        return jsonify(customer.to_dict())

    return jsonify({"message": "Customer not found"}), 404


def remove_customer(customer_id):
    deleted = delete_customer(customer_id)

    if deleted:
        return jsonify({"message": "Customer deleted successfully"})

    return jsonify({"message": "Customer not found"}), 404


