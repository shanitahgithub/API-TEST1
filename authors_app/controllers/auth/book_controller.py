from flask import Blueprint,request, jsonify
from authors_app.models.book import Book
from authors_app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from authors_app.models.user import User

# Creating a blueprint
books= Blueprint('books', __name__, url_prefix='/api/v1/books')

# Defining the creation endpoint
@books.route('/create', methods=["POST"])
@jwt_required()
def create_book():
    try:
        # Extracting user data from the request JSON
        title = request.json.get("title")
        description = request.json.get("description")
        price = request.json.get("price")
        image = request.json.get("image")
        pages = request.json.get("pages")
        # user_id = request.json.get("user_id")
        company_id = request.json.get("company_id")
        isbn= request.json.get("isbn")
        genre=request.json.get('genre')
        
        current_user_id = get_jwt_identity()
        print("Token Identity:", current_user_id)
        
        user_id = current_user_id 



        # Validating input data
        if not all([title, description, price, image, pages,  isbn, genre, ]):
            return jsonify({"error": 'All fields are required'}), 400
        

        # Creating a new instance of the Book model
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

        # Adding the new book instance to the database session
        db.session.add(new_book)

        # Committing the session to save the changes to the database
        db.session.commit()

        # Returning a success response
        return jsonify({'message': 'Book created successfully',
                        'book':{
                            'book_id':new_book.id,
                            'title':new_book.title,
                            'description':new_book.description,
                            'price':new_book.price,
                            'image':new_book.image,
                            'pages':new_book.pages,
                            'company_id':new_book.company_id,
                            'user_id':new_book.user_id,
                            'isbn':new_book.isbn,
                            'genre':new_book.genre}}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)})

#  Editing a book
@books.route('/edit/<int:id>', methods=["PUT"])
@jwt_required()  # Ensuring a valid JWT token is provided
def edit_book(id):
    try:
        # Extracting user_id from the JWT token
        user= get_jwt_identity()

        # Extracting book data from the request JSON
        data = request.json
        book= Book.query.filter_by(id=id,user_id=user).first()
        if not book:
            return jsonify({'error': 'You have no access to this book'}), 404

        # Updating book fields 
        if 'title' in data:
            book.title = data['title']
        if 'description' in data:
            book.description = data['description']
        if 'price' in data:
            book.description = data['book']
        if 'image' in data:
            book.image = data['image']
        if 'pages' in data:
            book.pages = data['pages']
        if 'user_id' in data:
            book.user_id = data['user_id']
        if 'company_id' in data:
            book.company_id = data['company_id']
        if 'isbn' in data:
            book.isbn = data['isbn']
        if 'genre' in data:
            book.genre = data['genre']

        # Committing the session to save the changes to the database
        db.session.commit()

        # Returning a success response
        return jsonify({'message': 'Book updated successfully',
'book':{
                            'title':book.title,
                            'description':book.description,
                            'price':book.price,
                            'image':book.image,
                            'pages':book.pages,
                            'company_id':book.company_id,
                            'user_id':book.user_id,
                            'isbn':book.isbn,
                            'genre':book.genre}})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500  
    
# Deleting book
@books.route('/delete/<int:id>', methods=["DELETE"])
@jwt_required()  # Ensuring a valid JWT token is provided
def delete_book(id):
    try:
        # Extracting user_id from the JWT token
        user= get_jwt_identity()

        # Retrieving the book to delete
        book= Book.query.filter_by(id=id,user_id=user).first()
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # Deleting the book
        db.session.delete(book)
        db.session.commit()

        return jsonify({'message': 'Book has been deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Getting all books
@books.route('/allBooks', methods=["GET"])
@jwt_required()  # Ensuring a valid JWT token is provided
def get_all_books():
    try:
        # Extracting user_id from the JWT token
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401


        # Querying all books from the database
        allBooks = Book.query.all()

        # Serializing books data
        serialized_allBooks = []
        for book in allBooks:
            serialized_book = {
                'id':book.id,
                'title': book.title,
                'image': book.image,
                'description': book.description,
                'price': book.price,
                'user_id': book.user_id,
                'pages': book.pages,
                'isbn': book.isbn,
                'company_id': book.company_id,
                'user_id': book.user_id,
                'genre': book.genre,
            }
            serialized_allBooks.append(serialized_book)

        # Returning the serialized books data
        return jsonify({'books': serialized_allBooks}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Getting a specific book
@books.route('/book/<int:id>', methods=["GET"])
@jwt_required()  # Ensuring a valid JWT token is provided
def get_book(id):
    try:
        # Extracting  user_id from the JWT token
        user = get_jwt_identity()

        # Retrievig the user
        
        book= Book.query.filter_by(id=id,user_id=user).first()
        

        # Checking if the book exists
        if not book:
            return jsonify({'error': 'You have no access to this book'}), 404

        
        # Serializing book data
        serialized_book = {
                'id': book.id,
                'title': book.title,
                'image': book.image,
                'description': book.description,
                'price': book.price,
                'user_id': book.user_id,
                'pages': book.pages,
                'isbn': book.isbn,
                'company_id': book.company_id,
                'user_id': book.user_id,
                'genre': book.genre,
        }

        # Returning the serialized book data
        return jsonify({'book': serialized_book}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500   


   


    