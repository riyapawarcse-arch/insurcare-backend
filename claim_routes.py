from flask import Blueprint
from controllers.claim_controller import (
    get_claims,
    get_claim,
    add_claim,
    modify_claim_status,
    remove_claim
)

claim_bp = Blueprint('claim_bp', __name__)

@claim_bp.route('/claims', methods=['GET'])
def fetch_all():
    return get_claims()

@claim_bp.route('/claims/<int:claim_id>', methods=['GET'])
def fetch_one(claim_id):
    return get_claim(claim_id)

@claim_bp.route('/claims', methods=['POST'])
def create():
    return add_claim()

@claim_bp.route('/claims/<int:claim_id>/status', methods=['PUT'])
def update_status(claim_id):
    return modify_claim_status(claim_id)

@claim_bp.route('/claims/<int:claim_id>', methods=['DELETE'])
def delete(claim_id):
    return remove_claim(claim_id)
