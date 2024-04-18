from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from src import db
from src.models.staff import Staff
from src.models.customers import Customer
from src.models.login_details import LoginDetails

# Create blueprint for authentication
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.route('/register', methods=['POST'])
def register():
    # Get data from request
    data = request.get_json()
    
    try:
        username = data.get('username')
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        role = data.get('role','customer').lower() # Default role
        current_user = data.get('current_user',1001)
    
        # Hash the password
        password_hash = generate_password_hash(password)
        
        if role in ['staff','admin']:
            # Create a new staff member and login details
            user = Staff(name=name,email=email,mobile_number=mobile,role=role,created_by=current_user)
            db.session.add(user)
            db.session.flush() # Flush to get the staff id before committing
            login_detail = LoginDetails(staff_id=user.staff_id, username=username,password=password_hash,created_by=current_user,updated_by=current_user)
        else:
            # Create new customer and login details
            user = Customer(name=name,email=email,mobile_number=mobile,created_by=current_user)
            db.session.add(user)
            db.session.flush()
            login_detail = LoginDetails(customer_id=user.customer_id,username=username, password=password_hash, created_by=user.customer_id, updated_by=user.customer_id)
        
        db.session.add(login_detail)
        db.session.commit()
        current_app.logger.info(f"User registered successfully: {username}")    
        return jsonify({"message":"User registered successfully"}),201
    except Exception as e:
        current_app.logger.error(f"Error registering user: {e}")
        return jsonify({"error":"Registration failed","details":str(e)}),500

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Query login_details to get user by the username provided
    login_detail = LoginDetails.query.filter_by(username=username).first()
    
    if login_detail and check_password_hash(login_detail.password, password):
        access_token = create_access_token(identity={'user_id': login_detail.staff_id or login_detail.customer_id})
        if login_detail.staff_id:
            # Fetch staff profile details
            staff = Staff.query.get(login_detail.staff_id)
            profile_data = {
                "user_id":staff.staff_id,
                "name": staff.name,
                # "role": staff.role
            }
        elif login_detail.customer_id:
            customer = Customer.query.get(login_detail.customer_id)
            profile_data = {
                "user_id": customer.customer_id,
                "name": customer.name,
            }
        else:
            return jsonify({"message":"User role could not be determined"}), 401
        
        profile_data["access_token"] = access_token
        
        return jsonify({
            "message":"Login successful",
            "profile": profile_data
        }), 200
    else:
        return jsonify({"message":"Invalid username or password."}), 401
            
    