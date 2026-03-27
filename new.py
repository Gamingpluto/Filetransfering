from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return '''
    <html>
    <head>
    <title>File Transfer</title>

    <style>
    body {
        font-family: Arial;
        background: #0f172a;
        color: white;
        text-align: center;
    }

    .file {
        margin: 10px;
        padding: 10px;
        background: #1e293b;
        border-radius: 10px;
    }
    </style>

    </head>

    <body>

    <h2>📁 File Transfer</h2>

    <form id="uploadForm">
        <input type="file" id="fileInput">
        <button>Upload</button>
    </form>

    <p id="status"></p>
    <progress id="progressBar" value="0" max="100"></progress>

    <h3>Files:</h3>
    <div id="fileList"></div>

    <script>
    async function loadFiles() {
        let res = await fetch('/api/files');
        let data = await res.json();

        let html = "";
        data.files.forEach(file => {
            html += `
            <div class="file">
                <a href="/download/${file}">${file}</a>
            </div>`;
        });

        document.getElementById("fileList").innerHTML = html;
    }

    document.getElementById("uploadForm").onsubmit = (e) => {
        e.preventDefault();

        let file = document.getElementById("fileInput").files[0];
        let formData = new FormData();
        formData.append("file", file);

        let xhr = new XMLHttpRequest();

        xhr.upload.onprogress = (e) => {
            let percent = (e.loaded / e.total) * 100;
            document.getElementById("progressBar").value = percent;
        };

        xhr.onload = () => {
            document.getElementById("status").innerText = "Upload Done!";
            loadFiles();
        };

        xhr.open("POST", "/upload");
        xhr.send(formData);
    };

    loadFiles();
    setInterval(loadFiles, 3000);
    </script>

    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return "OK"

@app.route('/api/files')
def api_files():
    return jsonify({"files": os.listdir(UPLOAD_FOLDER)})

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run()
