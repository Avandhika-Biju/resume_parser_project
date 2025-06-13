from flask import Flask, render_template, request
from resume_parser_utils import extract_text_from_file, extract_entities
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    parsed_data = {"NAME": None, "EMAIL": None, "PHONE": None, "SKILLS": []}
    if request.method == "POST":
        uploaded_file = request.files["resume"]
        if uploaded_file:
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(filepath)

            text = extract_text_from_file(filepath)
            parsed_data = extract_entities(text)

    return render_template("index.html", result=parsed_data)

if __name__ == "__main__":
    app.run(debug=True)
