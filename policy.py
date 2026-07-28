from database import db

class Policy(db.Model):
    __tablename__ = 'policies'

    id = db.Column(db.Integer, primary_key=True)
    policy_number = db.Column(db.String(50), unique=True, nullable=False)
    policy_type = db.Column(db.String(50), nullable=False) # e.g., 'Health', 'Life', 'Auto'
    premium_amount = db.Column(db.Float, nullable=False)
    coverage_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Active') # 'Active', 'Expired', 'Cancelled'
    
    # Foreign Key pointing to Customer
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "policy_number": self.policy_number,
            "policy_type": self.policy_type,
            "premium_amount": self.premium_amount,
            "coverage_amount": self.coverage_amount,
            "status": self.status,
            "customer_id": self.customer_id
        }