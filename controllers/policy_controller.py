from flask import request, jsonify
from services.policy_service import (
    get_all_policies,
    get_policy_by_id,
    create_policy,
    update_policy,
    delete_policy
)

def get_policies():
    policies = get_all_policies()
    return jsonify({"success": True, "data": policies}), 200

def get_policy(policy_id):
    policy = get_policy_by_id(policy_id)
    if not policy:
        return jsonify({"success": False, "message": "Policy not found"}), 404
    return jsonify({"success": True, "data": policy}), 200

def add_policy():
    data = request.get_json()
    
    required_fields = ['policy_number', 'policy_type', 'premium_amount', 'coverage_amount', 'customer_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing field: {field}"}), 400

    policy, error = create_policy(data)
    if error:
        return jsonify({"success": False, "message": error}), 400

    return jsonify({"success": True, "data": policy, "message": "Policy created successfully"}), 201

def edit_policy(policy_id):
    data = request.get_json()
    policy, error = update_policy(policy_id, data)
    if error:
        return jsonify({"success": False, "message": error}), 404
    return jsonify({"success": True, "data": policy, "message": "Policy updated successfully"}), 200

def remove_policy(policy_id):
    success = delete_policy(policy_id)
    if not success:
        return jsonify({"success": False, "message": "Policy not found"}), 404
    return jsonify({"success": True, "message": "Policy deleted successfully"}), 200
