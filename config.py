import os
from dotenv import load_dotenv

load_dotenv()  # carga el .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "False") == "True"

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///portfolio.db"

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
