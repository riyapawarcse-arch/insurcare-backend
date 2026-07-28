from flask import jsonify
from services.dashboard_service import get_dashboard_stats

def fetch_dashboard_stats():
    stats = get_dashboard_stats()
    return jsonify(stats), 200
