from flask import Flask, jsonify, request

app = Flask(__name__)


books = [
    {
        'id': 1,
        'title': 'The Alchemist',
        'author': 'Paulo Coelho',
        'published': 1988
    },
    {
        'id': 2,
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'published': 1960
    },
    {
        'id': 3,
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'published': 1925
    }
]


@app.route('/books', methods=['GET'])
def get_all_books():
    return jsonify({'books': books})


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book)
    return jsonify({'message': 'Book not found.'}), 404


@app.route('/books', methods=['POST'])
def create_book():
    new_book = {
        'id': len(books) + 1,
        'title': request.json['title'],
        'author': request.json['author'],
        'published': request.json['published']
    }
    books.append(new_book)
    return jsonify(new_book), 201


if __name__ == '__main__':
    app.run(debug=True)
