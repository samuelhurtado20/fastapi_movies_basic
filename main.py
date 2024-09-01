from typing import List
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from JWTBearer import JWTBearer
from jwt_manager import create_token
from models.movie import Movie
from models.user import User
from services.movies import MovieService

app = FastAPI()
# Para cambiar el nombre de la aplicacion
app.title = "Mi aplicacion con FastAPI"

# Para cambiar la version de la aplicacion
app.version = "0.0.1"

mv = MovieService()

# los tags nos permite agrupar las rutas de la aplicacion


@app.get("/", tags=['home'])
def read_root():
    return {"Hello": "World"}


@app.get('/home', tags=['home'])
def home():
    return HTMLResponse('<h1 style=color:red> hola mundo </h2>')

@app.post("/login", tags=["auth"])
def login(user: User):
    if (user.email == "admin@gmail.com" and user.password == "123456"):
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content={"message": "Credenciales inválidas, intente de nuevo"})

@app.get("/movies", tags=["Movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    movies = mv.get_movies()
    return JSONResponse(content=movies, status_code=200)


@app.get(path="/movies/{id}", tags=["Movies"], response_model=Movie)
def get_movies(id: int = Path(ge=1, le=2000)) -> Movie:
    movie = mv.get_movie_by_id(id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(content=movie, status_code=200)


@app.get('/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    movies = mv.get_movies_by_category(category)
    if not movies:
        raise HTTPException(status_code=404, detail="Movies not found")
    return JSONResponse(content=movies, status_code=200)


@app.post('/movies/', response_model=list[Movie], tags=['Movies'])
def post_new_movie(new_movie: Movie) -> list[Movie]:
    movies = mv.post_new_movie(new_movie)
    return JSONResponse(content=movies, status_code=201)


@app.put('/movies/{id}', tags=['Movies'], response_model=Movie)
async def update_movie(id: int, movie: Movie) -> Movie:
    movie = mv.update_movie(id, movie)
    return JSONResponse(content=movie, status_code=200)


@app.delete('/movies/{id}', tags=['Movies'], response_model=list[Movie])
async def delete_movie(id: int) -> list[Movie]:
    movies = mv.delete_movie(id)
    return JSONResponse(content=movies, status_code=201)
