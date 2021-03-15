import json, os
from pathlib import Path
from flask import render_template, request, Blueprint, redirect, url_for, flash, Markup

main = Blueprint("main", __name__)

data_filename = Path("./personal_website2/data.json")
with open(data_filename) as file:
    data = json.load(file)

@main.route("/")
@main.route("/home")
def home():
    if data:
        resume = get_resume_file(data)
    return render_template("home.html", data=data, resume=resume)

# Helpers
def get_resume_file(data):
    for file in data['files']:
        if file['name'] == "resume":
            print(f"{file['filename']}.{file['extension']}")
            return f"{file['filename']}.{file['extension']}"
    return "#"

