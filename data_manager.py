from models import db, User, Movie

class DataManager:
    def create_user(self, name: str) -> None:
        """Add a new user to the database."""
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    def get_users(self) -> list[User]:
        """Return all users."""
        return User.query.all()

    def get_movies(self, user_id: int) -> list[Movie]:
        """Return all movies for a given user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, name: str, director: str, year: int, poster_url: str, user_id: int) -> None:
        """Add a new movie to a user's favorites."""
        movie = Movie(
            name=name,
            director=director,
            year=year,
            poster_url=poster_url,
            user_id=user_id
        )
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id: int, new_title: str) -> None:
        """Update the title of an existing movie."""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()

    def delete_movie(self, movie_id: int) -> None:
        """Delete a movie by ID."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
