

from authors_app.controllers.auth.auth_controller import auth


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



# Application Factory Function enable us to work with multiple instances
# The app instance is created under the function def create_app():
def create_app():
    
    app=Flask(__name__)
    
   

    app.config.from_object('config.Config')  

    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    

    
    from authors_app.models import book
    from authors_app.models import company
    from authors_app.models import user
    
    @app.route('/api/swagger.json')
    def swagger_json():
    #  swag = swagger(app)
     swag = swagger(app, from_file_keyword='swagger_from_file')
     swag['info']['version'] = "1.0"
     swag['info']['title'] = "My API"
     return jsonify(swag)
    
# Swagger UI configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
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

    

    



    


