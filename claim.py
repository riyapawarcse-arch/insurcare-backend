from database import db
from datetime import datetime

class Claim(db.Model):
    __tablename__ = 'claims'

    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), nullable=False)
    claim_amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending') # Pending, Approved, Rejected
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "policy_id": self.policy_id,
            "claim_amount": self.claim_amount,
            "reason": self.reason,
            "status": self.status,
            "submission_date": self.submission_date.strftime('%Y-%m-%d %H:%M:%S') if self.submission_date else None
        }
    