from flask import Blueprint, request, redirect, url_for, render_template, current_app, flash
from functools import wraps
from extensions import db
from models import Project
import os
import uuid
from werkzeug.utils import secure_filename

private_bp = Blueprint('private', __name__)

# Decorador admin kawaii
def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != os.getenv("ADMIN_USER") or auth.password != os.getenv("ADMIN_PASS"):
            return ("No autorizado", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated

# ================================
# Configuración de subida
# ================================
IMAGE_UPLOAD_FOLDER = 'static/img'
REPORT_UPLOAD_FOLDER = 'static/reports'

ALLOWED_IMAGE_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_REPORT_EXT = {'pdf', 'doc', 'docx'}

def ensure_dirs():
    os.makedirs(os.path.join(current_app.root_path, IMAGE_UPLOAD_FOLDER), exist_ok=True)
    os.makedirs(os.path.join(current_app.root_path, REPORT_UPLOAD_FOLDER), exist_ok=True)

def allowed_ext(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

def save_upload(file_storage, dest_folder, prefix):
    """
    Guarda un FileStorage en /static/... con nombre único.
    Retorna:
      - rel_for_static: ruta relativa para url_for('static', filename=...)
      - unique_name: nombre único del archivo (sin carpeta)
    """
    original = secure_filename(file_storage.filename)
    ext = original.rsplit('.', 1)[1].lower()
    unique_name = f"{prefix}-{uuid.uuid4().hex}.{ext}"
    abs_dir = os.path.join(current_app.root_path, dest_folder)
    os.makedirs(abs_dir, exist_ok=True)
    abs_path = os.path.join(abs_dir, unique_name)
    file_storage.save(abs_path)
    rel_for_static = f"{os.path.basename(dest_folder)}/{unique_name}"  # p.ej. 'img/...' o 'reports/...'
    return rel_for_static, unique_name

# =========================================================
# Ruta para agregar proyecto con imagen, reporte y GitHub
# =========================================================
@private_bp.route("/add_project", methods=["GET", "POST"])
@admin_only
def add_project():
    if request.method == "POST":
        ensure_dirs()

        title = (request.form.get("title") or "").strip()
        summary = (request.form.get("summary") or "").strip()
        github_url = (request.form.get("github_url") or "").strip()

        # =======================
        # Imagen (opcional)
        # =======================
        image_fs = request.files.get("image")
        image_filename_only = None  # tu template hace: 'img/' + project.image

        if image_fs and image_fs.filename:
            if not allowed_ext(image_fs.filename, ALLOWED_IMAGE_EXT):
                flash("Formato de imagen no permitido. Usa png/jpg/jpeg/gif/webp.", "warning")
                return redirect(request.url)
            # Guardamos y almacenamos solo el nombre (no la carpeta)
            rel_path_img, unique_img = save_upload(image_fs, IMAGE_UPLOAD_FOLDER, prefix="img")
            image_filename_only = unique_img

        # =======================
        # Reporte (opcional)
        # =======================
        report_fs = request.files.get("report_file")
        report_relpath = None  # se usará con url_for('static', filename=project.report_file)

        if report_fs and report_fs.filename:
            if not allowed_ext(report_fs.filename, ALLOWED_REPORT_EXT):
                flash("Formato de reporte no permitido. Usa pdf/doc/docx.", "warning")
                return redirect(request.url)
            rel_path_report, _ = save_upload(report_fs, REPORT_UPLOAD_FOLDER, prefix="report")
            report_relpath = rel_path_report  # p.ej. 'reports/report-uuid.pdf'

        # =======================
        # Crear proyecto
        # =======================
        new_project = Project(
            title=title,
            summary=summary,
            image=image_filename_only,
            github_url=github_url if github_url else None,
            report_file=report_relpath if report_relpath else None,
        )

        db.session.add(new_project)
        db.session.commit()

        flash("Proyecto creado con éxito ✨", "success")
        return redirect(url_for("public.projects", project_id=new_project.id))

    return render_template("add_project.html")
