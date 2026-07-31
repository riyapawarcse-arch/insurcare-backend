from flask import Blueprint
from controllers.document_controller import upload_file, fetch_documents

document_bp = Blueprint('document_bp', __name__)

@document_bp.route('/documents/upload', methods=['POST'])
def handle_upload():
    return upload_file()

@document_bp.route('/documents/customer/<int:customer_id>', methods=['GET'])
def get_by_customer(customer_id):
    return fetch_documents(customer_id)