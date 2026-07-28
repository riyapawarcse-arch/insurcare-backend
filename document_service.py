import os
from werkzeug.utils import secure_filename
from database import db
from models.document import Document
from models.customer import Customer

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_document(customer_id, file):
    customer = Customer.query.get(customer_id)
    if not customer:
        return None, "Customer not found"

    if not file or file.filename == '':
        return None, "No file provided"

    if not allowed_file(file.filename):
        return None, "Invalid file type. Allowed: pdf, png, jpg, jpeg"

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    new_doc = Document(
        customer_id=customer_id,
        file_name=filename,
        file_path=file_path
    )

    db.session.add(new_doc)
    db.session.commit()
    return new_doc.to_dict(), None

def get_customer_documents(customer_id):
    docs = Document.query.filter_by(customer_id=customer_id).all()
    return [doc.to_dict() for doc in docs]