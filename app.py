from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy()
db.init_app(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


all_books = []

with app.app_context():
    db.create_all()

with app.app_context():
    new_book_entry = Books(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book_entry)
    db.session.commit()

@app.route('/')
def home():
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        new_book = request.form.to_dict()
        all_books.append(new_book)
        print(all_books)
    return redirect(url_for('add'))


if __name__ == '__main__':
    app.run()
