from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils import is_admin
from src.services.category_service import CategoryService, fetch_all_categories, fetch_category, update_category

categories = Blueprint('categories',__name__, url_prefix='/api/v1/categories')

@categories.route('/', methods=["POST"])
@jwt_required()
def post_category():
    if not is_admin():
        current_app.logger.warning("Unauthorized attempt to access product addition.")
        return jsonify({"error":"Unauthorized access."}),403
    user = get_jwt_identity() # Accessed from user token
    response, status = CategoryService.post(request.json, user['user_id'])
    return response, status


@categories.route('/<int:category_id>', methods=["PATCH"])
@jwt_required()
def patch_category(category_id):
    if not is_admin():
        current_app.logger.warning("Unauthorized attempt to access product addition.")
        return jsonify({"error":"Unauthorized access."}),403
    user_id = get_jwt_identity()
    response,status = update_category(category_id,request.json, user_id)
    return jsonify(response),status


@categories.route('/', methods=["GET"])
@jwt_required()
def get_categories():
    response,status = CategoryService.get()    
    return response,status


@categories.route('/<int:category_id>', methods=["GET"])
@jwt_required()
def get_product(category_id):
    response,status = fetch_category(category_id)
    return jsonify(response),status