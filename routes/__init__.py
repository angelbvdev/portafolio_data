from flask import Flask
from .public_routes import public_bp
from .private_routes import private_bp

# routes/__init__.py
def register_routes(app):
    from .public_routes import public_bp
    from .private_routes import private_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(private_bp)
