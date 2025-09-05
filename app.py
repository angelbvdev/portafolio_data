from flask import Flask
from config import DevConfig
import os
from extensions import db  # importamos la db desde extensions

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)  # inicializamos SQLAlchemy con la app

# Registrar rutas
from routes import register_routes
register_routes(app)

# Crear tablas automáticamente al primer request (útil para Render gratis)
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
