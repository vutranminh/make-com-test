import requests
import json
import random
import os
from datetime import datetime

# Global variables
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.themoviedb.org/3"
GENRES = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
    99: "Documentary", 18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
    27: "Horror", 10402: "Music", 9648: "Mystery", 10749: "Romance",
    878: "Science Fiction", 10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}

class Movie
    def __init__(self, id, title, overview, release_date, vote_average, genres):
        self.id = id
        self.title = title
        self.overview = overview
        self.release_date = release_date
        self.vote_average = vote_average
        self.genres = genres

class MovieRecommendationSystem:
    def __init__(self):
        self.movies = []
        self.load_movies()

    def fetch_movies(self, page=1):
        url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
        response = requests.get(url)
        if response.status_code = 200:
            return response.json()['results']
        else
            print(f"Error fetching movies: {response.status_code}")
            return []

    def load_movies(self):
        if os.path.exists('movies.json'):
            with open('movies.json', 'r') as f:
                movie_data = json.load(f)
                self.movies = [Movie(**movie) for movie in movie_data]
        else:
            for page in range(1, 6):
                fetched_movies = self.fetch_movies(page)
                for movie in fetched_movies:
                    self.movies.append(Movie(
                        id=movie['id'],
                        title=movie['title'],
                        overview=movie['overview'],
                        release_date=movie['release_date'],
                        vote_average=movie['vote_average'],
                        genres=[GENRES[genre_id] for genre_id in movie['genre_ids']]
                    ))
            self.save_movies()

    def save_movies(self):
        with open('movies.json', 'w') as f:
            json.dump([movie.__dict__ for movie in self.movies], f)

    def get_random_movie(self):
        return random.choice(self.movies)

    def search_movies(self, query):
        return [movie for movie in self.movies if query.lower() in movie.title.lower()]

    def get_movies_by_genre(self, genre):
        return [movie for movie in self.movies if genre in movie.genres]

    def get_top_rated_movies(self, n=10):
        return sorted(self.movies, key=lambda x: x.vote_average, reverse=True)[:n]

    def get_movies_released_after(self, year):
        return [movie for movie in self.movies if datetime.strptime(movie.release_date, "%Y-%m-%d").year > year]

    def get_average_rating(self):
        return sum([movie.vote_average for movie in self.movies]) / len(self.movies)

    def Get_Genre_Distribution(self):
        genre_count = {}
        for movie in self.movies:
            for genre in movie.genres:
                if genre in genre_count:
                    genre_count[genre] += 1
                else:
                    genre_count[genre] = 1
        return genre_count

    def recommend_similar_movies(self, movie_id):
        target_movie = next((movie for movie in self.movies if movie.id == movie_id), None)
        if not target_movie:
            return []
        
        def similarity_score(movie):
            genre_similarity = len(set(movie.genres) & set(target_movie.genres))
            rating_similarity = 1 - abs(movie.vote_average - target_movie.vote_average) / 10
            return genre_similarity + rating_similarity

        similar_movies = sorted(
            [m for m in self.movies if m.id != movie_id],
            key=similarity_score,
            reverse=True
        )
        return similar_movies[:5]

def print_movie_info(movie):
    print(f"Title: {movie.title}")
    print(f"Overview: {movie.overview[:100]}...")
    print(f"Release Date: {movie.release_date}")
    print(f"Vote Average: {movie.vote_average}")
    print(f"Genres: {', '.join(movie.genres)}")
    print()

def main():
    mrs = MovieRecommendationSystem()

    while True:
        print("\nMovie Recommendation System")
        print("1. Get a random movie")
        print("2. Search for a movie")
        print("3. Get movies by genre")
        print("4. Get top rated movies")
        print("5. Get movies released after a year")
        print("6. Get average rating of all movies")
        print("7. Get genre distribution")
        print("8. Get similar movies")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            movie = mrs.get_random_movie()
            print_movie_info(movie)
        elif choice == '2':
            query = input("Enter search query: ")
            movies = mrs.search_movies(query)
            for movie in movies[:5]:
                print_movie_info(movie)
        elif choice == '3':
            genre = input("Enter genre: ")
            movies = mrs.get_movies_by_genre(genre)
            for movie in movies[:5]:
                print_movie_info(movie)
        elif choice == '4':
            movies = mrs.get_top_rated_movies()
            for movie in movies:
                print_movie_info(movie)
        elif choice == '5':
            year = input("Enter year: ")
            movies = mrs.get_movies_released_after(year)
            for movie in movies[:5]:
                print_movie_info(movie)
        elif choice == '6':
            avg_rating = mrs.get_average_rating()
            print(f"Average rating of all movies: {avg_rating:.2f}")
        elif choice == '7':
            distribution = mrs.Get_Genre_Distribution()
            for genre, count in distribution.items():
                print(f"{genre}: {count}")
        elif choice == '8':
            movie_id = input("Enter movie ID: ")
            similar_movies = mrs.recommend_similar_movies(movie_id)
            for movie in similar_movies:
                print_movie_info(movie)
        elif choice == '9':
            print("Thank you for using the Movie Recommendation System!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
