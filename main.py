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


@app.api_route("/users/login", methods=["POST"], response_class=fastapi.responses.HTMLResponse)
def login(response: fastapi.Response, request: fastapi.Request, email: str = Form(...), password: str = Form(...)):
    
    j = users_db.fetch({"email": str(email.lower())})

    if j.count == 1:
        x = bcrypt.checkpw(password.encode(), j.items[0]['password'].encode())
        user = j.items[0]
        
        if x == True:
            response = templates.get_template("redirect.html").render()
            response.set_cookie(key="key", value=user['key'])
            return response

        else:
            response = templates.TemplateResponse("redirect.html", {"request": request, "url": "/login"})
            return response

    else:
        response = templates.TemplateResponse("redirect.html", {"request": request, "url": "/login"})
        return response


@app.api_route("/login", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def render_login(request: fastapi.Request):
    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('login.html').render()

    else:
        return templates.get_template('redirect.html').render({"url": "/"})
    

@app.api_route("/users/register", methods=["POST"], response_class=fastapi.responses.HTMLResponse)
def register(response: fastapi.Response, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    j = users_db.fetch({"email": email.lower()})

    if j.count != 0:
        return templates.get_template('redirect.html').render({"url": "/register"})

    else:
        try:
            p = password.encode()
            hashed_p = bcrypt.hashpw(p,"$2b$12$vj2GaHW10eRxDcJTTTAWI.".encode())
            key = secrets.token_urlsafe(12)

            u = {"key": key, "name": name, "email": email.lower(), "password": hashed_p.decode()}
            users_db.put(u)

            response.set_cookie(key="key", value=u['key'])
            response = templates.get_template("redirect.html").render({"url": "/"})
            return response

        except Exception as e:
            return templates.get_template('redirect.html').render({"url": "/register"})


@app.api_route("/register", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def render_register(request: fastapi.Request):
    
    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('register.html').render()

    else:
        return templates.get_template("redirect.html", {"request": request, "url": "/"})
    #return templates.get_template('index.html').render()
    

@app.get("/users/logout", response_class=fastapi.responses.HTMLResponse)
async def logout(response: fastapi.Response, request: fastapi.Request):

    response = templates.get_template("redirect.html").render({"url": "/"})
    response.delete_cookie("key", path="/")
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)