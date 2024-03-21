from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager




from flask_sqlalchemy import SQLAlchemy
# from authors_app.extensions import db,migrate



db=SQLAlchemy()
migrate= Migrate()
bcrypt=Bcrypt()
jwt = JWTManager()