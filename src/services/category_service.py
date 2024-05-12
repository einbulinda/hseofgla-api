from flask import current_app, jsonify
from .extensions import db
from src.models import Category
from src.utils import format_category
from sqlalchemy.exc import SQLAlchemyError

class CategoryService:
    @staticmethod
    def post(data, user):
        """Add a new category to the application"""
        current_app.logger.info(f"User ID {user} is commencing addition of a new category")
        try:
            new_category = Category(category_name = data["category_name"], parent_category_id = data["parent_category_id"], created_by = user)
            db.session.add(new_category)
            db.session.commit()
            return jsonify({"message":"Category added successfully."}),201
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add category:{str(e)}")
            return jsonify({"error":"Database error", "message":str(e)}),500
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding new category: {e}")
            return jsonify({"error":"Database error","message":str(e)}),500
    
    @staticmethod
    def get():
        """Returns list of all categories"""
        current_app.logger.info("Fetching all categories")
        try:
            categories = Category.query.filter_by(is_active=True).all()
            category_list = [format_category(category) for category in categories]
            current_app.logger.info(f"Successfully retrieved {len(category_list)} categories.")
            current_app.logger.info(category_list)
            return jsonify(category_list),200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Error fetching categories:{str(e)}")
            return jsonify({"error":"Database error", "message":str(e)}),500
        except Exception as e:
            current_app.logger.error(f"Error fetching categories:{str(e)}")
            return jsonify({"error":"Unexpected Error", "message":str(e)}),500




def fetch_all_categories():
    """Returns list of all categories"""
    current_app.logger.info("Fetching all categories")
    pass

def fetch_category(id):
    """Returns details of a single category"""
    current_app.logger.info(f"Fetching category details for ID {id}")
    pass

def update_category(id, data,  user):
    """Updates details of a given category"""
    current_app.logger.info(f"User {user} is updating category details for ID {id}")

    pass