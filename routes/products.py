from fastapi import APIRouter, Depends, HTTPException,status, Cookie
from database import crud,databases,schema,models
from sqlalchemy.orm import Session
from typing import Union, Optional, List

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/category")
async def read_category(
    db : Session = Depends(databases.get_db)
):
    categories = crud.get_category(db=db)
    
    return categories

@router.post("/category")
async def create_category(
    db : Session = Depends(databases.get_db),
    items : schema.CategoryCreate = Depends()
):
    try:
        item = crud.create_category(db=db, item = items)
        
        return item
    
    except Exception as e:
        if "1062" in str(e):
            msg = f"Duplicate entry '{items.title}'"
        else:
            msg = str(e)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
