from app import app
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask import escape, request
import functools, config
import models
from database import db_insert, db_delete
from flask_login import current_user
from time import time
import datetime
from threading import Lock

# socketIO
socketio = SocketIO(app, async_mode=config.SOCKETIO_ASYNC_MODE, cors_allowed_origins='*')

# Login円滑化
login_thread = None
login_thread_lock = Lock()
login_list = {}

# socketIO上でのログインユーザー判定
def socket_auth_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

# メッセージ送信
@socketio.on('send_message')
@socket_auth_only
def send_message(json):
    # json処理
    ## タグ除外
    json['comment'] = escape(json['comment']).striptags()
    ## 情報付与
    if 'user_id' not in json:
        json['user_id'] = current_user.id
        json['name'] = current_user.name
        json['date'] = time()

    # コメント保存
    comment = models.Chat(user_id=json['user_id'], name=json['name'], comment=json['comment'], time=json['date'])
    db_insert(comment)
    
    # date変換
    json['date'] = datetime.datetime.fromtimestamp(json['date']).strftime('%I:%M:%S%p(%b %d)')
    
    # 出力
    print('received json: ' + comment.name + ':' + comment.comment)
    emit('my_response', json, broadcast=True)

# ログイン用バックグラウンド処理スレッド
def login_thread_background():
    # スレッドを保持
    while True:
        # ログイン待ちが存在する場合は実行
        if len(login_list) > 0:
            socketio.emit('login_confirm', {'confirm': 1})
            for k in list(login_list):
                # 加算・自動削除
                login_list[k] += 1
                if login_list[k] > 10: # 10秒経過で削除
                    del(login_list[k])
            # wait
            socketio.sleep(1)
        else:
            socketio.sleep(3)

# 接続
@socketio.on('connect')
@socket_auth_only
def connect():
    # ログイン円滑化スレッド立ち上げ・ID追加
    global login_list, login_thread
    login_list[request.sid] = 1
    with login_thread_lock:
        if login_thread is None:
            login_thread = socketio.start_background_task(login_thread_background)
    # wait
    socketio.sleep(0.5)
    # login表示
    json = {
        'comment': current_user.name+'(#'+current_user.id+') is activated',
        'name': 'Owner',
        'user_id': 'Bot',
        'date': time(),
    }
    send_message(json)

# 切断
@socketio.on('disconnect')
@socket_auth_only
def disconnect():
    json = {
        'comment': current_user.name+'(#'+current_user.id+') is deactivated',
        'name': 'Owner',
        'user_id': 'Bot',
        'date': time(),
    }
    send_message(json)