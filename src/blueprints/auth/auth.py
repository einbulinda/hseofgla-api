from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from src import db, limiter
import time
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
        username = data['username']
        name = data['name']
        email = data['email']
        mobile = data['mobile']
        password = data['password']
        role = data.get('role','customer').lower() # Default role
        current_user = data.get('current_user',1001)
        password_hash = generate_password_hash(password)
    
        with db.session.begin():  # For handling transaction commit and rollback       
            if role in ['staff','admin']:
                # Create a new staff member and login details
                user = Staff(name=name,email=email,mobile_number=mobile,role=role,created_by=current_user)
            else:
                # Create new customer and login details
                user = Customer(name=name,email=email,mobile_number=mobile,created_by=current_user)
            
            db.session.add(user)
            db.session.flush() # Flush to get the staff id before committing

            login_detail = LoginDetails(
                staff_id=user.staff_id if isinstance(user,Staff) else None,
                customer_id=user.customer_id if isinstance(user, Customer) else None,
                username=username, password=password_hash, created_by=current_user, updated_by=current_user)
            
            db.session.add(login_detail)

        current_app.logger.info(f"User registered successfully: {username}")    
        return jsonify({"message":"User registered successfully"}),201
    except Exception as e:
        current_app.logger.error(f"Error registering user: {e}")
        return jsonify({"error":"Registration failed","details":str(e)}),500

@auth.route('/login', methods=['POST'])
@limiter.limit("5 per minute") # 5 attempts in a minute.
def login():
    """Provides logic for Customer login"""   

    # Identify source system
    source = request.headers.get('Source-System','customer')  # Default to 'customer' if not provided
    data = request.get_json()
    username = data['username']
    password = data['password']

    time.sleep(1) # Time delay to discourage brute force.

    # Determine query based on the source system
    user = None
    if source.lower() == 'back-office':
        user = LoginDetails.query.filter(LoginDetails.username == username, LoginDetails.staff_id.isnot(None)).first()
    else:
        user = LoginDetails.query.filter(LoginDetails.username == username, LoginDetails.customer_id.isnot(None)).first()
    
    if user and (user.failed_attempts >= 5 or user.is_locked):
        return jsonify({"error":"Account is locked due to too many failed attempts or administrative reasons."}),403

    if user and check_password_hash(user.password, password):
        # Reset the failed attempt count on success.
        user.failed_attempts = 0
        db.session.commit()

        # Create access token using the identity of the user
        access_token = create_access_token(identity={"user_id":user.staff_id if user.staff_id else user.customer_id})
        record_login_session(user.staff_id, request)
        
        return jsonify({
            "message":"Login successful",
            "username": user.username,
            "access_token" : access_token
        }), 200
    else:
        user.failed_attempts = user.failed_attempts + 1
        db.session.commit()
        return jsonify({"message":"Invalid username or password."}), 401

def record_login_session(user_id, request):
    """Record a new login session for a staff member."""
    from src.models.staff_login_sessions import StaffLoginSessions
    
    new_session = StaffLoginSessions(
        staff_id = user_id,
        ip_address = request.remote_addr,
        device_info = str(request.user_agent)
    )
    db.session.add(new_session)
    db.session.commit()
