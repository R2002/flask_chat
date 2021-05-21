#------------------------------------------------------------#
# 設定ファイル
# instanceディレクトリにはDBへのパス、APIキーなどを記載する。
#------------------------------------------------------------#
# SQLAlchemy:
# 警告が出るので無効
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Socketio:
# 非同期処理に使用するライブラリの指定（`eventlet` or `gevent`）
SOCKETIO_ASYNC_MODE = 'eventlet'