from flask import Flask
import config, views, models
import instance.dev.config, instance.prd.config
from database import init_database
from flask_login import LoginManager, current_user
import os
from werkzeug.routing import Rule

# create_app
def create_app():
    # Flask
    app = Flask(__name__, static_url_path='/flask_chat/static')
    # config
    app.config.from_object('config')
    app.config.from_object('instance.dev.config')
    # app.config.from_object('instance.prd.config')
    # DB初期設定
    init_database(app)
    # 出力
    return app

app = create_app()

# ルーティング設定
APP_ROOT = app.config['APPLICATION_ROOT']
if not APP_ROOT is None:
    # define custom_rule class
    class Custom_Rule(Rule):
        def __init__(self, string, *args, **kwargs):
            # check endswith '/'
            if APP_ROOT.endswith('/'):
                prefix_without_end_slash = APP_ROOT.rstrip('/')
            else:
                prefix_without_end_slash = APP_ROOT
            # check startswith '/'
            if APP_ROOT.startswith('/'):
                prefix = prefix_without_end_slash
            else:
                prefix = '/' + prefix_without_end_slash
            super(Custom_Rule, self).__init__(prefix + string, *args, **kwargs)

    # set url_rule_class
    app.url_rule_class = Custom_Rule

# ログイン関係
# ログインマネージャー
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# user_idロード
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

# Blueprint
app.register_blueprint(views.index.app, url_prefix='/')
app.register_blueprint(views.auth.app, url_prefix='/app')
app.register_blueprint(views.chat.app, url_prefix='/app')
