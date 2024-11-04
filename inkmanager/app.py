from fastapi import FastAPI

from inkmanager.routes import products, users

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)


@app.get('/')
def opa():
    return {'message': 'opa'}
