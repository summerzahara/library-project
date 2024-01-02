from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from icecream import ic

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-books-collection.db"
db = SQLAlchemy()
db.init_app(app)


# db.session.close_all()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


# all_books = []

with app.app_context():
    db.create_all()


# with app.app_context():
# new_book_entry = Books(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
# db.session.add(new_book_entry)
# db.session.commit()

@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Books).order_by(Books.title))
        all_books = result.scalars().all()
        rows = len(all_books)
        ic(rows)
    return render_template('index.html', books=all_books, rows=rows)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        new_book = request.form.to_dict()
        ic(new_book)
        with app.app_context():
            new_book_entry = Books(title=new_book["title"], author=new_book["author"], rating=new_book["rating"])
            db.session.add(new_book_entry)
            db.session.commit()
    return redirect(url_for('add'))


@app.route("/edit/<row_id>", methods=['GET', 'POST'])
def edit(row_id):
    if request.method == 'GET':
        with app.app_context():
            book = db.session.execute(db.select(Books).where(Books.id == row_id)).scalar()
        return render_template('edit.html', book=book)
    if request.method == 'POST':
        with app.app_context():
            new_rating = request.form.to_dict()
            book = db.session.execute(db.select(Books).where(Books.id == row_id)).scalar()
            book.rating = new_rating["new_rating"]
            db.session.commit()
        return redirect(url_for("home"))

@app.route("/delete/<row_id>")
def delete(row_id):
    with app.app_context():
        delete_book = db.session.execute(db.select(Books).where(Books.id == row_id)).scalar()
        db.session.delete(delete_book)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run()
