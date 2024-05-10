from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import secure_filename
from sqlalchemy.exc import SQLAlchemyError
import logging
import os
from sqlalchemy.orm import joinedload
from src.services.extensions import db
from src.utils import is_admin
from src.models import Product, ProductVariant, ProductAttribute, Inventory, ProductImage



products = Blueprint('products',__name__, url_prefix='/api/v1/products')

@products.route('/',methods=["POST"])
@jwt_required()
def add_product():
    if not is_admin():
        current_app.logger.warning("Unauthorized attempt to access product addition.")
        return jsonify({"error":"Unauthorized access."}),403
    
    # Extracting JSON from the request
    user_id = get_jwt_identity()
    data = request.json
    header = data.get('header')
    variants = data.get('variants',[])
    
    try:
        # Creating Product instance
        new_product = Product(product_name=header['product_name'],category_id=header['category_id'], created_by=user_id)
        db.session.add(new_product)
        db.session.flush() # To get the product_id

        # Create new Product Variant
        for variant in variants:
            new_variant = ProductVariant(
                product_id=new_product.id,
                sku=variants["sku"],
                price=variants["price"]
            )
            db.session.add(new_variant)
            db.session.flush()  # Get the variant_id

            # Add Attributes
            for attribute in variant.get("attributes",[]):
                new_attribute = ProductAttribute(
                    variant_id=new_variant.variant_id,
                    name=attribute["name"],
                    value=attribute["value"]
                )
                db.session.add(new_attribute)

                # Add Inventory
                new_inventory = Inventory(
                    variant_id=new_variant.variant_id,
                    quantity=variant["quantity"]
                )
                db.session.add(new_inventory)

                # Handle Image Upload
                for image_data in variant.get("images",[]):
                    image_filename = secure_filename(image_data["name"])
                    image_path = os.path.join('/path/to/upload/directory', image_filename)
                    # Handle file saving logic or cloud upload here
                    

                    new_image = ProductImage(
                        variant_id=new_variant.id, 
                        image_name=image_data['name'],
                        image_url=image_path  # Path to external hosted URL
                    )                
                    db.session.add(new_image)

        db.session.commit()
        current_app.logger.info("New product added successfully.")
        return jsonify({"message":"Product added successfully"}),201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to add product: {e}")
        return jsonify({"error":"Failed to save product","message":str(e)}),500


@products.route('/', methods=["GET"])
@jwt_required()
def get_products():
    """Returns all products with their details"""
    current_app.logger.info("Fetching all products")
    try:
    # Fetch all product details in one query to avoid N+1 problem
        products = Product.query.options(
            joinedload(Product.variants)
            .joinedload(ProductVariant.attributes),
            joinedload(Product.variants)
            .joinedload(ProductVariant.images)
        ).all()

        # Convert data to JSON format
        products_list = []
        for product in products:
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
            products_list.append(product_data)
        current_app.logger.info(f"Successfully retrieved {len(products_list)} products.")
        return jsonify(products_list),200
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error fetching products:{str(e)}")
        return jsonify({"error":"Database error", "message":str(e)}),500
    except Exception as e:
        current_app.logger.error(f"Error fetching products:{str(e)}")
        return jsonify({"error":"Unexpected Error", "message":str(e)}),500
        


@products.route('/<int:product_id>', methods=["GET"])
@jwt_required()
def get_product(product_id):
    """Gets details of a specific product"""
    current_app.logger.info(f"Getting details for product with ID: {product_id}")
    try:
        # Fetch product with all its related details
        product = Product.query.options(
            joinedload(Product.variants)
            .joinedload(ProductVariant.attributes),
            joinedload(Product.variants)
            .joinedload(ProductVariant.images)
        ).filter_by(product_id=product_id).first()

        if not product:
            current_app.logger.warning(f"Product with ID {product_id} not found.")
            return jsonify({"error":"Product Not Found"}),404
        
        # Serialize the data
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
        return jsonify(product_data),200
    except Exception as e:
        current_app.logger.error(f"Error fetching product with ID {product_id}: {e}.")
        return jsonify({"error":"Internal Server Error","message":str(e)}),500
