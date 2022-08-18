import os
from flask import (
    Flask, render_template, url_for, request, session, flash, redirect, abort, g, make_response
)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from db import create_db, connect_db
from config import APP_DATABASE
from FDataBase import FDataBase
from UserLogin import UserLogin


app = Flask(__name__)
app.config.from_object('config.Config')

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
if not os.path.exists(os.path.join(app.root_path, 'flsite.db')):
    create_db(app, os.path.join(app.root_path, 'sq_db.sql'))

LOGIN_MANAGER = LoginManager(app)
LOGIN_MANAGER.login_view = 'login'
LOGIN_MANAGER.login_message_category = 'error'


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, APP_DATABASE)


def get_db():
    # open DB connection
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db(app)
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    # close DB connection
    if hasattr(g, 'link_db'):
        g.link_db.close()


# @app.route('/')
# def index():
#     context = {'menu': current_db().getMenu(), 'title': 'Home', 'posts': current_db().getPostsAnnounce()}
#     content = render_template('index.html', **context)
#     response = make_response(content)
    # response.headers['Content-Type'] = 'text/plain'
    # response.headers['Server'] = 'flasksite'

    # response = make_response(content, 500)  # 500 is response code

    # img = None
    # with app.open_resource(''.join((app.root_path, '/static/images/default.png')), mode='rb') as f:
    #     img = f.read()
    # if img is None:
    #     return  'No image'
    # response = make_response(img)
    # response.headers['Content-Type'] = 'image.png'
    # return response
    # return "<h1>Home</h1>", 200, {'Content-Type': 'text/plain'}


# @app.route('/')
# def index():
#     return redirect(url_for('about'), code=302 )


# @app.route('/')
# def index():
#     is_logged = request.cookies.get('logged')
#     context = {'menu': current_db().getMenu(), 'title': 'Home', 'posts': current_db().getPostsAnnounce(), 'logged': is_logged}
#     content = render_template('index.html', **context)
#
#     response = make_response(content)
#     response.headers['Content-Type'] = 'text/html'
#     response.headers['Server'] = 'flasksite'
#     return response


@app.route('/')
def index():
    # session.permanent = True
    # if 'visits' in session:
    #     session['visits'][0] += 1
    #     session.modified = True
    # else:
    #     session['visits'] = [1]
    # context = {'menu': APP_DATABASE.getMenu(), 'title': 'Home', 'posts': APP_DATABASE.getPostsAnnounce(), 'visits': session['visits']}
    context = {'menu': APP_DATABASE.getMenu(), 'title': 'Home', 'posts': APP_DATABASE.getPostsAnnounce()}
    content = render_template('index.html', **context)

    response = make_response(content)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Server'] = 'flasksite'
    return response


@app.before_request
def set_app_database():
    global APP_DATABASE
    db = get_db()
    APP_DATABASE = FDataBase(db)


# @app.after_request
# def after_my_request(response):
#     print('app.after_request: after_my_request() called')
#     return response
#
#
# @app.teardown_request
# def teardown__my_request(response):
#     print('app.teardown__my_request: teardown__my_request() called')
#     return response


@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        post_title = request.form.get('post_title')
        post_content = request.form.get('post_content')
        post_url = request.form.get('post_url')
        if post_title and post_content:
            is_post_added, msg = APP_DATABASE.addPost(post_title, post_content, post_url)
            if is_post_added is True:
                flash(f'Post added {msg}', category='success')
            else:
                flash(f'Post adding error: {msg}', category='error')

    context = {'menu': APP_DATABASE.getMenu(), 'title': 'Add post'}
    return render_template('add_post.html', **context)


@app.route('/post/<string:post_url>')
@login_required
def show_post(post_url):
    post_title, post_content = APP_DATABASE.getPost(post_url)
    if not post_title:
        abort(404)

    context = {'menu': APP_DATABASE.getMenu(), 'title': post_title, 'post_content': post_content}
    return render_template('post.html', **context)


@app.route('/about')
def about():
    context = {'menu': APP_DATABASE.getMenu(), 'title': 'About'}
    return render_template('about.html', **context)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if request.form.get('username') and request.form.get('email') and request.form.get('message'):
            flash('Form sent', category='success')
        else:
            flash('Sending error', category='error')

    context = {'menu': APP_DATABASE.getMenu(), 'title': 'Contact-us'}
    return render_template('contact.html', **context)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if username and email:
            msg = ''
            if password1 != password2:
                msg = "Passwords don't match"
            else:
                hashed_password = generate_password_hash(password1)
                user_added, msg = APP_DATABASE.addUser(username, email, hashed_password)
                if user_added is True:
                    flash('Registration succeed', 'success')
                    return redirect(url_for('login'))
            flash(f'Registration error: {msg}', 'error')

        else:
            flash('Wrong filled fields', 'error')
    context = {'menu': APP_DATABASE.getMenu(), 'title': 'Register'}
    return render_template('register.html', **context)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('profile'))
    # if session.get(COOKIE_LOGGED) and request.cookies.get('logged'):
    #     return redirect(url_for('profile', username=session[COOKIE_LOGGED]))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = APP_DATABASE.getUserByEmail(email)

        if user is not None and check_password_hash(user['password'], password):
            remainme = True if request.form.get('remainme') else False

            user_login = UserLogin().login_user(user)
            login_user(user_login, remember=remainme)

            flash('Login succeed', 'success')
            # session[COOKIE_LOGGED] = username
            response = make_response(redirect(url_for('profile')))
            # response.set_cookie('logged', 'yes', 60)  # 60 sec
            return response
        else:
            flash(f'Login error: wrong login or password', 'error')



    context = {'menu': APP_DATABASE.getMenu(), 'title': 'Login'}
    return render_template('login.html', **context)


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out', 'success')
    response = make_response(redirect(url_for('login')))
    # response.delete_cookie('logged')
    return response


# @app.route('/profile/<username>')
# def profile(username):
#     if COOKIE_LOGGED not in session or session.get(COOKIE_LOGGED) != username:
#         abort(401)
#     context = {'menu': APP_DATABASE.getMenu(), 'title': 'Profile', 'username': username}
#     return render_template('profile.html', **context)


@app.route('/profile')
@login_required
def profile():
    context = {'menu': APP_DATABASE.getMenu(), 'title': 'Profile', 'current_user': current_user}

    return render_template('profile.html', **context)
#     return f"""
#     <p><a href="{url_for('logout')}">Logout</a>
#     <p> user info: {current_user.get_ud()}
# """


@app.errorhandler(404)
def page_not_found(error):
    context = {'menu': APP_DATABASE.getMenu(), 'title': 'Page not found'}
    return render_template('page404.html', **context), 404


# with app.test_request_context():
#     print(url_for('about'))
#     print(url_for('profile', username='Vlad'))

if __name__ == '__main__':
    app.run(debug=True)
