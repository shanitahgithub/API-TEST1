from flask import Flask
from authors_app.extensions import db
from datetime import datetime


class Company(db.Model):
    __tablename__="companies"
    # Attributes of the User and their respective constraints  
    id = db.Column(db.Integer,primary_key= True)
    company_name = db.Column(db.String(50), unique=True)
    origin=db.Column(db.String(50), nullable=False)
    description=db.Column(db.Text(255), nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())  
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # user = db.relationship("User", backref="companies")
    # from authors_app.models.book import Book
    from sqlalchemy.orm import relationship 
    user = db.relationship('User', backref='companies')
    # user = db.relationship("User", backref="companies")
    


    def __init__(self,company_name,origin,description,user_id):
        self.company_name=company_name
        self.origin=origin
        self.description=description
        user_id=user_id
       

    def __repr__(self):
         return f'{self.company_name} {self.origin}'
    

        

    