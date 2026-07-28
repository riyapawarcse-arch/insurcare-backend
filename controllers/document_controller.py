from flask import request, jsonify
from services.document_service import save_document, get_customer_documents

def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in request"}), 400

    customer_id = request.form.get('customer_id')
    if not customer_id:
        return jsonify({"message": "customer_id is required"}), 400

    file = request.files['file']
    doc, error = save_document(customer_id, file)
    if error:
        return jsonify({"message": error}), 400

    return jsonify({"message": "Document uploaded successfully", "document": doc}), 201

def fetch_documents(customer_id):
    docs = get_customer_documents(customer_id)
    return jsonify(docs), 200