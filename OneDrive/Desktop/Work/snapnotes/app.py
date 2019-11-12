from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import pyrebase
from flask_wtf.csrf import CSRFProtect

config = {
        "apiKey": os.environ.get("API_KEY"),
        "authDomain": "snapnotes-258517.firebaseapp.com",
        "databaseURL": "https://snapnotes-258517.firebaseio.com",
        "storageBucket": "snapnotes-258517.appspot.com",
    }
firebase = pyrebase.initialize_app(config)
db = firebase.database()
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
SECRET_KEY = os.environ.get("SECRET_KEY", "adji31802jkasdaqwQ21")
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def permissible(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def detect_document_uri(uri, course):
    """Detects document features in the file located in Google Cloud
    Storage."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)
    print(uri, response.text_annotations)
    if len(response.text_annotations) > 0:
        total = response.text_annotations[0].description
        title = total.split("\n", 1)[0]
        content = total.split("\n", 1)[1]
        print(title, content)
        db.child("courses").child(course).child(title).set(content)


@app.route('/')
def home():
    base = db.child("courses").get()
    courses = {}
    for course in base.each():
        courses[course.key()] = (course.val())
    return render_template("index.html", courses=courses, home=True)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/view_note/<course_name>/<class_title>')
def view(course_name, class_title):
    _class = db.child("courses").child(course_name).child(class_title).get()
    return render_template("view.html", description=_class.val(), course_name=course_name, class_title=class_title)


@app.route('/edit/<course_name>/<class_title>', methods=['GET','POST'])
def edit(course_name, class_title):
    if request.method == "POST":
        db.child("courses").child(course_name).update({class_title: request.form['newText']})
        return redirect('/view_note/{}/{}'.format(course_name, class_title))
    _class = db.child("courses").child(course_name).child(class_title).get()
    return render_template("edit.html", description=_class.val(), course_name=course_name, class_title=class_title)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        ""
        if 'file' not in request.files:
            "error"
            print("Invalid")
        file = request.files['file']
        course = request.form['courseName']
        print("Received data!")
        if file and permissible(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = "http://snapnotes-cutie.herokuapp.com/static/uploads/"+filename
            detect_document_uri(image_url, course)
            return redirect('/')
    return render_template("form.html", home=False)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run()
