import os
from db import create_db, connect_db
from flask import (
    Flask, render_template, url_for, request, session, flash, redirect, abort, g
)

app = Flask(__name__)
app.config.from_object('config.Config')

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
if not os.path.exists(os.path.join(app.root_path, 'flsite.db')):
    create_db(app, os.path.join(app.root_path, 'sq_db.sql'))


MENU = [
    {'name': 'Home', 'url': '/'},
    {'name': 'Install', 'url': '/install-flask'},
    {'name': 'First app', 'url': '/first-app'},
    {'name': 'Contact us', 'url': '/contact'},
    {'name': 'About', 'url': '/about'},
    {'name': 'Login', 'url': '/login'}
]


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


@app.route('/')
def index():
    context = {'menu': MENU, 'title': 'Home'}
    return render_template('index.html', **context)


@app.route('/about')
def about():
    context = {'menu': MENU, 'title': 'About'}
    return render_template('about.html', **context)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session.get('userLogged') != username:
        abort(401)
    context = {'menu': MENU, 'title': 'Profile', 'username': username}
    return render_template('profile.html', **context)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if request.form.get('username') and request.form.get('email') and request.form.get('message'):
            flash('Form sent', category='success')
        else:
            flash('Sending error', category='error')

    context = {'menu': MENU, 'title': 'Contact-us'}
    return render_template('contact.html', **context)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form.get('username') == 'vlad' and request.form.get('password') == '123':  # if user in DB
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    context = {'menu': MENU, 'title': 'Login'}
    return render_template('login.html', **context)


@app.errorhandler(404)
def page_not_found(error):
    context = {'menu': MENU, 'title': 'Page not found'}
    return render_template('page404.html', **context), 404


# with app.test_request_context():
#     print(url_for('about'))
#     print(url_for('profile', username='Vlad'))

if __name__ == '__main__':
    app.run(debug=True)
