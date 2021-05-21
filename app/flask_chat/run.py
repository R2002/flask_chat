from app_socket import app as application
from app_socket import socketio

if __name__ == '__main__':
    # config
    # print(application.config)

    # ルーティング設定
    # print(application.url_map)

    # run
    # application.run()
    socketio.run(application)