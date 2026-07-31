from flask import Blueprint
from controllers.policy_controller import (
    get_policies,
    get_policy,
    add_policy,
    edit_policy,
    remove_policy
)

policy_bp = Blueprint('policy_bp', __name__)

@policy_bp.route('/policies', methods=['POST'])
def create():
    return add_policy()

@policy_bp.route('/policies', methods=['GET'])
def get_all():
    return get_policies()