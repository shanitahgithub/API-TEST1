

from authors_app.controllers.auth.auth_controller import auth

from authors_app.controllers.auth.book_controller import books
from authors_app.controllers.auth.company_controller import companies
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from authors_app.extensions import migrate,bcrypt
from authors_app.extensions import db



# Application Factory Function enable us to work with multiple instances
# The app instance is created under the function(def create_app():
def create_app():
    
    app=Flask(__name__)
    
   

    app.config.from_object('config.Config')  

    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    
    from authors_app.models import book
    from authors_app.models import company
    from authors_app.models import user
   

    
    
    @app.route('/')
    def home():
        return "WELCOME TO MY AUTHORS API"
    
    
    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(books, url_prefix='/api/v1/books')
    app.register_blueprint(companies, url_prefix='/api/v1/companies')
    

    
    return app


    


