from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.premium import PremiumPayment
from database import db
from datetime import datetime

premium_bp = Blueprint('premium_bp', __name__)

@premium_bp.route('/api/premiums', methods=['GET'])
@jwt_required()
def get_premiums():
    payments = PremiumPayment.query.all()
    return jsonify([p.to_dict() for p in payments]), 200

@premium_bp.route('/api/premiums', methods=['POST'])
@jwt_required()
def add_premium():
    data = request.get_json()
    
    payment_date = datetime.utcnow()
    if data.get('payment_date'):
        try:
            payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d')
        except ValueError:
            pass

    new_payment = PremiumPayment(
        policy_id=data['policy_id'],
        amount=float(data['amount']),
        payment_status=data.get('payment_status', 'Paid'),
        payment_date=payment_date
    )
    
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Premium payment recorded successfully!', 'payment': new_payment.to_dict()}), 201

