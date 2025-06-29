from flask import Flask, render_template, request, redirect, url_for
import os
from models import db, User
from data_manager import DataManager
from typing import Optional

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'movies.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
data_manager = DataManager()

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Render the user overview page."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Handle creation of a new user."""
    name: Optional[str] = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id: int):
    """Delete a user and all their movies."""
    user = User.query.get(user_id)
    if user:
        for movie in user.movies:
            db.session.delete(movie)
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def list_movies(user_id: int):
    """List or add movies for a given user."""
    if request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        poster_url = request.form.get('poster_url')

        if name:
            try:
                year_int = int(year)
            except (TypeError, ValueError):
                year_int = None
            data_manager.add_movie(name, director, year_int, poster_url, user_id)

        return redirect(url_for('list_movies', user_id=user_id))

    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id: int, movie_id: int):
    """Delete a specific movie for a user."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(user_id: int, movie_id: int):
    """Edit a movie entry."""
    movie = data_manager.get_movie(movie_id)

    if request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')

        try:
            year_int = int(year)
        except (TypeError, ValueError):
            year_int = None

        data_manager.update_movie(movie_id, name, director, year_int)
        return redirect(url_for('list_movies', user_id=user_id))

    return render_template('edit_movie.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id: int):
    """Edit the name of a user."""
    user = data_manager.get_user(user_id)

    if request.method == 'POST':
        new_name = request.form.get('name')
        if new_name:
            data_manager.update_user(user_id, new_name)
            return redirect(url_for('index'))

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/add_from_api', methods=['GET', 'POST'])
def add_movie_from_api(user_id: int):
    """Add a movie via OMDb API by title."""
    error: Optional[str] = None

    if request.method == 'POST':
        title = request.form.get('title')
        data = data_manager.fetch_movie_data(title)

        if data:
            data_manager.add_movie(
                name=data['name'],
                director=data['director'],
                year=data['year'],
                poster_url=data['poster_url'],
                user_id=user_id
            )
            return redirect(url_for('list_movies', user_id=user_id))
        error = f"❌ Movie '{title}' could not be found or there was a problem with the API."

    return render_template('add_from_api.html', user_id=user_id, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
