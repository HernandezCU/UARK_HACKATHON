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
def root(request: fastapi.Request):
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


@app.api_route("/user/login", methods=["POST"], response_class=fastapi.responses.HTMLResponse)
def login(response: fastapi.Response, request: fastapi.Request, email: str = Form(...), password: str = Form(...)):
    
    j = users_db.fetch({"email": str(email.lower())})

    if j.count == 1:
        x = bcrypt.checkpw(password.encode(), j.items[0]['password'].encode())
        user = j.items[0]
        
        if x == True:
            response = fastapi.responses.RedirectResponse(url="/", status_code=200)
            response.set_cookie(key="key", value=user['key'])
            return response

        else:
            response = fastapi.responses.RedirectResponse(url="/login", status_code=200)
            return response

    else:
        response = fastapi.responses.RedirectResponse(url="/login", status_code=200)
        return response


@app.api_route("/login", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def render_login(request: fastapi.Request):
    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('login.html').render()

    else:
        return fastapi.responses.RedirectResponse(url="/", status_code=200)
    

@app.api_route("/user/register", methods=["POST"], response_class=fastapi.responses.HTMLResponse)
def register():
    return "REGISTER"


@app.api_route("/register", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def render_register(request: fastapi.Request):
    
    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('register.html').render()

    else:
        return fastapi.responses.RedirectResponse(url="/", status_code=200)
    #return templates.get_template('index.html').render()
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)