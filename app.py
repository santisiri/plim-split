import os
from flask import Flask, request, render_template, send_from_directory, Response
from video_scene_splitter import split_video, detect_scenes
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_progress():
    def progress_callback(progress, status):
        yield f"data: {json.dumps({'progress': progress, 'status': status})}\n\n"

    return progress_callback

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            def generate():
                progress_cb = generate_progress()
                # First detect scenes
                scenes = detect_scenes(file_path)
                # Then split the video using detected scenes
                split_video(file_path, scenes, OUTPUT_FOLDER, progress_callback=progress_cb)
                
                # Send the list of generated scenes
                scene_files = os.listdir(OUTPUT_FOLDER)
                yield f"data: {json.dumps({'scenes': scene_files})}\n\n"
            
            return Response(generate(), mimetype='text/event-stream')
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

