from flask import current_app, jsonify
from .extensions import db
from src.models import Category
from src.utils import format_category, is_admin, handle_db_operation
from sqlalchemy.exc import SQLAlchemyError

class CategoryService:
    @staticmethod
    def add_category(data, user):
        """Add a new category to the application"""
        current_app.logger.info(f"User ID {user} is commencing addition of a new category")
        
        authorized, response, status = is_admin()
        if not authorized:
            return jsonify(response), status
        
        def add():    
            new_category = Category(
                category_name = data["category_name"], 
                parent_category_id = data["parent_category_id"], 
                created_by = user
            )
            db.session.add(new_category)

        return handle_db_operation(add,"Category added successfully")
    
    @staticmethod
    def fetch_categories():
        """Returns list of all categories"""
        current_app.logger.info("Fetching all categories")
        try:
            authorized, response, status = is_admin()
            if not authorized:
                return jsonify(response), status    

            categories = Category.query.filter_by(is_active=True).all()
            category_list = [format_category(category) for category in categories]
            current_app.logger.info(f"Successfully retrieved {len(category_list)} categories.")
            return category_list, 200
        
        except SQLAlchemyError as e:
            current_app.logger.error(f"Error fetching categories:{str(e)}")
            return {"error":"Database error", "message":str(e)}, 500
        except Exception as e:
            current_app.logger.error(f"Error fetching categories:{str(e)}")
            return {"error":"Unexpected Error", "message":str(e)}, 500
    
    @staticmethod
    def fetch_category(id):
        """Returns details of a single category"""
        current_app.logger.info(f"Fetching category details for ID {id}")
        try:
            category = Category.query.filter_by(is_active=True, category_id=id).first()

            if not category:
                current_app.logger.warning(f"Category with ID {id} not found")
                return {"error":"Category Not Found"},  404
            

            category_data = format_category(category)
            return category_data, 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Error fetching categories:{str(e)}")
            return {"error":"Database error", "message":str(e)}, 500
        except Exception as e:
            current_app.logger.error(f"Error fetching categories:{str(e)}")
            return {"error":"Unexpected Error", "message":str(e)}, 500
    
    @staticmethod
    def update_category(id,data,user):
        """Updates details of a given category"""
        try:
            current_app.logger.info(f"User {user} is updating category details for ID {id}")

            authorized, response, status = is_admin()
            if not authorized:
                return jsonify(response), status

            # Fetch the category being updated
            category = Category.query.filter_by(category_id=id).first()

            if not category:
                    current_app.logger.warning(f"Category with ID {id} not found")
                    return {"error":"Category Not Found"}, 404

            category.category_name = data.get("category_name", category.category_name)
            category.parent_category_id = data.get("parent_category_id", category.parent_category_id)
            category.is_active = data.get("is_active", category.is_active)
            category.updated_by = user

            db.session.add(category)
            db.session.commit()
            return {"message":"Category updated successfully."}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to update category:{str(e)}")
            return {"error":"Database error", "message":str(e)}, 500
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating category: {e}")
            return {"error":"Database error","message":str(e)}, 500





