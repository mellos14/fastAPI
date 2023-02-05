from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
app.title = "Mi app con FastAPI"
app.version = "0.0.1"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Las credenciales son invalidas")


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float
    category: str

    class Config:
        schema_extra = {
            "example": {
                'id': 1,
                'title': "Pelicula",
                'overview': "Descripción de la película",
                            'year': 2022,
                            'rating': 9.4,
                            'category': "Ninguna"

            }
        }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'},
    {
        'id': 2,
        'title': 'Avatar2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'}


]


@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1> Hello World </h1>')


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)


@app.get('/movies', tags=['movies'], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movie():
    return JSONResponse(status_code=200, content=movies)


@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    data = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=data)


@app.post('/movies/', tags=['movies'], status_code=201)
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(status_code=201, content={'message': "Se ha registrado la pelicula"})


@app.put('/movies/{id}', tags=['movies'], status_code=200)
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(status_code=200, content={'message': "Se ha modificado la pelicula"})


@app.delete('/movies/{id}', tags=['movies'], status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={'message': "Se ha eliminado la pelicula"})
