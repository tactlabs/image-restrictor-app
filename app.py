from flask import Flask,render_template,request,redirect,flash
import os
from werkzeug.utils import secure_filename
from PIL import Image


app = Flask(__name__)
PORT = 3000

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "34c75cac10fb587135e2b27ef5765007"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     

@app.route('/',methods=["GET","POST"])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part!")
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash("No image selected for uploading!")
            return redirect(request.url)

        # if file.filename  != '':
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'img.jpg'))
            image =Image.open("static/uploads/img.jpg")  
            width1, height1 = image.size
            if width1 == 120 and  height1 == 120:
                # return "File uploaded successfully!"
                return render_template("result.html",width1 = width1 , height1 =height1)
            elif width1 == 140 and height1 == 120:
                return render_template("result.html",width1 = width1 , height1 =height1)

            else:
                return "<h3>Error...!! image must be exactly in this size only (120 X 120) or (140 X 120).</h3>"
        else:
            flash('Only image files are allowed to upload!! allowed types are - (png, jpg, jpeg)')
            return redirect(request.url)    
    else:
        return render_template("index.html")        

     
            
if __name__ == '__main__':
    app.run(debug=True,port=PORT)