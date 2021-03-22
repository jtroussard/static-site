import json, os
from pathlib import Path
from flask import render_template, request, Blueprint, redirect, url_for, flash, Markup

main = Blueprint("main", __name__)

data_filename = Path("./personal_website2/website_data.json")
with open(data_filename) as file:
    data = json.load(file)

# if main section is set to not show the data object passed to jinja will be emtpy - control
@main.route("/")
@main.route("/home")
def home():
    if data:
        # fetch assests
        resume = get_resume_file(data)

        # create special variables
        address = build_address(data)

        # get website configuration settings
        website = data.get("website")
        ctrls = website.get("controls")
        images = website.get("images")

        # get section variable lists/dicts
        personal = data.get("personal")
        intr_d = build_jinja_data_dict(data, "introduction")
        smbc_d = build_jinja_data_dict(data, "social_media")
        spec_d = build_jinja_data_dict(data, "specifications")
        skil_l = build_jinja_list(data, ctrls, "professional_skills")
        expr_l = build_jinja_list(data, ctrls, "experience")
        educ_l = build_jinja_list(data, ctrls, "education")
        # refs_l

        # hard HTML sections
        if data.get("sections").get("portfolios").get("show"):
            p_entries = data.get("sections").get("portfolios").get("entries")
            p_header = build_portfolio_header(p_entries, ctrls)
            p_tabs = build_portfolio_tabs(p_entries, ctrls)

    return render_template(
        "home.html",
        data=data,
        resume=resume,
        address=address,
        website=website,
        images=images,
        personal=personal,
        intr_d=intr_d,
        smbc_d=smbc_d,
        spec_d=spec_d,
        skil_l=skil_l,
        expr_l=expr_l,
        educ_l=educ_l,
        p_entries=p_entries,
        p_header=p_header,
        p_tabs=p_tabs,
    )


# Helpers
def get_resume_file(data):
    for file in data["files"]:
        if file["name"] == "resume":
            return f"{file['filename']}.{file['extension']}"
    return "#"


def build_address(data):
    template = data.get("website").get("styles").get("address_style").get("template")
    arguments = data.get("sections").get("specifications").get("address").get("text")
    return template.format(**arguments)


def build_jinja_list(data, ctrls, section):
    entries = data.get("sections").get(section).get("entries")
    section_l = []

    if data.get("sections").get(section).get("show"):
        for entry in entries:
            if len(section_l) < ctrls.get("limits").get(section):
                section_l.append(entry)
    return section_l


def build_jinja_data_dict(data, section):
    entries = data.get("sections").get(section)
    section_d = {}

    if entries.get("show"):
        for k, v in entries.items():
            if k == "show":
                continue
            section_d[k] = v
    return section_d


def build_portfolio_header(p, ctrls):
    # build header
    header = ""
    # for each type
    first_type = True
    curr_idx = -1
    for p_type in p:
        curr_idx += 1
        # build button
        if curr_idx + 1 <= ctrls.get("limits").get("portfolio"):
            header = header + """<li class="nav-item">"""
            if first_type:
                first_type = False
                header = (
                    header
                    + f"""<a class="nav-link active" data-toggle="tab" href="#{p_type.get("href")}" role="tablist">"""
                )
            else:
                header = (
                    header
                    + f"""<a class="nav-link" data-toggle="tab" href="#{p_type.get("href")}" role="tablist">"""
                )
            header = (
                header
                + f"""<i class="{p_type.get("fa_style_prefix")} {p_type.get("fa_name")}" aria-hidden="true"></i></a></li>"""
            )
    return header


def build_portfolio_tabs(p, ctrls):
    # build tabbed pane
    tabbed_pane = ""
    card_counter = 0

    first_tab_pane = True
    # for each type
    for p_type in p:
        if first_tab_pane:
            first_tab_pane = False
            tabbed_pane = (
                tabbed_pane
                + f"""<div class="tab-pane active" id="{p_type.get('href')}"><div class="ml-auto mr-auto"><div class="row">"""
            )
        else:
            tabbed_pane = (
                tabbed_pane
                + f"""<div class="tab-pane" id="{p_type.get('href')}"><div class="ml-auto mr-auto"><div class="row">"""
            )

        # NON FUNCTIONAL FOR LOOP - determine how many cards go into each column
        card_counter = 0
        projects = p_type.get("projects")
        for card in projects:
            card_counter += 1
        col_max = round(card_counter / 2)

        current_card_index = 0
        for n in range(2):
            # build column 1
            if n == 0:
                tabbed_pane = tabbed_pane + """<div class="col-md-6">"""
                for p_card in projects:
                    # build n cards - cards close their own divs
                    card = ""
                    if current_card_index == 0 or current_card_index < col_max:
                        card = f"""<div class="cc-porfolio-image img-raised aos-init aos-animate" data-aos="fade-up" data-aos-anchor-placement="top-bottom"><a href="{p_card.get('link')}"><figure class="cc-effect"><img src="/static/images/{p_card.get('picture')}" alt="Image"/><figcaption><div class="h4">{p_card.get('title')}</div><p>{p_card.get('subtitle')}</p></figcaption></figure></a></div>"""
                        tabbed_pane = tabbed_pane + card
                        current_card_index += 1

                # close column 1
                tabbed_pane = tabbed_pane + "</div>"

            # build column two
            if n == 1:
                tabbed_pane = tabbed_pane + """<div class="col-md-6">"""

                index = len(projects) - (current_card_index)
                if index > 0:
                    for p_card in projects[index * -1 :]:
                        # build n cards
                        card = f"""<div class="cc-porfolio-image img-raised aos-init aos-animate" data-aos="fade-up" data-aos-anchor-placement="top-bottom"><a href="{p_card.get('link')}"><figure class="cc-effect"><img src="/static/images/{p_card.get('picture')}" alt="Image"/><figcaption><div class="h4">{p_card.get('title')}</div><p>{p_card.get('subtitle')}</p></figcaption></figure></a></div>"""
                        tabbed_pane = tabbed_pane + card

                # close column 2
                tabbed_pane = tabbed_pane + "</div>"

        # close tab-pane, ml-atuo, row
        tabbed_pane = tabbed_pane + "</div></div></div>"

    return tabbed_pane
