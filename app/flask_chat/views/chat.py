from flask import Blueprint, render_template
import models
from flask_login import login_required, current_user
from sqlalchemy import desc
import datetime

app = Blueprint('chat', __name__)

@app.route('/chat')
@login_required
def chat():
    list_chat = models.Chat.query.order_by(desc(models.Chat.time)).limit(20).all()
    for list in list_chat:
        list.date = datetime.datetime.fromtimestamp(list.time).strftime('%I:%M:%S%p(%b %d)')
    return render_template('app/chat.html', list_chat=list_chat)