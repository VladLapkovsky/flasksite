from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Users, Profiles

app = Flask(__name__)
app.config.from_object('config.Config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:passwords@localhost/mydatabase'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:passwords@localhost/mydatabase'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://user:passwords@127.0.0.1:1521/mydatabase'

db.init_app(app)
db.create_all(app=app)


@app.route('/')
def index():
    users = []
    try:
        users = Users.query.all()
    except Exception as e:
        flash(f'DB reading error: {e}', 'error')

    context = {'title': 'Home', 'users': users}
    return render_template('index.html', **context)


@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        # validate...
        hashed_password = generate_password_hash(request.form['password2'])

        try:
            user = Users(email=request.form['email'], password=hashed_password)
            db.session.add(user)
            db.session.flush()

            profile = Profiles(
                name=request.form['name'],
                age=request.form['age'],
                city=request.form['city'],
                user_id=user.id
            )
            db.session.add(profile)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash(f'DB adding error: {e}', 'error')

    return render_template('register.html', title='Register')


if __name__ == '__main__':
    app.run(debug=True)
