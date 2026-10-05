from tempfile import template

from fastapi import FastAPI,Request
from pydantic import BaseModel
from starlette.responses import FileResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


class post(BaseModel):
    title: str
    text: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request,"index.html",{"request":request})

@app.get("/{post_id}", response_class=HTMLResponse)
async def root(request: Request, post_id: int):
    return templates.TemplateResponse(request,"post.html",{"id":post_id})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
