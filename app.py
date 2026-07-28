# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allows React frontend to make requests to Flask API

# Configuration
app.config['SECRET_KEY'] = 'insurcare-super-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insurcare.db'  # Uses SQLite locally; easily swapped to PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-insurcare-secret-key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ==========================================
# DATABASE MODELS
# ==========================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Admin')

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    custom_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    status = db.Column(db.String(20), default='Active')

class Policy(db.Model):
    __tablename__ = 'policies'
    id = db.Column(db.Integer, primary_key=True)
    policy_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    policy_type = db.Column(db.String(100), nullable=False)
    premium_amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Active')

class Claim(db.Model):
    __tablename__ = 'claims'
    id = db.Column(db.Integer, primary_key=True)
    claim_code = db.Column(db.String(20), unique=True, nullable=False)
    applicant = db.Column(db.String(100), nullable=False)
    policy_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    submission_date = db.Column(db.String(20), default=datetime.utcnow().strftime('%Y-%m-%d'))

# Initialize database tables
with app.app_context():
    db.create_all()

# ==========================================
# API ENDPOINTS
# ==========================================

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Insur-Care API is running!"}), 200

# AUTHENTICATION
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_pw, role=data.get('role', 'Admin'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity={"id": user.id, "email": user.email, "role": user.role})
        return jsonify({"token": token, "user": {"name": user.name, "email": user.email, "role": user.role}}), 200
    return jsonify({"error": "Invalid email or password"}), 401

# CLAIMS MODULE
@app.route('/api/claims', methods=['GET'])
def get_claims():
    claims = Claim.query.all()
    output = []
    for c in claims:
        output.append({
            "id": c.claim_code,
            "applicant": c.applicant,
            "policyId": c.policy_id,
            "amount": f"₹{c.amount:,.0f}",
            "numericAmount": c.amount,
            "status": c.status,
            "submissionDate": c.submission_date,
            "description": c.description
        })
    return jsonify(output), 200

@app.route('/api/claims/<claim_code>/status', methods=['PATCH'])
def update_claim_status(claim_code):
    data = request.get_json()
    claim = Claim.query.filter_by(claim_code=claim_code).first()
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    
    claim.status = data.get('status', claim.status)
    db.session.commit()
    return jsonify({"message": f"Claim status updated to {claim.status}"}), 200

# CUSTOMERS MODULE
@app.route('/api/customers', methods=['GET', 'POST'])
def handle_customers():
    if request.method == 'POST':
        data = request.get_json()
        count = Customer.query.count()
        new_cust = Customer(
            custom_id=f"CUST-60{count+1}",
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            address=data.get('address', '')
        )
        db.session.add(new_cust)
        db.session.commit()
        return jsonify({"message": "Customer created successfully"}), 201

    customers = Customer.query.all()
    output = []
    for c in customers:
        output.append({
            "id": c.custom_id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "address": c.address,
            "status": c.status
        })
    return jsonify(output), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    