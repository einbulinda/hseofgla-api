from flask import jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
import os
from .extensions import db
from src.utils import format_product_data
from src.models import Product, ProductVariant, ProductAttribute, Inventory, ProductImage


def add_product(data, user_id):
    """Add a new product to the application"""
    try:
        new_product = Product(
            product_name=data['header']['product_name'],
            category_id=data['header']['category_id'], 
            created_by=user_id
        )
        db.session.add(new_product)
        db.session.flush()

        for variant in data['variants']:
            process_variant(variant, new_product.product_id, user_id)
        
        db.session.commit()
        current_app.logger.info("New product added successfully.")
        return jsonify({"message":"Product added successfully"}),201
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to add product:{str(e)}")
        return jsonify({"error":"Database error", "message":str(e)}),500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding new product: {e}")
        return jsonify({"error":"Database error","message":str(e)}),500

def process_variant(variant_data, product_id, user_id):
    """Save Product Variant"""    
    new_variant = ProductVariant(
        product_id = product_id,
        sku = variant_data['sku'],
        price = variant_data['price'],
        created_by = user_id,
    )
    db.session.add(new_variant)
    db.session.flush()

    # Save the quantities on adding product
    add_inventory(new_variant.variant_id, variant_data['quantity'], user_id)

    for attribute in variant_data['attributes']:
        process_attributes(attribute, new_variant.variant_id, user_id)
    
    for image in variant_data['images']:
        save_image(image, new_variant.variant_id, user_id)

    
def process_attributes(attr_data, variant_id, user_id):
    """Save a variant attributes for a Product"""
    new_attr = ProductAttribute(
        variant_id=variant_id,
        name=attr_data["name"],
        value=attr_data["value"],
        created_by = user_id
    )
    db.session.add(new_attr)


def add_inventory(variant_id, quantity, user_id):
    """Update Product Inventory"""
    new_inventory = Inventory(
        variant_id = variant_id,
        quantity = quantity,
        created_by = user_id
    )
    db.session.add(new_inventory)

def save_image(image, variant_id, user_id):
    """Save Product Images"""
    image_filename = secure_filename(image["name"])
    image_path = os.path.join('/path/to/upload/directory', image_filename)
    
    # Handle file saving logic or cloud upload here
                    

    new_image = ProductImage(
        variant_id=variant_id, 
        image_name=image['name'],
        image_url=image_path  # Path to external hosted URL
    )                
    db.session.add(new_image)

def fetch_all_products():
    """Returns all products with their details"""
    current_app.logger.info("Fetching all products")
    
    try:
        # Fetch all product details in one query to avoid N+1 problem
        products = Product.query.options(
            joinedload(Product.variants)
            .joinedload(ProductVariant.attributes),
            joinedload(Product.variants)
            .joinedload(ProductVariant.images)
        ).filter_by(is_active=True).all()    

        products_list = [format_product_data(product) for product in products]
        current_app.logger.info(f"Successfully retrieved {len(products_list)} products.")
        return jsonify(products_list),200
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error fetching products:{str(e)}")
        return jsonify({"error":"Database error", "message":str(e)}),500
    except Exception as e:
        current_app.logger.error(f"Error fetching products:{str(e)}")
        return jsonify({"error":"Unexpected Error", "message":str(e)}),500
        

def fetch_product(product_id):
    """Gets details of a specific product"""
    current_app.logger.info(f"Getting details for product with ID: {product_id}")
    current_app.logger.info(f"Getting details for product with ID: {product_id}")
    try:
        # Fetch product with all its related details
        product = Product.query.options(
            joinedload(Product.variants)
            .joinedload(ProductVariant.attributes),
            joinedload(Product.variants)
            .joinedload(ProductVariant.images)
        ).filter_by(product_id=product_id,is_active=True).first()

        if not product:
            current_app.logger.warning(f"Product with ID {product_id} not found.")
            return jsonify({"error":"Product Not Found"}),404
        
        # Serialize the data
        product_data = format_product_data(product)
        return jsonify(product_data),200
    except Exception as e:
        current_app.logger.error(f"Error fetching product with ID {product_id}: {e}.")
        return jsonify({"error":"Internal Server Error","message":str(e)}),500

def update_product_dtls(product_id,product_data, user):
    """Updates part of the details for a product."""
    current_app.logger.info(f"Attempting to update product with ID {product_id}")

    try:
        # Fetch the existing product
        product = Product.query.filter_by(product_id=product_id,is_active=True).first()
        if not product:
            current_app.logger.warning(f"Product with ID: {product_id} not found for update")
            return jsonify({"error":"Product Not Found"}),404
        
        # Update Product Core details
        product.product_name = product_data.get("product_name",product.product_name)
        product.category_id = product_data.get("category_id",product.category_id)
        product.is_active = product_data.get("is_active", product.is_active)
        product.updated_by = user

        # Update Variants
        if 'variants' in product_data:
            for variant_data in product_data['variants']:
                variant = ProductVariant.query.get(variant_data['variant_id'])
                if variant:
                    variant.sku = variant_data.get('sku',variant.sku)
                    variant.price = variant_data.get('price',variant.price)
                
                # Update attributes
                for attr_data in variant_data.get('attributes',[]):
                    attribute = next((attr for attr in variant.attributes if attr.attribute_id == attr_data['attribute_id']), None)
                    if attribute:
                        attribute.name = attr_data.get("name",attribute.name)
                        attribute.value = attr_data.get("value",attribute.value)
                
                # Update Images
                for img_data in variant_data.get('images',[]):
                    image = next((img for img in variant.images if variant.image_id == img_data["image_id"]), None)
                    if image:
                        image.image_name = img_data.get("image_name",image.image_name)
                        image.value = img_data.get("value",image.value)
        db.session.add(product)
        db.session.commit()
        current_app.logger.info(f"Product with ID {product_id} updated successfully")
        return jsonify({"message": "Product updated successfully"}),200
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error during product update: {str(e)}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error during product update: {str(e)}")
        return jsonify({"error":"Internal server error", "message":str(e)}),500




