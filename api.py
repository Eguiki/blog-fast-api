from urllib.request import Request

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse

import models
import schemas
from database import get_db

router = APIRouter(prefix='/api', tags=['Post'])



@router.get("/", response_model=list[schemas.PostResponse])
async def root(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    return post

@router.post("/", response_model=schemas.PostResponse)
async def post_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(
        title=post.title,
        text=post.text
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    old_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    new_post = models.Post(
        title=post.title,
        text=post.text
    )
    old_post.title = new_post.title
    old_post.text = new_post.text
    db.commit()
    db.refresh(old_post)
    return old_post


@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(post)
    db.commit()
    return {"message": "success"}