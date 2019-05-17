#upload this to git

import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, render_template, send_file, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'mp3', 'mp4',
                            'webm'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('[File successfully uploaded]')
            return redirect(url_for('upload_form'))
        else:
            flash('[wrong file format]')
            return redirect(url_for('upload_form'))


@app.route('/files', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):


    # Joining the base and the requested path
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        #return abort(404)
        return render_template('404.html'), 404 #TODO better 404 page

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)


    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files)

if __name__ == "__main__":
    app.run(debug=True)