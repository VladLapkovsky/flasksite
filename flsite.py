import os
from db import create_db, connect_db
from flask import (
    Flask, render_template, url_for, request, session, flash, redirect, abort, g, make_response
)
from FDataBase import FDataBase

app = Flask(__name__)
app.config.from_object('config.Config')

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
if not os.path.exists(os.path.join(app.root_path, 'flsite.db')):
    create_db(app, os.path.join(app.root_path, 'sq_db.sql'))


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


def current_db():
    db = get_db()
    return FDataBase(db)


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


@app.route('/')
def index():
    context = {'menu': current_db().getMenu(), 'title': 'Home', 'posts': current_db().getPostsAnnounce()}
    content = render_template('index.html', **context)

    response = make_response(content)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Server'] = 'flasksite'
    return response


@app.before_request
def before_my_request():
    print('app.before_request: before_my_request() called')


@app.after_request
def after_my_request(response):
    print('app.after_request: after_my_request() called')
    return response


@app.teardown_request
def teardown__my_request(response):
    print('app.teardown__my_request: teardown__my_request() called')
    return response


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        post_title = request.form.get('post_title')
        post_content = request.form.get('post_content')
        post_url = request.form.get('post_url')
        if post_title and post_content:
            is_post_added = current_db().addPost(post_title, post_content, post_url)
            if is_post_added is True:
                flash('Post added', category='success')
            else:
                flash('Post adding error', category='error')

    context = {'menu': current_db().getMenu(), 'title': 'Add post'}
    return render_template('add_post.html', **context)


@app.route('/post/<string:post_url>')
def show_post(post_url):
    post_title, post_content = current_db().getPost(post_url)
    if not post_title:
        abort(404)

    context = {'menu': current_db().getMenu(), 'title': post_title, 'post_content': post_content}
    return render_template('post.html', **context)


@app.route('/about')
def about():
    context = {'menu': current_db().getMenu(), 'title': 'About'}
    return render_template('about.html', **context)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session.get('userLogged') != username:
        abort(401)
    context = {'menu': current_db().getMenu(), 'title': 'Profile', 'username': username}
    return render_template('profile.html', **context)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if request.form.get('username') and request.form.get('email') and request.form.get('message'):
            flash('Form sent', category='success')
        else:
            flash('Sending error', category='error')

    context = {'menu': current_db().getMenu(), 'title': 'Contact-us'}
    return render_template('contact.html', **context)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form.get('username') == 'vlad' and request.form.get('password') == '123':  # if user in DB
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    context = {'menu': current_db().getMenu(), 'title': 'Login'}
    return render_template('login.html', **context)


@app.errorhandler(404)
def page_not_found(error):
    context = {'menu': current_db().getMenu(), 'title': 'Page not found'}
    return render_template('page404.html', **context), 404


# with app.test_request_context():
#     print(url_for('about'))
#     print(url_for('profile', username='Vlad'))

if __name__ == '__main__':
    app.run(debug=True)
