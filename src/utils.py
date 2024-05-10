from flask_jwt_extended import get_jwt_identity
from src.models.login_detail import LoginDetails
from src.models.staff import Staff


def is_admin():
        """Confirmation of an admin user"""
        # Get the user ID from JWT token
        user_id = get_jwt_identity()["user_id"]
        
        # Check if user corresponds to a staff member
        login_details = LoginDetails.query.filter_by(staff_id=user_id).first()

        if login_details:
                staff_member = Staff.query.filter_by(staff_id=login_details.staff_id).first()
                if staff_member and staff_member.role == 'admin':
                        return True
                return False

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