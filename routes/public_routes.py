from flask import Blueprint, render_template
from extensions import db
from models import Project

# Definimos el blueprint kawaii~
public_bp = Blueprint('public', __name__)

@public_bp.route("/")
def index():
    projects = Project.query.all()
    return render_template("index.html", projects=projects)

@public_bp.route("/about")
def about():
    return render_template("about.html")

@public_bp.route("/projects")
def projects():
    projects = Project.query.all()
    return render_template("projects.html", projects=projects)

@public_bp.route("/project/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("project_detail.html", project=project)

@public_bp.route("/contact")
def contact():
    return render_template("contact.html")
