from database import db
from models.premium import PremiumPayment
from models.policy import Policy

def get_all_payments():
    payments = PremiumPayment.query.all()
    return [p.to_dict() for p in payments]

def record_payment(data):
    policy = Policy.query.get(data.get('policy_id'))
    if not policy:
        return None, "Policy not found"

    new_payment = PremiumPayment(
        policy_id=data.get('policy_id'),
        amount=data.get('amount'),
        payment_status=data.get('payment_status', 'Paid')
    )

    db.session.add(new_payment)
    db.session.commit()
    return new_payment.to_dict(), None

def get_payments_by_policy(policy_id):
    payments = PremiumPayment.query.filter_by(policy_id=policy_id).all()
    return [p.to_dict() for p in payments]
