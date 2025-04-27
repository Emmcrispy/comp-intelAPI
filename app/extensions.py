from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
swagger = Swagger()
