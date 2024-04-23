from flask import Blueprint, request, jsonify
from authors_app.models.company import Company
from authors_app.models.user import User
# from flask import Blueprint, request, jsonify
# from authors_app.models.company import Company, db
# from authors_app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from authors_app.extensions import db,Bcrypt,JWTManager
from flask_jwt_extended import  create_access_token,create_refresh_token


companies = Blueprint('company', __name__, url_prefix='/api/v1/companies')

# Endpoint for creating a company
@companies.route('/create', methods=['POST'])
@jwt_required()  # This decorator ensures that a valid JWT token is provided
def create_company():
    try:
        # Extracting request data
        company_name = request.json.get('company_name')
        origin = request.json.get('origin')
        description = request.json.get('description')
        
        # Debugging: Printing the token identity
        current_user_id = get_jwt_identity()
        print("Token Identity:", current_user_id)

        # You can get user_id from the access token instead of sending it in the request
        user_id = current_user_id  # Using the user ID extracted from the token
        
        # Basic input validation
        if not company_name:
            return jsonify({"error": 'Company name is required'}), 400

        if not origin:
            return jsonify({"error": 'Company origin is required'}), 400

        if not description:
            return jsonify({"error": 'Company description is required'}), 400
        
        if Company.query.filter_by(company_name=company_name).first():
            return jsonify({"error":'Company already exists'})

        # Creating a new company associated with the user
        new_company = Company(
            company_name=company_name,
            origin=origin,
            description=description,
            user_id=user_id
        )

        # Adding the new company to the session
        db.session.add(new_company)
        
        # Committing the changes to the database
        db.session.commit()

        # Building a response message
        message = f" '{new_company.company_name}' company has been  has been successfully created"
        return jsonify({"message": message,
                     'company':{
                         'company_id':new_company.id,
                         'company_name':new_company.company_name,
                         'origin':new_company.origin,
                         'description':new_company.description,
                         'user_id':new_company.user_id} }), 201

    except Exception as e:
        # Rolling back the session in case of an error
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
  
# Editing a company
@companies.route('/edit/<int:id>', methods=["PUT"])
@jwt_required()  # Ensuring a valid JWT token is provided
def edit_company(id):
    try:
        # Extracting user_id from the JWT token
        user= get_jwt_identity()

        # Extracting company data from the request JSON
        data = request.json
        company= Company.query.filter_by(id=id,user_id=user).first()
        if not company:
            return jsonify({'error': 'You have no access to this Company'}), 404

        # Updating company fields 
        if 'company_name' in data:
            company.title = data['company_name']
        if 'description' in data:
            company.description = data['description']
        if 'origin' in data:
            company.description = data['origin']
        
         # Committing the session to save the changes to the database
        db.session.commit()

        # Returning a success response
        return jsonify({'message': 'Company has been updated successfully',
                        'company':{
                         'company_name':company.company_name,
                         'origin':company.origin,
                         'description':company.description,
                         'user_id':company.user_id} }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 
    
# Deleting a company
@companies.route('/delete/<int:id>', methods=["DELETE"])
@jwt_required()  # Ensuring a valid JWT token is provided
def delete_company(id):
    try:
        # Extracting user_id from the JWT token
        user= get_jwt_identity()

        # Retrieving the company to delete
        company= Company.query.filter_by(id=id,user_id=user).first()
        if not company:
            return jsonify({'error': 'You have no access to this Company'}), 404

        # Deleting the company
        db.session.delete(company)
        db.session.commit()

        return jsonify({'message': 'Company has been deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Getting a specific company
@companies.route('/company/<int:id>', methods=["GET"])
@jwt_required()  # Ensuring a valid JWT token is provided
def get_company(id):
    try:
        # Extracting  user_id from the JWT token
        user = get_jwt_identity()

        # Retrievig the user
        
        company= Company.query.filter_by(id=id,user_id=user).first()
        

        # Checking if the company exists
        if not company:
            return jsonify({'error': 'You have no access to this company'}), 404

        
        # Serializing company data
        serialized_company= {
                'id': company.id,
                'company_name': company.company_name,
                'origin': company.origin,
                'description': company.description,
                'user_id':company.user_id
                
        }

        # Returning the serialized company data
        return jsonify({'company': serialized_company}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500   

# Getting all Companies
@companies.route('/allCompanies', methods=["GET"])
@jwt_required()  # Ensuring a valid JWT token is provided
def get_all_companies():
    try:
        # Extracting user_id from the JWT token
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401


        # Querying all companies from the database
        allCompanies = Company.query.all()

        # Serializing company data
        serialized_allCompanies = []
        for company in allCompanies:
            serialized_company= {
                'id': company.id,
                'company_name': company.company_name,
                'origin': company.origin,
                'description': company.description,
                
                'user_id': company.user_id,

            }
            serialized_allCompanies.append(serialized_company)

        # Returning the serialized company data
        return jsonify({'companies': serialized_allCompanies}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
   
 

    


