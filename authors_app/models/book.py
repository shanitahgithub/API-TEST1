
from sqlalchemy.orm import relationship
from authors_app.extensions import db


from datetime import datetime



class Book(db.Model):
    __tablename__ = "books"  
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    image = db.Column(db.String(255))
    price = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'),nullable=False) 
    isbn=db.Column(db.String(30),nullable=False,unique=False)
    genre=db.Column(db.String(30),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())  
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    from authors_app.models.user import User
    # users = db.relationship("User", backref="books")  # Define the relationship with the User model
    # companies = relationship("Company", backref="books")
    

    # company = db.relationship('Company', backref=db.backref("books", lazy=True))
    


    def __init__(self, title, description,isbn,genre,company_id,price, pages, user_id,image=None):
        self.title = title
        self.description = description
        self.price=price
        self.pages=pages
        self.user_id = user_id
        
        self.image=image
        self.company_id = company_id
        self.isbn = isbn
        self.genre = genre


    def __repr__(self):
        return f'{self.title},{self.description}>'
