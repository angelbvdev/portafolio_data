from extensions import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.Text, nullable=True)                
    image = db.Column(db.String(200), nullable=True)      
    status = db.Column(db.String(50), default="En progreso")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_file = db.Column(db.String(200), nullable=True)   
    github_url = db.Column(db.String(250), nullable=True)   
