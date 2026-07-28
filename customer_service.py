from database import db
from models.customer import Customer


def get_all_customers():
    return Customer.query.all()


def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)


def add_customer(data):
    customer = Customer(
        name=data["name"],
        email=data["email"],
        phone=data["phone"]
    )

    db.session.add(customer)
    db.session.commit()

    return customer


def update_customer(customer_id, data):
    customer = Customer.query.get(customer_id)

    if customer:
        customer.name = data["name"]
        customer.email = data["email"]
        customer.phone = data["phone"]

        db.session.commit()

    return customer


def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return True

    return False 
