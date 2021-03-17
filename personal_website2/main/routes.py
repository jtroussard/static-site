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
        portfolio_data = build_distinct_portfolio_type_data(data)
    return render_template("home.html", data=data, resume=resume, portfolio_data=portfolio_data)

# Helpers
def get_resume_file(data):
    for file in data['files']:
        if file['name'] == "resume":
            print(f"{file['filename']}.{file['extension']}")
            return f"{file['filename']}.{file['extension']}"
    return "#"

def build_distinct_portfolio_type_data(data):
    distinct_types_list = []
    distinct_types = []
    for portfolio in data['portfolios']:
        if portfolio['project_type'] not in distinct_types:
            distinct_type_data = {
                "project_type": "",
                "project_img": "",
                "project_color": ""
            }
            distinct_type_data['project_type'] = portfolio['project_type']
            distinct_type_data['project_img'] = portfolio['project_img']
            distinct_type_data['project_color'] = portfolio['project_color']
            distinct_types_list.append(distinct_type_data)
            distinct_types.append(portfolio['project_type'])
    return distinct_types_list

