from flask import Flask, render_template, url_for, request, flash
from credentials import PROJECT_SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = PROJECT_SECRET_KEY


MENU = [
    {'name': 'Install', 'url': 'install-flask'},
    {'name': 'First app', 'url': 'first-app'},
    {'name': 'Contact us', 'url': 'contact'}
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
    return f"User: {username}"


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if request.form.get('username') and request.form.get('email') and request.form.get('message'):
            flash('Form sent', category='success')
        else:
            flash('Sending error', category='error')

    context = {'menu': MENU, 'title': 'About'}
    return render_template('contact.html', **context)


# with app.test_request_context():
#     print(url_for('about'))
#     print(url_for('profile', username='Vlad'))

if __name__ == '__main__':
    app.run(debug=True)
