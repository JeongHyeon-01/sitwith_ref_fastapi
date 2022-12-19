from fastapi import APIRouter, Depends, HTTPException,status, Cookie
from database import crud,databases,schema,models
from sqlalchemy.orm import Session
from typing import Union, Optional, List
from core.log import LOG
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
    items : schema.CategoryCreate,
    db : Session = Depends(databases.get_db),
):
    try:
        item = crud.create_category(db=db, item = items)
        
        return item
    
    except Exception as e:
        LOG.error(str(e))
        if "1062" in str(e):
            msg = f"Duplicate entry '{items.title}'"
        else:
            msg = str(e)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

@router.post("/product")
async def create_product(
    items : schema.ProductCreate,
    db : Session = Depends(databases.get_db)
):
    try:
        item = crud.create_product(db=db,item=items)
        return item
    except Exception as e:
        LOG.error(str(e))
        if "1062" in str(e):
            msg = f"Duplicate entry '{items.name}'"
        else:
            msg = str(e)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )