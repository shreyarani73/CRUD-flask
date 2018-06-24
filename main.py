import os
from flask import Flask, render_template, session, redirect
from flask import request
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "main.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/library'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class Book(db.Model):
	ISBN = db.Column(db.Integer,unique=True,primary_key=True)
	BookName = db.Column(db.String(10),unique=True,primary_key=False)
	Author = db.Column(db.String(10),unique=True,primary_key=False)

	def __repr__(self):
		return "<ISBN: {}, BookName: {}, Author: {}>".format(self.ISBN,self.BookName,self.Author)


@app.route("/", methods=["GET","POST"])
def home():
    # return "My Flask app"
    books = None
    if request.form:
    	# print(request.form)
    	try:
    		book = Book(ISBN=request.form.get("ISBN"), BookName=request.form.get("BookName"),Author=request.form.get("Author"))
    		db.session.add(book)
    		db.session.commit()
    	except Exception as e:
    		db.session().rollback()
    		print("Failed to add book")
    		print(e)
    books= Book.query.all()
    return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
	try:
		newISBN = request.form.get("newISBN")
		oldISBN = request.form.get("oldISBN")
		book = Book.query.filter_by(ISBN=oldISBN).first()
		book.ISBN = newISBN
		db.session.commit()
		newBookName = request.form.get("newBookName")
		oldBookName = request.form.get("oldBookName")
		book = Book.query.filter_by(BookName=oldBookName).first()
		book.BookName = newBookName
		db.session.commit()
		newAUTHOR = request.form.get("newAUTHOR")
		oldAUTHOR = request.form.get("oldAUTHOR")
		book = Book.query.filter_by(AUTHOR=oldAUTHOR).first()
		book.AUTHOR = newAUTHOR
		db.session.commit()
	except Exception as e:
		print("Counldn't update book title")
		print(e)
	finally:
		return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    ISBN = request.form.get("ISBN")
    book = Book.query.filter_by(ISBN=ISBN).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

# @app.route('/')
# def testdb():
    # if db.session.query('1').from_statement('SELECT 1').all():
        # return 'It works.'
    # else:
        # return 'Something is broken.'
if __name__ == "__main__":
    app.run(debug=True)