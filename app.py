import os
from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
from video_scene_splitter import main as split_video
import zipfile
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            with tempfile.TemporaryDirectory() as tmpdirname:
                file_path = os.path.join(tmpdirname, filename)
                file.save(file_path)
                
                # Process the video
                output_dir = os.path.join(tmpdirname, 'output')
                os.makedirs(output_dir, exist_ok=True)
                split_video(file_path, output_dir)
                
                # Zip the output files
                zip_path = os.path.join(tmpdirname, 'scenes.zip')
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for root, dirs, files in os.walk(output_dir):
                        for file in files:
                            zipf.write(os.path.join(root, file), file)
                
                return send_file(zip_path, as_attachment=True)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

