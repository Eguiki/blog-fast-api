from tempfile import template

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from rich_toolkit import form
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import models
from database import engine, get_db


class post(BaseModel):
    title: str
    text: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")
models.Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return templates.TemplateResponse(request,"index.html",{"request":request,"posts":posts})

@app.get("/{post_id}", response_class=HTMLResponse)
async def root(request: Request, post_id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    return templates.TemplateResponse(request,"post.html",{"post":post})

@app.get("/newpost/", response_class=HTMLResponse)
def newpost(request: Request):
    return templates.TemplateResponse(request,"create_post.html",{"request":request})

@app.post("/newpost/", response_class=HTMLResponse)
async def newpost(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    post = models.Post()
    post.title = form["title"]
    post.text = form["text"]
    db.add(post)
    db.commit()

    return RedirectResponse('/', status_code=303)

@app.get("/delete/{post_id}", response_class=HTMLResponse)
async def delete(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == int(post_id)).first()
    db.delete(post)
    db.commit()
    return RedirectResponse('/', status_code=303)

@app.get("/update/{post_id}", response_class=HTMLResponse)
def newpost(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    return templates.TemplateResponse(request,"update_post.html",{"request":request,"post": post})

@app.post("/update/{post_id}", response_class=HTMLResponse)
async def update(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    form = await request.form()
    post.title = form["title"]
    post.text = form["text"]
    db.add(post)
    db.commit()
    return RedirectResponse('/', status_code=303)



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
