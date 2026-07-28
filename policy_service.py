from database import db
from models.policy import Policy
from models.customer import Customer

def get_all_policies():
    policies = Policy.query.all()
    return [policy.to_dict() for policy in policies]

def get_policy_by_id(policy_id):
    policy = Policy.query.get(policy_id)
    return policy.to_dict() if policy else None

def create_policy(data):
    # Check if the linked customer actually exists
    customer = Customer.query.get(data.get('customer_id'))
    if not customer:
        return None, "Customer not found"

    # Check for duplicate policy number
    existing_policy = Policy.query.filter_by(policy_number=data.get('policy_number')).first()
    if existing_policy:
        return None, "Policy number already exists"

    new_policy = Policy(
        policy_number=data.get('policy_number'),
        policy_type=data.get('policy_type'),
        premium_amount=data.get('premium_amount'),
        coverage_amount=data.get('coverage_amount'),
        status=data.get('status', 'Active'),
        customer_id=data.get('customer_id')
    )

    db.session.add(new_policy)
    db.session.commit()
    return new_policy.to_dict(), None

def update_policy(policy_id, data):
    policy = Policy.query.get(policy_id)
    if not policy:
        return None, "Policy not found"

    policy.policy_type = data.get('policy_type', policy.policy_type)
    policy.premium_amount = data.get('premium_amount', policy.premium_amount)
    policy.coverage_amount = data.get('coverage_amount', policy.coverage_amount)
    policy.status = data.get('status', policy.status)

    db.session.commit()
    return policy.to_dict(), None

def delete_policy(policy_id):
    policy = Policy.query.get(policy_id)
    if not policy:
        return False
    db.session.delete(policy)
    db.session.commit()
    return True
