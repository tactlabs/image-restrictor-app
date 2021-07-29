from flask import Flask,render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename
import urllib.request
import os

app = Flask(__name__)
PORT = 3000
UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "34c75cac10fb587135e2b27ef5765007"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] =  16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png' , 'jpg' ,'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/',methods=["GET","POST"])
def upload_image():
    if 'file' not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("No image selected for uploading!")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        flash("Image successfully uploaded and displayed below")
        return render_template("index.html",filename = filename)
    else:
        flash("Images with size (120 x 120) or (140 x 120) are only allowed! ")
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static',filename='uploads/' + filename),code=301)

if __name__ == '__main__':
    app.run(debug=True,port=PORT)