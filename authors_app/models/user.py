from flask import Flask
from authors_app.extensions import db
from datetime import datetime




class User(db.Model):
    __tablename__="users"
    # Attributes of the User and their respective constraints  
    id = db.Column(db.Integer,primary_key= True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name=db.Column(db.String(50), nullable=False)
    email   = db.Column(db.String(20), nullable=False , unique=True)
    
    contact  =db.Column(db.String(255), nullable=False,unique=True)
    image=db.Column(db.String(255), nullable=True )
    biography=db.Column(db.Text(255), nullable=True )
    user_type=db.Column(db.String(50), default='author')
    password = db.Column(db.Text(255), nullable=False , unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())  
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    # books = relationship("Book", backref="user", cascade="all, delete-orphan")

    

    # companies = db.relationship("Company", backref="users")

# Creating a constructor for the user model
    
    def __init__(self,first_name,last_name,biography,user_type,password,contact,email,image=None):
        self.first_name=first_name
        self.last_name=last_name
        self.email= email
        self.contact= contact
        self.image= image
        self.biography=biography
        self.password=password
        self.user_type=user_type

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'




































    
    







       

