from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "Mi app con FastAPI"
app.version = "0.0.1"


class Movie(BaseModel):
          id: Optional[int]=None
          title : str = Field(min_length=5,max_length=15)
          overview :str = Field(min_length=15,max_length=50)
          year :int = Field(le=2022)
          rating : float
          category : str

          class Config:
                    schema_extra = {
                              "example":{
                                        'id': 1,
                                        'title':"Pelicula",
                                        'overview':"Descripción de la película",
                                        'year':2022,
                                        'rating':9.4,
                                        'category':"Ninguna"

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


@app.get('/', tags= ['Home'])
def message():
          return HTMLResponse('<h1> Hello World </h1>')

@app.get('/movies',tags=['movies'])
def get_movie():
          return JSONResponse(content= movies)

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge= 1, le= 2000)):
          for item in movies:
                    if item["id"]== id:
                           return JSONResponse(content= item)  
          return JSONResponse(content= [])

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query (min_length=5,max_length=15)):
          data = [movie for movie in movies if movie['category']==category]
          return JSONResponse(content= data) 
@app.post('/movies/', tags=['movies'])
def create_movie(movie:Movie):
          movies.append(movie)
          return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id:int,movie:Movie):
          for item in movies:
                    if item["id"]== id:
                           item["title"] = movie.title
                           item["overview"] = movie.overview
                           item["year"] = movie.year
                           item["rating"] = movie.rating
                           item["category"] = movie.category
                           return movies

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
          for item in movies:
                    if item["id"]== id:
                              movies.remove(item)
                              return movies

