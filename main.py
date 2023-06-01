
import os
from flask import Flask,  make_response, render_template, request, send_file
import webbrowser
import subprocess
import sys

class _Directory:
    def __init__(self, basedir, relpath=''):
        self.name = os.path.basename(relpath)
        self.children = []
        for name in sorted(os.listdir(os.path.join(basedir, relpath))):
            cur_relpath = os.path.join(relpath, name)
            cur_path = os.path.join(basedir, cur_relpath)
            if os.path.isdir(cur_path):
                cur_dir = _Directory(basedir, cur_relpath)
                if cur_dir.children:
                    self.children.append(cur_dir)


from user_data import UserData

app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('DEEPZOOM_MULTISERVER_SETTINGS', silent=True)
user_data = UserData()

@app.before_first_request
def _setup():
    app.basedir = None
    app.configured = False
    app.last_tile_name = None
    app.last_file_name = None

@app.route('/')
def index():
    
    path_address = request.args.get("path_address")

    if not path_address:
        return render_template('main_init.html', file_list=user_data.load_user_paths()) #get the paths of the user (setted paths)

    #separate files from paths
    files = []
    paths = []

    for sub in os.listdir(path_address):
        print(sub)
        file_url = path_address+"/"+sub
        
        if os.path.isfile(file_url):
            files.append(file_url)
        else:
            paths.append(file_url)

    return render_template('main_init.html', files=files, paths=paths)

@app.route('/remove_user_path', methods=['POST'])
def remove_user_path():
    data = request.get_json()

    return make_response(user_data.remove_path(data['user_path']))

@app.route('/add_user_path', methods=['POST'])
def add_user_path():
    data = request.get_json()

    return make_response(user_data.save_user_path(data['user_path']))

@app.route('/clear_user_path', methods=['GET'])
def clear_user_paths():
    user_data.clear()
    return make_response("All user paths was deleted.")

@app.route('/download', methods=['GET', 'POST'])
def download():
    file_url = request.args.get('file_url')
    return send_file(file_url, as_attachment=True)


if sys.platform == 'darwin':
    subprocess.Popen(['open', "localhost:80"])
else:
    webbrowser.open_new("localhost:80")

app.run(host="0.0.0.0", port=80, threaded=True)