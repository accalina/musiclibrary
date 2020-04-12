
import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_socketio import SocketIO, emit, send
from util.youtube import download_mp3


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

app = CustomFlask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('message', message, broadcast=True)

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/file', methods=['GET', 'POST'])
def filemanager():
    if request.method == "GET":
        data = []
        for filename in os.listdir('static/music'):
            fileinfo = filename.split('-')
            data.append({"name": "-".join(fileinfo[:-1]), "link": "https://www.youtube.com/watch?v="+fileinfo[-1], "filepath": filename})
        return jsonify({"data": data})

    if request.method == "POST":
        url = request.form.get('url', '')
        if url:
            download_mp3(url)
            return jsonify({"msg": "Download in progress..."})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')