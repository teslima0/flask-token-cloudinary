from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.uploader
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
load_dotenv()

app= Flask(__name__)
CORS(app)
db = SQLAlchemy()
def create_app():
    #app= Flask(__name__)
    #db = SQLAlchemy()
    app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db" 
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost/flask-img' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
   
    db.init_app(app)
    jwt = JWTManager(app)

    cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('API_KEY'),
    api_secret = os.getenv('API_SECRET'),
    )


    from .import models

    with app.app_context():
        db.create_all()


    
    #register view
    from .views import views
    from .auths import auths

    app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(deletes, url_prefix='/')
    app.register_blueprint(auths, url_prefix='/')
    
    return app
