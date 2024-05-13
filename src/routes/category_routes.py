from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils import is_admin
from src.services.category_service import CategoryService

categories = Blueprint('categories',__name__, url_prefix='/api/v1/categories')

@categories.route('/', methods=["POST"])
@jwt_required()
def post_category():        
    response, status = CategoryService.add_category(request.json, get_jwt_identity()["user_id"])
    return jsonify(response), status


@categories.route('/<int:category_id>', methods=["PATCH"])
@jwt_required()
def patch_category(category_id):
    response,status = CategoryService.update_category(category_id,request.json, get_jwt_identity()['user_id'])
    return jsonify(response), status


@categories.route('/', methods=["GET"])
@jwt_required()
def get_categories():
    response,status = CategoryService.fetch_categories()    
    return jsonify(response),status


@categories.route('/<int:category_id>', methods=["GET"])
@jwt_required()
def get_product(category_id):
    response,status = CategoryService.fetch_category(category_id)
    return jsonify(response), status