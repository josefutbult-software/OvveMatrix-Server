from flask import Flask, request
from flask import render_template
import getpass
import json
import os
import time

last_data = None
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        set_state(request.form)

    return render_template("index.html", 
        state=format_state(get_state()),
        time="{:.1f}".format(get_time_since_pull()))


@app.route("/data", methods=['POST', 'GET'])
def pull_data():
    register_pull()
    return last_data


def format_state(state):
    state['paint']['pattern'] = ''.join(state['paint']['pattern'])
    return state


def get_state():
    with open(os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'persistant', 'state.json'))
    ) as file:
        return json.loads(file.read())


def set_state(form):
    global last_data
    
    state = get_state()

    try:
        mode = form['mode']
        if mode == 'text':
            state['text']['text'] = form['text']
            state['text']['color'] = form['color']
            last_data = {'text': state['text']}

        elif mode == 'waves':
            state['waves']['color1'] = form['color1']
            state['waves']['color2'] = form['color2']
            last_data = {'waves': state['waves']}

        elif mode == 'stars':
            state['stars']['color1'] = form['color1']
            state['stars']['color2'] = form['color2']
            last_data = {'stars': state['stars']}
        
        elif mode == 'paint':
            state['paint']['color'] = form['color']
            pattern = []
            for instance in list(filter(lambda instance: instance != '', form['pattern'].split('#'))):
                pattern.append(f"#{instance}")
            pattern += ["#ffffff"] * (150 - len(pattern))
            state['paint']['pattern'] = pattern 
            last_data = {'paint': state['paint']}

        else:
            return
    except:
        return



    with open(os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'persistant', 'state.json')), 
    "w") as file:
        file.write(json.dumps(state, sort_keys=True, indent=4))


def register_pull():
    with open(os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'persistant', 'last_pull.bin')), 
    "wb") as file:
        file.write(int(time.time() * 1000).to_bytes(64, 'big'))


def get_time_since_pull():
    with open(os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'persistant', 'last_pull.bin')), 
    "rb") as file:
        last_time = float(int.from_bytes(file.read(), 'big')) / 1000
        return time.time() - last_time


if __name__ == "__main__":
    last_data = {'text': get_state()['text']}

    if getpass.getuser() == "josef":
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.run(host='0.0.0.0', port='8000', debug=True)
    else:
        app.run(host='0.0.0.0', port='80')
