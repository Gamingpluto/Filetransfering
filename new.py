from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🌐 MAIN PAGE
@app.route('/')
def index():
    return '''
<html>
<head>
<title>File Transfer</title>

<style>
body {
    margin: 0;
    font-family: Arial;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.container {
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 30px;
    width: 380px;
    box-shadow: 0 0 40px rgba(0,0,0,0.5);
}

/* DROP AREA */
#drop-area {
    border: 2px dashed rgba(255,255,255,0.3);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    transition: 0.3s;
}

#drop-area.hover {
    background: rgba(255,255,255,0.1);
}

button {
    background: rgba(34,197,94,0.8);
    border: none;
    padding: 10px;
    border-radius: 10px;
    color: white;
    cursor: pointer;
}

.delete {
    background: rgba(239,68,68,0.8);
}

/* FILE CARDS */
.card {
    background: rgba(255,255,255,0.05);
    margin: 10px 0;
    padding: 12px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>

</head>

<body>

<div class="container">

<h2>📁 File Transfer</h2>

<div id="drop-area">
    <p>📤 Drag & Drop Files Here</p>
    <input type="file" id="fileInput">
    <button onclick="uploadFile()">Upload</button>
</div>

<progress id="progressBar" value="0" max="100"></progress>
<p id="status"></p>

<div id="fileList"></div>

</div>

<script>

// 📂 ICON DETECTION
function getIcon(file) {
    let ext = file.split('.').pop().toLowerCase();

    if (["png","jpg","jpeg","gif"].includes(ext)) return "🖼️";
    if (["mp4","mkv","avi"].includes(ext)) return "🎬";
    if (["mp3","wav"].includes(ext)) return "🎵";
    if (["pdf"].includes(ext)) return "📄";
    return "📁";
}

// 📥 LOAD FILES
async function loadFiles() {
    let res = await fetch('/api/files');
    let data = await res.json();

    let html = "";
    data.files.forEach(file => {
        html += `
        <div class="card">
            <span>${getIcon(file)} 
            <a href="/download/${file}" style="color:white;">${file}</a></span>
            <button class="delete" onclick="deleteFile('${file}')">✖</button>
        </div>`;
    });

    document.getElementById("fileList").innerHTML = html;
}

// ❌ DELETE FILE
async function deleteFile(file) {
    await fetch('/delete/' + file);
    loadFiles();
}

// 📤 UPLOAD FILE
function uploadFile(file = null) {
    let selected = file || document.getElementById("fileInput").files[0];
    if (!selected) return;

    let formData = new FormData();
    formData.append("file", selected);

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
}

// 🖱️ DRAG & DROP
let dropArea = document.getElementById("drop-area");

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("hover");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("hover");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("hover");

    let file = e.dataTransfer.files[0];
    uploadFile(file);
});

loadFiles();
setInterval(loadFiles, 3000);

</script>

</body>
</html>
'''

# 📤 UPLOAD ROUTE
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return "OK"

# 📂 FILE LIST API
@app.route('/api/files')
def api_files():
    return jsonify({"files": os.listdir(UPLOAD_FOLDER)})

# 📥 DOWNLOAD
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# ❌ DELETE
@app.route('/delete/<filename>')
def delete_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    return "Deleted"

# ▶️ RUN

if __name__ == "__main__":
    app.run()
