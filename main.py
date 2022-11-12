import json
import fastapi
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

app = fastapi.FastAPI(docs_url="/api/documentation", redoc_url=None)
templates = Environment(loader=FileSystemLoader('templates'))

# register static folder
app.mount("/statics", StaticFiles(directory="statics"), name="statics")


@app.api_route("/", methods=["GET"], response_class=fastapi.responses.HTMLResponse)
def root():
    return templates.get_template('index.html').render()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)