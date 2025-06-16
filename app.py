from flask import Flask, request, send_from_directory, jsonify, render_template, redirect, url_for
import os
from pathlib import Path
import yt_dlp

app = Flask(__name__, static_folder="static", template_folder="templates")

# Folder for downloaded videos
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"status": "error", "message": "URL is missing"}), 400

        def progress_hook(d):
            if d['status'] == 'finished':
                print("✅ Download complete")

        ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    'progress_hooks': [progress_hook],
    'format': 'best',
    'merge_output_format': 'mp4',
    'cookiefile': os.path.join(os.path.dirname(__file__), 'cookies.txt')  # 👈 add this
}


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            filename_only = os.path.basename(filename)

        return jsonify({
            "status": "success",
            "filename": filename_only,
            "download_url": f"/downloads/{filename_only}"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/downloads/<path:filename>")
def serve_download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
