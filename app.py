from flask import Flask
from config import DevConfig
import os
from extensions import db  # importamos la db desde extensions

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)  # inicializamos SQLAlchemy con la app, no creamos una nueva

# Registrar rutas al final, después de db y modelos
from routes import register_routes
register_routes(app)

if __name__ == "__main__":
    # Crear la base de datos si no existe kawaii~
    with app.app_context():
        db_file = DevConfig.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
        if not os.path.exists(db_file):
            db.create_all()
            print("✨ Base de datos SQLite creada kawaii~ 💖")
        else:
            print("💖 Base de datos SQLite ya existe, todo listo~")

    app.run(debug=True)
