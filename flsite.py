from flask import (
    Flask,
    render_template,
    url_for,
    request,
    session,
    flash,
    redirect,
    abort
)
from credentials import PROJECT_SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = PROJECT_SECRET_KEY


MENU = [
    {'name': 'Install', 'url': 'install-flask'},
    {'name': 'First app', 'url': 'first-app'},
    {'name': 'Contact us', 'url': 'contact'},
    {'name': 'About', 'url': 'about'},
    {'name': 'Login', 'url': 'login'}
]


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
