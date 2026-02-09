from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

#DELETE
from demodata import grants

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
        title = request.form.get("title")
        description = request.form.get("description")
        files = request.files.getlist("files")

        print("Title:", title)
        print("Description:", description)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        #return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    title = request.form["title"]
    description = request.form["description"]

    #project_text = f"{title} {description}"

    results = grants #match_grants(project_text, grants)

    return render_template("results.html", results=results, title=title, description=description)


if __name__ == "__main__":
    app.run(debug=True)
