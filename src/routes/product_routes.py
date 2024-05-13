from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.product_service import add_product, fetch_all_products, fetch_product, update_product_dtls
from src.utils import is_admin

products = Blueprint('products',__name__, url_prefix='/api/v1/products')


@products.route('/',methods=["POST"])
@jwt_required()
def add_product_route():
    if not is_admin():
        current_app.logger.warning("Unauthorized attempt to access product addition.")
        return jsonify({"error":"Unauthorized access."}),403    
    # Extracting JSON from the request
    user_id = get_jwt_identity()
    response, status = add_product(request.json, user_id)
    return jsonify(response),status

@products.route('/', methods=["GET"])
@jwt_required()
def get_products():
    response,status = fetch_all_products()    
    return jsonify(response),status

@products.route('/<int:product_id>', methods=["GET"])
@jwt_required()
def get_product(product_id):
    response,status = fetch_product(product_id)
    return jsonify(response),status

@products.route('/<int:product_id>', methods=["PATCH"])
@jwt_required()
def update_product(product_id):
    user = get_jwt_identity()
    if not is_admin():
        current_app.logger.warning("Unauthorized attempt to access product addition.")
        return jsonify({"error":"Unauthorized access."}),403
    
    response,status = update_product_dtls(product_id,request.json, user["user_id"])
    return jsonify(response),status

