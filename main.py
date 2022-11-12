import json
from deta import Deta
import secrets
import bcrypt
import fastapi
from fastapi import HTTPException, Form
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

app = fastapi.FastAPI(docs_url="/api/documentation", redoc_url=None)
templates = Environment(loader=FileSystemLoader('templates'))


deta = Deta("b0j1zima_gUAdFysbwx7adfr7bQ7xRQkvajyp8vxu")

users_db = deta.Base("users")
pantries_db = deta.Base("pantries")

# register static folder
app.mount("/statics", StaticFiles(directory="statics"), name="statics")


@app.api_route("/", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def root(response: fastapi.Response, request: fastapi.Request):
    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('index.html').render()

    else:
        try:
            j = users_db.fetch({"key": k})

        except Exception as e:
            print(e)
            raise HTTPException(status_code=422, detail="Something went wrong")

        return templates.get_template('inventory.html').render()

@app.api_route("/login", methods=["GET", "POST"], response_class=fastapi.responses.HTMLResponse)
def root():
    return templates.get_template('login.html').render()
    #return templates.get_template('index.html').render()

@app.api_route("/register", methods=["POST"], response_class=fastapi.responses.HTMLResponse)
def root():
    return "REGISTER"
    #return templates.get_template('index.html').render()
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)