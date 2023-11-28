from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        book_title = request.form['title']
        book_author = request.form['author']
        book_rating = request.form['rating']
        print(book_title, book_author, book_rating)
    return redirect(url_for('add'))


if __name__ == '__main__':
    app.run()
