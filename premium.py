from database import db
from datetime import datetime

class PremiumPayment(db.Model):
    __tablename__ = 'premium_payments'

    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), default='Paid')  # Paid, Pending, Overdue
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "policy_id": self.policy_id,
            "amount": self.amount,
            "payment_status": self.payment_status,
            "payment_date": self.payment_date.strftime('%Y-%m-%d %H:%M:%S') if self.payment_date else None
        }
    
    