from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.user import User
from models.customer import Customer  # Ensure your model imports match your project
from models.policy import Policy
from models.claim import Claim

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    try:
        # Count records from database (or return default counts if tables are empty)
        total_customers = Customer.query.count() if hasattr(Customer, 'query') else 0
        active_policies = Policy.query.count() if hasattr(Policy, 'query') else 0
        total_claims = Claim.query.count() if hasattr(Claim, 'query') else 0
        
        return jsonify({
            'totalCustomers': total_customers,
            'activePolicies': active_policies,
            'totalClaims': total_claims,
            'totalPremiums': 125000  # Placeholder or total calculated from db
        }), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching metrics', 'error': str(e)}), 500
    