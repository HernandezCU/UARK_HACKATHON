import json
import random
from deta import Deta
import secrets
import bcrypt
import fastapi
import datetime
from fastapi import HTTPException, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
import requests

app = fastapi.FastAPI(docs_url="/api/documentation", redoc_url=None)
templates = Environment(loader=FileSystemLoader('templates'))


deta = Deta("b0j1zima_gUAdFysbwx7adfr7bQ7xRQkvajyp8vxu")

users_db = deta.Base("users")
pantries_db = deta.Base("pantries")
food_photos = deta.Drive("food_photos")
recipes_db = deta.Base("recipes")



app.mount("/statics", StaticFiles(directory="statics"), name="statics")


def create_item(id, nm, qt, pic, upc):
    r = random.randint(91,547)
    date = datetime.datetime.now()
    exp_d = date + datetime.timedelta(days=r)
    return {id: {
            "item_id": id,
            "name": nm,
            "quantity": qt,
            "image": pic,
            "upc": upc,
            "date_added": str(date.year) + "/" + str(date.month) + "/" + str(date.day),
            "expiration_date": str(exp_d.year) + "/" + str(exp_d.month) + "/" + str(exp_d.day)
            }}


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
        try:
            x = pantries_db.fetch({"key": k}).items[0]
            z = x['items']
            l = []
            for i in z:
                l.append(z[i])


            return templates.get_template('inventory.html').render({"items": l})
        except Exception as e:
            print(e)
            return templates.get_template('inventory.html').render({"items": []})


@app.api_route("/users/login", methods=["POST"], response_class=fastapi.responses.HTMLResponse)
def login(response: fastapi.Response, request: fastapi.Request, email: str = Form(...), password: str = Form(...)):

    j = users_db.fetch({"email": str(email.lower())})

    if j.count == 1:
        x = bcrypt.checkpw(password.encode(), j.items[0]['password'].encode())
        user = j.items[0]

        if x == True:
            response.set_cookie(key="key", value=user['key'])
            return templates.get_template("redirect.html").render({"url": "/"})

        else:
            response = templates.get_template("redirect.html").render({"url": "/login"})
            return response

    else:
        response = templates.get_template("redirect.html").render({"url": "/login"})
        return response


