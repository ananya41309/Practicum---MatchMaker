from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from demodata import grants
from file_parser import parse_file  
from keyword_extractor import extract_keywords

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "csv", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        files = request.files.getlist("files")

        extracted_text = ""

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

  
                extracted_text += parse_file(file_path) + "\n"


        project_text = f"{title}\n{description}\n{extracted_text}"

        keywords = extract_keywords(project_text)

        print("EXTRACTED KEYWORDS:")
        print(keywords)


        print("PROJECT TEXT PREVIEW:")
        print(project_text[:500])

        return redirect(url_for("search"))

    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    title = request.form["title"]
    description = request.form["description"]


    results = grants

    return render_template(
        "results.html",
        results=results,
        title=title,
        description=description
    )


if __name__ == "__main__":
    app.run(debug=True)
