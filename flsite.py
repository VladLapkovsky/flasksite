from flask import Flask, render_template

app = Flask(__name__)

MENU = ['Install', 'First app', 'Contact us']


@app.route('/')
def index():
    context = {'menu': MENU, 'title': 'Home'}
    return render_template('index.html', **context)


@app.route('/about')
def about():
    context = {'menu': MENU, 'title': 'About'}
    return render_template('about.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
