from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.utils import is_admin



products = Blueprint('products',__name__, url_prefix='/api/v1/products')

@products.route('/', methods=['POST'])
@jwt_required()
def add_product():
    if not is_admin():
        return jsonify({"error":"Unauthorized access."}),403
