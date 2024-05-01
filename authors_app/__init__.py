

from authors_app.controllers.auth.auth_controller import auth

import os
import json
from authors_app.controllers.auth.book_controller import books
from authors_app.controllers.auth.company_controller import companies
from flask import Flask,jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from authors_app.extensions import migrate,bcrypt,jwt
from authors_app.extensions import db
from flask_jwt_extended import get_jwt_identity,jwt_required
from collections import OrderedDict



# Application Factory Function enable us to work with multiple instances
# The app instance is created under the function def create_app():

    
def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object('config.Config')  

    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    
    from authors_app.models import book
    from authors_app.models import company
    from authors_app.models import user
    
    # Serving Swagger JSON
    @app.route('/api/swagger.json')
    def swagger_json():
        
        swagger_data = {
    "swagger": "2.0",
    "info": {
        "version": "3.0.0",
        "title": "Authors API",
        "description": "API for managing authors, books, and companies"
    },
    "basePath": "/api/v1",
    "paths": {
        "/auth/register": {
            "post": {
                "summary": "Register a new user",
                "description": "Register a new user with the provided information",
                "parameters": [
                    {
                        "name": "User",
                        "in": "body",
                        "description": "User details",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "email": {"type": "string"},
                                "image": {"type": "string"},
                                "biography": {"type": "string"},
                                "user_type": {"type": "string"},
                                "password": {"type": "string"},
                                "contact": {"type": "string"}
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "User created successfully"},
                    "400": {"description": "Bad request"},
                    "409": {"description": "Conflict - User with this email already exists"}
                }
            }
        },
        "/auth/login": {
            "post": {
                "summary": "Login",
                "description": "Login with email and password",
                "parameters": [
                    {
                        "name": "Credentials",
                        "in": "body",
                        "description": "User email and password",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string"},
                                "password": {"type": "string"}
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {"description": "Login successful"},
                    "401": {"description": "Unauthorized - Invalid email or password"}
                }
            }
        },
        "/auth/edit/{id}": {
            "put": {
                "summary": "Edit user details",
                "description": "Edit user details by ID",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "User ID",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "User",
                        "in": "body",
                        "description": "Updated user details",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "email": {"type": "string"},
                                "image": {"type": "string"},
                                "biography": {"type": "string"},
                                "user_type": {"type": "string"},
                                "password": {"type": "string"},
                                "contact": {"type": "string"}
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "User updated successfully"},
                    "404": {"description": "Not found - User not found"},
                    "500": {"description": "Internal Server Error"}
                },
                "security": [
                    {"BearerAuth": []}
                ]
            }
        },
        "/auth/delete/{id}": {
            "delete": {
                "summary": "Delete user",
                "description": "Delete user by ID",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "User ID",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {"description": "User deleted successfully"},
                    "404": {"description": "Not found - User not found"},
                    "500": {"description": "Internal Server Error"}
                },
                "security": [
                    {"BearerAuth": []}
                ]
            }
        },
        "/auth/users": {
            "get": {
                "summary": "Get all users",
                "description": "Get details of all users",
                "responses": {
                    "200": {"description": "Success"},
                    "500": {"description": "Internal Server Error"}
                },
                "security": [
                    {"BearerAuth": []}
                ]
            }
        },
        "/auth/user/{id}": {
            "get": {
                "summary": "Get specific user",
                "description": "Get user details by ID",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "User ID",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {"description": "Success"},
                    "404": {"description": "Not found - User not found"},
                    "500": {"description": "Internal Server Error"}
                },
                "security": [
                    {"BearerAuth": []}
                ]
            }
        }
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
    "security": [
        {
            "BearerAuth": []
        }
    ]
}
        

# Converting to JSON and return
        return jsonify(swagger_data)
    
    
    
            
        return jsonify(swagger_data)
# Swagger UI configuration
    SWAGGER_URL = '/api/docs'  # <--- Ensure this matches the URL prefix in your Swagger UI
    API_URL = '/api/swagger.json'  # <--- Ensure this matches the URL for serving Swagger JSON
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "My API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    @app.route('/')
    def home():
        return "WELCOME TO MY AUTHORS API"
    
    
    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(books, url_prefix='/api/v1/books')
    app.register_blueprint(companies, url_prefix='/api/v1/companies')
    
    
    return app

    



   


    







# swagger_data = {
        #     "swagger": "2.0",
        #     "info": {
        #         "version": "1.0.0",
        #         "title": "Authors API",
        #         "description": "API for managing authors, books, and companies"
        #     },
        #     "basePath": "/api/v1",
        #     "paths": {
        #         # Define your API paths here
        #         # Example paths from your Swagger specification
        #         "/auth/register": {
        #             "post": {
        #                 "summary": "Register a new user",
        #                 "description": "Register a new user with the provided information",
        #                 "parameters": [
        #                     {
        #                         "name": "User",
        #                         "in": "body",
        #                         "description": "User details",
        #                         "required": True,
        #                         "schema": {
        #                             "type": "object",
        #                             "properties": {
        #                                 "first_name": {"type": "string"},
        #                                 "last_name": {"type": "string"},
        #                                 "email": {"type": "string"},
        #                                 "image": {"type": "string"},
        #                                 "biography": {"type": "string"},
        #                                 "user_type": {"type": "string"},
        #                                 "password": {"type": "string"},
        #                                 "contact": {"type": "string"}
        #                             }
        #                         }
        #                     }
        #                 ],
        #                 "responses": {
        #                     "201": {"description": "User created successfully"},
        #                     "400": {"description": "Bad request"},
        #                     "409": {"description": "Conflict - User with this email already exists"}
        #                 }
        #             }
        #         },
        #         # Add other paths similarly
        #     }
        # }
        # return jsonify(swagger_data)
# def create_app():
    
#     app=Flask(__name__)
    
   

#     app.config.from_object('config.Config')  

#     db.init_app(app)
#     migrate.init_app(app,db)
#     bcrypt.init_app(app)
#     jwt.init_app(app)
    

    
#     from authors_app.models import book
#     from authors_app.models import company
#     from authors_app.models import us




   

    
    
#     @app.route('/')
#     def home():
#         return "WELCOME TO MY AUTHORS API"
    
    
#     app.register_blueprint(auth, url_prefix='/api/v1/auth')
#     app.register_blueprint(books, url_prefix='/api/v1/books')
#     app.register_blueprint(companies, url_prefix='/api/v1/companies')
    
    
#     return app

    
