from flask import Blueprint, request, redirect, url_for, render_template, flash, session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


MENU = [
    {'url': 'index', 'title': 'Back to site'},
    {'url': '.index', 'title': 'Admin Panel'},
    {'url': '.login', 'title': 'Admin Panel login'},
    {'url': '.logout', 'title': 'Admin Panel logout'}
]

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

