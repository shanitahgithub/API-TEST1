from flask import Blueprint,request,jsonify
from authors_app.models.user import User,db
from authors_app.extensions import db,Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
# from flask_jwt_extended import create_access_token

# Creating a blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
bcrypt = Bcrypt()

# Defining the registration endpoint
@auth.route('/register', methods=["POST"])
def register():
    try:
        # Extracting user data from the request JSON
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]
        image = request.json["image"]
        biography = request.json["biography"]
        user_type = request.json["user_type"]
        password = request.json["password"]
        contact = request.json["contact"]  

        # Validating input data
        if not first_name:
            return jsonify({'error': "Your first_name is required"})
        if not last_name:
            return jsonify({'error': "Your last_name is required"})
        if not email:
            return jsonify({'error': "Your email is required"})
        if not image:
            return jsonify({'error': "Your image is required"})
        if not biography:
            return jsonify({'error': "Your biography is required"})
        if not user_type == "author" and not biography:
            return jsonify({'error': "Your biography is required"})
        if not contact:
            return jsonify({'error': "Contact is required"})
        if len(password) < 6:
            return jsonify({'error': "Your password must at least have 6 characters"})
        if User.query.filter_by(email=email).first():
            return jsonify({'error': "The email already exists"})
        existing_user = User.query.filter_by(password=password).first()
        if existing_user:
            return jsonify({'error': "A user with this password already exists"}), 409


        # Creating a new instance of the User model
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            image=image,
            biography=biography,
            user_type=user_type,
            password=hashed_password,
            contact=contact  
        )

        # Adding the new user instance to the database session
        db.session.add(new_user)

        # Committing the session to save the changes to the database
        db.session.commit()
        # access_token = create_access_token(identity=email)

        # Returning a success response
        # return jsonify({'message': 'User created successfully', 'access_token': access_token}), 201
        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)})
    

# Defining the login endpoint
@auth.route('/login', methods=["POST"])
def login():
    try:
        # Extracting email and password from the request JSON
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Retrieving the user by email
        user = User.query.filter_by(email=email).first()

        # Checking if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            # Returning a success response
            return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
        else:
            # Returning an error response if authentication fails
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Defining the edit user endpoint
@auth.route('/edit/<int:user_id>', methods=["PUT"])
def edit_user(user_id):
    try:
        # Extracting user data from the request JSON
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Updating user fields if provided in the request
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Checking if the new email already exists
            new_email = data['email']
            if new_email != user.email and User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'The email already exists'}), 400
            user.email = new_email
        if 'image' in data:
            user.image = data['image']
        if 'biography' in data:
            user.biography = data['biography']
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'password' in data:
            password = data['password']
            if len(password) < 6:
                return jsonify({'error': 'Password must have at least 6 characters'}), 400
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        if 'contact' in data:
            user.contact = data['contact']

        # Committing the session to save the changes to the database
        db.session.commit()

        # Returning a success response
        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500    
    
## Defining the delete user endpoint
@auth.route('/delete/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit() #pushes to the database

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 
    
# Getting all users
@auth.route('/users', methods=["GET"])
def get_all_users():
    try:
        # Querying all users from the database
        users = User.query.all()

        # Serializing users data in other words convert data into a format suitable for storage
        serialized_users = []
        for user in users:
            serialized_user = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'image': user.image,
                'biography': user.biography,
                'user_type': user.user_type,
                'contact': user.contact
            }
            serialized_users.append(serialized_user)

        # Returning the serialized users data
        return jsonify({'users': serialized_users}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#  Getting a specific user   
@auth.route('/user/<int:user_id>', methods=["GET"])
    # getting a spedific user
def get_user(user_id):
        try:
            # Querying the user from the database by user ID
            # trying to get a pecific user by passing in their user_id
            user = User.query.get(user_id)

            # Checking if the user exists
            if user:
                # Serializing the user data
                serialized_user = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'image': user.image,
                    'biography': user.biography,
                    'user_type': user.user_type,
                    'contact': user.contact
                }
                # Returning the serialized user data
                return jsonify({'user': serialized_user}), 200
            else:
                return jsonify({'error': 'User not found'}), 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        

# @auth.route('/create_access_token', methods=['POST'])
# def create_access_token():
#     try:
#         email = request.json.get('email')
#         password = request.json.get('password')

#         if not email or not password:
#             return jsonify({'error': 'Missing email or password'}), 400

#         user = User.query.filter_by(email=email).first()
#         if not user or not bcrypt.check_password_hash(user.password, password):
#             return jsonify({'error': 'Invalid email or password'}), 401

#         access_token = create_access_token(identity=user.id)
#         return jsonify({'access_token': access_token}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
      


    
    
    
    
    
    
    



