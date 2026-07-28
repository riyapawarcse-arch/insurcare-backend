from models.customer import Customer
from models.policy import Policy
from models.claim import Claim
from models.premium import PremiumPayment
from database import db
from sqlalchemy import func

def get_dashboard_stats():
    total_customers = Customer.query.count()
    total_policies = Policy.query.count()
    total_claims = Claim.query.count()
    
    # Calculate total revenue from 'Paid' premiums
    revenue_result = db.session.query(func.sum(PremiumPayment.amount)).filter_by(payment_status='Paid').scalar()
    total_revenue = revenue_result if revenue_result else 0.0

    return {
        "total_customers": total_customers,
        "total_policies": total_policies,
        "total_claims": total_claims,
        "total_revenue": total_revenue
    }
