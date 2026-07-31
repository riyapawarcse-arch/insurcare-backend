# InsurCare Backend API

The robust Flask-based REST API powering the Insurance Management Platform. It handles database modeling, authentication, business logic, role-based access control, and document processing.

## 🚀 Live API Endpoint
* **Base URL:** https://dashboard.render.com/project/prj-d9kfn4lg1s2s7381lrag 

---

## 🛠️ Tech Stack & Libraries
* **Language & Framework:** Python, Flask, Flask Blueprints
* **Database & ORM:** PostgreSQL, SQLAlchemy ORM
* **Migrations:** Flask-Migrate (Alembic)
* **Authentication & Security:** Flask-JWT-Extended, Flask-Bcrypt (Password Hashing)
* **Data Validation & Serialization:** Marshmallow
* **File Handling:** Werkzeug
* **Deployment:** Render

---

## 📂 Project Structure
```text
backend/
├── app.py
├── config.py
├── requirements.txt
├── models/         # SQLAlchemy database models
├── routes/         # API endpoints / Blueprints
├── services/       # Business logic and helper services
├── schemas/        # Marshmallow validation schemas
├── middleware/     # Custom auth and role verification
├── uploads/        # Stored documents and attachments
└── migrations/     # Database migration scripts
