from flask import Flask, render_template, request, redirect, url_for
import os
from models import db, User
from data_manager import DataManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('index'))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        # Erst alle Movies löschen (sonst ForeignKey-Fehler)
        for movie in user.movies:
            db.session.delete(movie)
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies')
def list_movies(user_id):
    return f"Here should be the movies for user {user_id}"


if __name__ == '__main__':
    app.run(debug=True)
