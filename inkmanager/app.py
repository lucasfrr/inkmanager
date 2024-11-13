from fastapi import FastAPI

from inkmanager.routes import auth, inks, needles, products, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(inks.router)
app.include_router(needles.router)
app.include_router(products.router)
app.include_router(users.router)


@app.get('/healthcheck')
def healtcheck():
    return {'healthy': 'yes!'}
