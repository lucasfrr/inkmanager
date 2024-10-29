from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def opa():
    return {'message': 'opa'}

