from flask import request, jsonify
from services.premium_service import (
    get_all_payments,
    record_payment,
    get_payments_by_policy
)

def fetch_payments():
    payments = get_all_payments()
    return jsonify(payments), 200

def add_payment():
    data = request.get_json()
    if not data or not data.get('policy_id') or not data.get('amount'):
        return jsonify({"message": "policy_id and amount are required"}), 400

    payment, error = record_payment(data)
    if error:
        return jsonify({"message": error}), 400

    return jsonify({"message": "Payment recorded successfully", "payment": payment}), 201

def fetch_by_policy(policy_id):
    payments = get_payments_by_policy(policy_id)
    return jsonify(payments), 200
