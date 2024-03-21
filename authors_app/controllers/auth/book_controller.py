from flask import Blueprint,request, jsonify
from authors_app.models.book import Book
from authors_app.extensions import db

# Creating a blueprint
books= Blueprint('books', __name__, url_prefix='/api/v1/books')

# Defining the registration endpoint
@books.route('/register', methods=["POST"])
def register():
    try:
        # Extract user data from the request JSON
        title = request.json["title"]
        description = request.json["description"]
        price = request.json["price"]
        image = request.json["image"]
        pages = request.json["pages"]
        user_id = request.json["user_id"]
        company_id = request.json["company_id"]
        isbn= request.json["isbn"] 
        genre=request.json['genre']



        # Validate input data
        if not all([title, description, price, image, pages,  isbn, genre, user_id]):
            return jsonify({"error": 'All fields are required'}), 400
        

        # Create a new instance of the User model
        new_book = Book(
            title=title,
            description=description,
            price=price,
            image=image,
            pages=pages,
            company_id=company_id,
            user_id=user_id,
            isbn=isbn,
            genre=genre,
               
        )

        # Add the new user instance to the database session
        db.session.add(new_book)

        # Commit the session to save the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'Book created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)})


