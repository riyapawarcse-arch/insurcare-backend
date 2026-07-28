from flask import request, jsonify
from services.claim_service import (
    get_all_claims,
    get_claim_by_id,
    create_claim,
    update_claim_status,
    delete_claim
)

def get_claims():
    claims = get_all_claims()
    return jsonify(claims), 200

def get_claim(claim_id):
    claim = get_claim_by_id(claim_id)
    if not claim:
        return jsonify({"message": "Claim not found"}), 404
    return jsonify(claim), 200

def add_claim():
    data = request.get_json()
    if not data or not data.get('policy_id') or not data.get('claim_amount') or not data.get('reason'):
        return jsonify({"message": "policy_id, claim_amount, and reason are required"}), 400

    claim, error = create_claim(data)
    if error:
        return jsonify({"message": error}), 400

    return jsonify({"message": "Claim submitted successfully", "claim": claim}), 201

def modify_claim_status(claim_id):
    data = request.get_json()
    status = data.get('status')
    if not status or status not in ['Pending', 'Approved', 'Rejected']:
        return jsonify({"message": "Valid status (Pending, Approved, Rejected) is required"}), 400

    claim, error = update_claim_status(claim_id, status)
    if error:
        return jsonify({"message": error}), 404

    return jsonify({"message": f"Claim status updated to {status}", "claim": claim}), 200

def remove_claim(claim_id):
    success = delete_claim(claim_id)
    if not success:
        return jsonify({"message": "Claim not found"}), 404
    return jsonify({"message": "Claim deleted successfully"}), 200
