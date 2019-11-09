from flask import Flask, render_template
import pyrebase
app = Flask(__name__)


@app.route('/')
def home():
    config = {
        "apiKey": "AIzaSyBOYXs9OOuFDXHIx6XyOh1a7xrDpcbf6Ls",
        "authDomain": "snapnotes-258517.firebaseapp.com",
        "databaseURL": "https://snapnotes-258517.firebaseio.com",
        "storageBucket": "snapnotes-258517.appspot.com",
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    base = db.child("courses").get()
    courses = {}
    for course in base.each():
        courses[course.key()] = (course.val())
    return render_template("index.html", courses=courses)


if __name__ == '__main__':
    app.run()
