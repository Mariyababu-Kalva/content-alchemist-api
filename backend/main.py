from fastapi import FastAPI
from backend.routers import summarize

app = FastAPI(title='Content Alchemist API')

app.include_router(summarize.router)

@app.get('/')
def read_root():
    return {'message': 'Welcome to the Content Alchemist API. The Alchemist is brewing!'}
