from fastapi import FastAPI

from inkmanager.routes import products

app = FastAPI()

app.include_router(products.router)


@app.get('/')
def opa():
    return {'message': 'opa'}
