import requests
from typing import Optional
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

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return User.query.get(user_id)

    def update_user(self, user_id: int, new_name: str) -> None:
        """Update a user's name."""
        user = User.query.get(user_id)
        if user:
            user.name = new_name
            db.session.commit()

    def get_movies(self, user_id: int) -> list[Movie]:
        """Return all movies for a given user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        """Return a movie by its ID."""
        return Movie.query.get(movie_id)

    def add_movie(
        self,
        name: str,
        director: Optional[str],
        year: Optional[int],
        poster_url: Optional[str],
        user_id: int
    ) -> None:
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

    def update_movie(self, movie_id: int, name: str, director: str, year: Optional[int]) -> None:
        """Update a movie's information."""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = name
            movie.director = director
            movie.year = year
            db.session.commit()

    def delete_movie(self, movie_id: int) -> None:
        """Delete a movie by ID."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()

    def fetch_movie_data(self, title: str) -> Optional[dict]:
        """Fetch movie details from OMDb API by title."""
        api_key = "f821c8bd"
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("Response") == "True":
                year_raw = data.get("Year")
                return {
                    "name": data.get("Title"),
                    "director": data.get("Director"),
                    "year": int(year_raw) if year_raw and year_raw.isdigit() else None,
                    "poster_url": data.get("Poster")
                }
        except (requests.RequestException, ValueError):
            pass
        return None
