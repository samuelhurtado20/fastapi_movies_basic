import json
from db.movies import MOVIES

class MovieService:
    
    def __init__(self):
        data = []
        # Open and read the JSON file
        with open('db/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.movies = data
    
    def get_movies(self):
        return self.movies

    def get_movie_by_id(self, id: int):
        for movie in self.movies:
            if movie["id"] == id:
                return movie
        return None

    def get_movies_by_category(self, category: str):
        return [movie for movie in self.movies if movie['category'] == category]

    def post_new_movie(self, new_movie):
        self.movies.append(json.loads(new_movie.json()))
        self._save_movies()
        return self.movies

    def update_movie(self, id: int, update_movie):
        for index, item in enumerate(self.movies):
            if item["id"] == id:
                self.movies[index].update(update_movie)
                self._save_movies()
                return self.movies[index]
        return None

    def delete_movie(self, id: int):
        for index, item in enumerate(self.movies):
            if item["id"] == id:
                self.movies.pop(index)
                self._save_movies()
        return self.movies
    
    def _save_movies(self):           
        # Serializing json
        json_object = json.dumps(self.movies, indent = 4)
        # Writing to sample.json        
        with open("db/data.json", "w", encoding='utf-8') as outfile:
            outfile.write(json_object)