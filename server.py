import os
import hashlib

from flask import Flask, redirect, request, render_template, url_for, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.instance_path, 'images')
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        filename, extension = file.filename.rsplit('.', 1)
        file.filename = hashlib.md5(filename.encode('utf-8')).hexdigest() + '.' + extension
        filename = photos.save(file)
        return redirect(url_for('uploaded_file', filename=filename))

    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)
