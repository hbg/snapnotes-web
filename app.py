from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import pyrebase

config = {
        "apiKey": "AIzaSyBOYXs9OOuFDXHIx6XyOh1a7xrDpcbf6Ls",
        "authDomain": "snapnotes-258517.firebaseapp.com",
        "databaseURL": "https://snapnotes-258517.firebaseio.com",
        "storageBucket": "snapnotes-258517.appspot.com",
    }
firebase = pyrebase.initialize_app(config)
db = firebase.database()
UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def permissible(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    base = db.child("courses").get()
    courses = {}
    for course in base.each():
        courses[course.key()] = (course.val())
    return render_template("index.html", courses=courses)


@app.route('/view_note/<course_name>/<class_title>')
def view(course_name, class_title):
    _class = db.child("courses").child(course_name).child(class_title).get()
    return render_template("view.html", description=_class.val(), course_name=course_name, class_title=class_title)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        ""
        if 'file' not in request.files:
            "error"
            print("Invalid")
        file = request.files['file']
        print("Received data!")
        if file and permissible(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/')
    return render_template("form.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run()
