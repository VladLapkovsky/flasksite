import sqlite3

from flask import Blueprint, request, redirect, url_for, render_template, flash, session, current_app, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


BLUEPRINT_DB = None
MENU = [
    {'url': 'index', 'title': 'Back to site'},
    {'url': '.index', 'title': 'Admin Panel'},
    {'url': '.login', 'title': 'Admin Panel login'},
    {'url': '.logout', 'title': 'Admin Panel logout'},
    {'url': '.list_pub', 'title': 'Publication List'}
]


@admin.before_request
def connect_blueprint_db():
    global BLUEPRINT_DB
    BLUEPRINT_DB = g.get('link_db')


@admin.teardown_request
def disconnect_blueprint_db(request):
    global BLUEPRINT_DB
    BLUEPRINT_DB = None
    return request


@admin.route('/')
def index():
    if not is_logged():
        return redirect(url_for('.login'))

    context = {'title': 'Admin Panel', 'menu': MENU}
    return render_template('admin/index.html', **context)


def login_admin():
    # Can't create Flask_Login instance one more time
    # Better to keep blueprints isolated
    session['admin_logged'] = 1


def is_logged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET' and is_logged():
        return redirect(url_for('.index'))

    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['password'] == '12345':
            login_admin()

            # dot meaning current blueprint, otherwise -> global index
            # it's better to use dot if the blueprint name can change
            return redirect(url_for('.index'))
            # return redirect(url_for('admin.index'))  # admin -> blueprint name
        else:
            flash('Login error: wrong login or password', 'error')

    context = {'title': 'Admin Panel login'}
    return render_template('admin/login.html', **context)


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if is_logged():
        logout_admin()

    return redirect(url_for('.login'))


@admin.route('/list-pub')
def list_pub():
    if not is_logged():
        return redirect(url_for('.login'))

    list_of_pub = []
    sql_query = 'SELECT title, text, url FROM posts'

    if BLUEPRINT_DB is not None:
        try:
            cursor = BLUEPRINT_DB.cursor()
            cursor.execute(sql_query)
            list_of_pub = cursor.fetchall()
        except sqlite3.Error as e:
            flash(f'Error occurs while getting post list from db: {e}', 'error')

    context = {'title': 'Publication List', 'menu': MENU, 'list_of_pub': list_of_pub}
    return render_template('admin/listpub.html', **context)
