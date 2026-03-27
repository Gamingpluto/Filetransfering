from flask import Flask, request, send_from_directory, redirect
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    files = os.listdir(UPLOAD_FOLDER)

    html = '''
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

    .container {
        margin-top: 50px;
    }

    input, button {
        padding: 10px;
        margin: 10px;
        border-radius: 8px;
        border: none;
    }

    button {
        background: #22c55e;
        color: white;
        cursor: pointer;
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
    <div class="container">

    <h2>📁 File Transfer System</h2>

    <<form id="uploadForm">
    <input type="file" id="fileInput">
    <button type="submit">Upload</button>
</form>

<p id="status"></p>
<progress id="progressBar" value="0" max="100"></progress>
    <h3>Files:</h3>
    '''

    # ✅ LOOP INSIDE FUNCTION
    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file)
        size = os.path.getsize(path) // 1024

        html += f'''
        <div class="file">
            <a href="/download/{file}">{file}</a> ({size} KB)
            <a href="/delete/{file}">
                <button>Delete</button>
            </a>
        </div>
        '''
        <script>
document.getElementById("uploadForm").onsubmit = async (e) => {
    e.preventDefault();

    let file = document.getElementById("fileInput").files[0];
    let formData = new FormData();
    formData.append("file", file);

    document.getElementById("status").innerText = "Uploading...";

    await fetch("/", {
        method: "POST",
        body: formData
    });

    document.getElementById("status").innerText = "Upload Done!";
    loadFiles(); // refresh file list
};
</script>

<script>
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

    xhr.open("POST", "/");
    xhr.send(formData);
};
</script>
setInterval(loadFiles, 3000);

    # ✅ CLOSE HTML
    html += '''
    </div>
    </body>
    </html>
    '''

    return html


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/api/files')
def api_files():
    files = os.listdir(UPLOAD_FOLDER)
    return {"files": files}

@app.route('/delete/<filename>')
def delete_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect('/')




if __name__ == "__main__":
    app.run()
