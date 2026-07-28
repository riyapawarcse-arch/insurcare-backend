from database import db
from models.claim import Claim
from models.policy import Policy

def get_all_claims():
    claims = Claim.query.all()
    return [claim.to_dict() for claim in claims]

def get_claim_by_id(claim_id):
    claim = Claim.query.get(claim_id)
    return claim.to_dict() if claim else None

def create_claim(data):
    # Check if the policy exists
    policy = Policy.query.get(data.get('policy_id'))
    if not policy:
        return None, "Policy not found"

    new_claim = Claim(
        policy_id=data.get('policy_id'),
        claim_amount=data.get('claim_amount'),
        reason=data.get('reason'),
        status=data.get('status', 'Pending')
    )

    db.session.add(new_claim)
    db.session.commit()
    return new_claim.to_dict(), None

def update_claim_status(claim_id, status):
    claim = Claim.query.get(claim_id)
    if not claim:
        return None, "Claim not found"

    claim.status = status
    db.session.commit()
    return claim.to_dict(), None

def delete_claim(claim_id):
    claim = Claim.query.get(claim_id)
    if not claim:
        return False
    db.session.delete(claim)
    db.session.commit()
    return True
