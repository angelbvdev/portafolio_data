from flask import Flask
from config import DevConfig
from extensions import db
import os

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

from routes import register_routes
register_routes(app)

# Crear tablas al iniciar el servidor
@app.before_serving
def create_tables():
    db.create_all()
    print("✨ Tablas creadas kawaii~ 💖")

if __name__ == "__main__":
    app.run(debug=True)
