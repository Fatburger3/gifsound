#!pyenv/bin/python

# AUTHORS: Erick Shaffer, Carsen Yates
# DATE: 11/14/2017
# PURPOSE: This file controls all the flask routes for gifsound


from flask import Flask, render_template, redirect, url_for, json
import os
from Controller.link_controller import *
from Controller.user_controller import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/featured')
def featured():
    return render_template('featured.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@app.route('/login/<username>/<password>', methods=['GET', 'POST'])
def login(username, password):
    data = {}
    code = 0
    user = get_user_by_username(username)
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        data['login'] = True
        data['name'] = username
        code = 200
    else:
        data['login'] = False
        code = 401

    return app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    data = {}
    logout_user()
    data['logged_out'] = True
    code = 200
    return app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )


@app.route('/register/<user_name>/<email>/<password>',
           methods=['POST', 'PUT'])
def register(user_name, email, password):
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = get_user_by_username(user_name)
    data = {}
    code = 0
    if user is not None:
        data = {"signup": "Username is taken"}
        code = 400
        data["username"] = "None"
    else:
        code = 200
        user = create_user(app, user_name, email, pw_hash, 1)
        return user
    return app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )


@app.route('/api/create/link/<name>/<path:full_link>/<path:gif_link>/<yt_id>',
           methods=['POST', 'PUT'])
def create_gif_sound(name, full_link, gif_link, yt_id):
    data = {"status": "Success"}
    code = 200
    if current_user.is_authenticated:
        create_link(name, current_user.user_id, full_link, gif_link, yt_id)
    else:
        create_link(name, None, full_link, gif_link, yt_id)
    return app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )


@app.route('/api/user_info', methods=['POST', 'GET'])
@login_required
def get_user_info(user_id, api_key):
    user = get_user(user_id)
    schema = UserSchema(many=True)
    result = schema.dumps(user)
    return result.data


# @app.route('/api/user_info', methods=['POST', 'GET'])
# def get_all_users_info(api_key):
#     return get_all_users()


@app.route('/api/links', methods=['POST'])
def get_links():
    links = get_all_links()
    schema = LinkSchema(many=True)
    result = schema.dumps(links)
    return result


@app.route('/smoke_test/<int:test>', methods=['POST', 'GET'])
def smoke_test(test):
    return 'hi'


# This route is for debugging, will be removed in productions
@app.route('/api/create_tables/<api_key>', methods=['POST', 'PUT'])
def create_tables(api_key):
    create_user_table()
    create_link_table()
    data = {'status': 'success'}
    code = 200
    return app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )


@app.route('/testview/')
def test_view_combo():
    return redirect(
        url_for('view_combo', gif_url='https://media4.giphy.com/avatars/100soft/WahNEDdlGjRZ.gif', yt_id='Hug0rfFC_L8'))


@app.route('/view/<path:gif_url>/<yt_id>/')
def view_combo(gif_url, yt_id):
    showinfo = 1  # Enable Title and video controls
    rel = 0  # Uhh I don't know
    start = 0  # starting point of video
    return render_template('view.html', gif=gif_url,
                           video=f'https://www.youtube.com/embed/{yt_id}?rel={rel}&amp;showinfo={showinfo}&amp;start={start}')


if __name__ == '__main__':
    app.run(debug=settings['development']['other']['debug'])
