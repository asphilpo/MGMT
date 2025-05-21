from flask import Flask, jsonify, request, send_from_directory, render_template, render_template_string
import os
from secret_config import UPLOAD_SECRET


app = Flask(__name__)

UPLOAD_FOLDERS = {
    'image': "static/images/",
    'report' : "static/reports/",
}

REPORTS_DIR = os.path.join(os.getcwd(), './static/reports/')


@app.route('/upload/<filetype>', methods=['POST'])
def upload_file(filetype):
    token = request.headers.get("Authorization")
    if token != f"Bearer {UPLOAD_SECRET}":
        return jsonify({"error": "Unauthorized Upload"}), 401
        
    if filetype not in UPLOAD_FOLDERS:
        return jsonify({'error': 'Invalid File Type'}), 400
    file = request.files.get("file")
    if not file or file.filename == '':
        return jsonify({'error' : 'No File Uploaded'}), 400
    save_path = os.path.join(UPLOAD_FOLDERS[filetype], file.filename)
    file.save(save_path)
    return jsonify({'success': True, 'filename': file.filename}), 200

@app.route('/reports/')
def list_reports():
    files = sorted(os.listdir(REPORTS_DIR))
    links = [
        f'<a href="{filename}">{filename}</a><br>'
        for filename in files if filename.endswith('.csv')
    ]
    return render_template_string(''.join(links))


@app.route('/reports/<path:filename>')
def serve_report(filename):
    return send_from_directory(REPORTS_DIR, filename)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/content')
def content():
    return render_template("content.html")

@app.route('/whatsnew')
def whats_new():
    return render_template("whatsnew.html")

def run():
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    
if __name__ == '__main__':
    run()
    