@app.api_route("/login", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def render_login(request: fastapi.Request):
    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('login.html').render()

    else:
        return templates.get_template('redirect.html').render({"url": "/"})


@app.api_route("/users/recipes", methods=["POST"], response_class=fastapi.responses.HTMLResponse)
async def recipes(request: fastapi.Request, response: fastapi.Response, item: str = Form(...)):
    k = request.cookies.get("key")
    if k is None:
        return templates.get_template('redirect.html').render({"url": "/login"})
    else:
        try:
            j = users_db.fetch({"key": k})

        except Exception as e:
            print(e)
            raise HTTPException(status_code=422, detail="Something went wrong")
        try:
            x = pantries_db.fetch({"key": k}).items[0]
            z = x['items']
            l = []
            for i in z:
                l.append(z[i])


            return templates.get_template('recipes.html').render({"items": l})
        except Exception as e:
            print(e)
            return templates.get_template('recipes.html').render({"items": []})


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
            pantries_db.put({"key": key, "items": {}})

            response.set_cookie(key="key", value=u['key'])
            return templates.get_template("redirect.html").render({"url": "/"})

        except Exception as e:
            return templates.get_template('redirect.html').render({"url": "/register"})


@app.api_route("/register", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def render_register(request: fastapi.Request):

    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('register.html').render()

    else:
        return templates.get_template("redirect.html", {"request": request, "url": "/"})

@app.api_route("/users/upload", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def render_upload(request: fastapi.Request):
    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('redirect.html').render({"url": "/login"})

    else:
        return templates.get_template('upload.html').render()


@app.api_route("/users/logout", response_class=fastapi.responses.HTMLResponse)
async def logout(response: fastapi.Response, request: fastapi.Request):

    response.delete_cookie("key", path="/")
    return templates.get_template("redirect.html").render({"url": "/"})


@app.api_route("/recipe", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
async def recipe(request: fastapi.Request):
    k = request.cookies.get("key")

    if k is None:
        return templates.get_template('redirect.html').render({"url": "/login"})

    else:
        return templates.get_template('recipe.html').render()



#FE USE ONLY
@app.api_route("/api/pantry/get", response_class=fastapi.responses.JSONResponse)
async def pantry(request: fastapi.Request):
    k = request.cookies.get("key")

    pantry = pantries_db.get(k)

    if pantry is not None:
        return json.dumps(pantry['items'])
    else:
        return json.dumps([])


@app.api_route("/api/pantry/add", response_class=fastapi.responses.JSONResponse)
async def add_pantry(request: fastapi.Request, item_id: str, name: str, quantity: int, image: str, upc: str):
    #add current date, and expiration date
    #item_ID, name, quantity, image, upc, name, quantity, image, upc
    k = request.cookies.get("key")
    if k is None:
        return {"error": "NOT_ALLOWED","code": 455}
    else:
        p = pantries_db.fetch({"key":k}).items[0]["items"]
        if p is not None:
            p.update(create_item(item_id, name, quantity, image, upc))
            pantries_db.put({"key": k, "items": p})
            return {"error": "NONE","code": 200}


@app.api_route("/api/pantry/item/{action}", response_class=fastapi.responses.JSONResponse)
async def update_count(request: fastapi.Request, action: str, id: str, num: int):

    p = pantries_db.fetch({"key": request.cookies.get("key")}).items[0]
    for i in p['items']:
        if str(p['items'][i]['item_id']) == str(id):
            print(p['items'][i]['quantity'])
            if action.lower() == "add":
                p['items'][i]['quantity'] += num
                pantries_db.put({"key": request.cookies.get("key"), "items": p['items']})
                return {"error": "NONE","code": 200}
            else:
                p['items'][i]['quantity'] -= num
                pantries_db.put({"key": request.cookies.get("key"), "items": p['items']})
                return {"error": "NONE","code": 200}

    return {"error": "ITEM_NOT_FOUND","code": 200}


@app.api_route("/api/upload", methods=["POST"], response_class=fastapi.responses.HTMLResponse)
async def upload_img(request: fastapi.Request, file: UploadFile = File(...)):
    k = request.cookies.get("key")
    if k is None:
        return {"error": "NOT_ALLOWED","code": 455}
    else:
        name = str(k) + ".png"
        f = file.file
        res = food_photos.put(name, f)
        print(res)
        return templates.get_template("redirect.html").render({"url": "/"})


@app.api_route("/api/cdn/{key}", response_class=fastapi.responses.JSONResponse)
async def get_cdn(request: fastapi.Request, key: str):
    res = food_photos.get(key + ".png")
    return fastapi.responses.StreamingResponse(res.iter_chunks(1024), media_type="image/png")


@app.api_route("/api/key", response_class=fastapi.responses.JSONResponse)
async def keys(request: fastapi.Request):

    ks = ["8d74294d6dfa492f845941e26d98c8e3", "d618860128c54d248fb9784f0e16cfce", "4bd03fd88e404d25993d236476d2cd7e"]
    k = request.cookies.get("key")

    if k is None:
        return {"error": "NOT_ALLOWED","code": 405 ,"key": "NOT_ALLOWED"}
    else:
        return {"error": "NONE","code": 200 ,"key": random.choice(ks)}


@app.api_route("/api/barcode/process", response_class=fastapi.responses.JSONResponse)
async def process_barcode(barcode: str, key: str):
    session = requests.Session()
    if key == "NOT_ALLOWED":
        return {"success": False}
    else:
        ks = ["8d74294d6dfa492f845941e26d98c8e3", "d618860128c54d248fb9784f0e16cfce", "4bd03fd88e404d25993d236476d2cd7e"]

        random_key = random.choice(ks)

        res = session.get(f'https://api.spoonacular.com/food/products/upc/{barcode}?apiKey={random_key}')
        res = res.json()


        if 'status' in res and res['status'] == "failure":
            return {"success": False}
        else:
            items = pantries_db.fetch().items
            for i in items:
                if i["key"] == key:
                    print(res)
                    i["items"].update(create_item(res["id"], res["title"], 1, res["image"], barcode))
                    pantries_db.put(i)
                    return {"success": True}

        return {"success": False}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="localhost", port=8000, reload=True)

