from flask_jwt_extended import get_jwt_identity
from src.models import LoginDetail, Staff
from flask import current_app
from services.extensions import db
from sqlalchemy.exc import SQLAlchemyError


def is_admin():
        """Confirmation of an admin user"""
        # Get the user ID from JWT token
        user_id = get_jwt_identity()["user_id"]
        
        # Check if user corresponds to a staff member
        login_details = LoginDetail.query.filter_by(staff_id=user_id).first()

        if login_details:
                staff_member = Staff.query.filter_by(staff_id=login_details.staff_id).first()
                if staff_member and staff_member.role == 'admin':
                        return True, None, None
                current_app.logger.warning("Unauthorized access to a restricted resource.")
                return False, {"error":"Unauthorized Access"}, 403

def format_product_data(product):
    """Convert Product Data to JSON Format"""
    product_data = {
        "product_id":product.product_id,
        "product_name": product.product_name,
        "variants":[{
            "variant_id": variant.variant_id,
            "sku": variant.sku,
            "price":float(variant.price),
            "attributes":[
                {"name":attribute.name, "value":attribute.value} 
                for attribute in variant.attributes
            ],
        "images":[
            {"image_name":image.image_name,"image_url":image.image_url}
            for image in variant.images

        ]

        } for variant in product.variants
        ]
    }
    return product_data

def format_category(data):
       """Formats category data to JSON"""
       category_data = {
              "category_id": data.category_id,
              "category_name": data.category_name,
              "parent_category_id": data.parent_category_id,
              "is_active": data.is_active
       }
       return category_data
       
def handle_db_operation(callable_func, success_msg):
       try:
              result = callable_func()
              db.session.commit()
              return {"message": success_msg}, 201
       except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add category:{str(e)}")
            return {"error":"Database error", "message":str(e)},500
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding new category: {e}")
            return {"error":"Database error","message":str(e)},500