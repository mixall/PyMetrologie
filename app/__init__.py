from flask import Flask, _app_ctx_stack
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from .config import Config
from .db import models
from .db.database import prepare_session

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
Bootstrap(app)
# csrf = CSRFProtect()
# csrf.init_app(app)

SessionLocal, engine = prepare_session(DB_URL=Config.SQLALCHEMY_DATABASE_URI)
models.Base.metadata.create_all(bind=engine)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

from .views import views, views_user, views_meters, views_devices, views_location

# from .main import main as main_blueprint
# app.register_blueprint(main_blueprint)
#
# from .auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint, url_prefix='/auth')
#
# from .api import api as api_blueprint
# app.register_blueprint(api_blueprint, url_prefix='/api/v1')
