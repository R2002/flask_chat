from flask import Blueprint, render_template
import models

app = Blueprint('index', __name__)

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/websocket')
def websocket():
    return render_template('pages/websocket.html')
