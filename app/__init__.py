from flask import Flask

from config import Config
from app.extensions import db, migrate, login_manager

def create_app(config_class = Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialize Flask Extension here
    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register Blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session().query(User).get(int(user_id))

    return app
 