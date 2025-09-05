from flask import Flask
from config import DevConfig
import os
from extensions import db

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

from routes import register_routes
register_routes(app)

# Crear la base de datos si no existe
def create_db():
    db_file = DevConfig.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
    if not os.path.exists(db_file):
        with app.app_context():
            db.create_all()
            print("✨ Base de datos SQLite creada kawaii~ 💖")
    else:
        print("💖 Base de datos SQLite ya existe, todo listo~")

create_db()  # llamar directamente al iniciar app
