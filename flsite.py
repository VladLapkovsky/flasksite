from flask import Flask, render_template, url_for, request

app = Flask(__name__)

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
        print(request.form['username'])
        print(request.form['email'])
        print(request.form['message'])
    context = {'menu': MENU, 'title': 'About'}
    return render_template('contact.html', **context)


# with app.test_request_context():
#     print(url_for('about'))
#     print(url_for('profile', username='Vlad'))

if __name__ == '__main__':
    app.run(debug=True)
