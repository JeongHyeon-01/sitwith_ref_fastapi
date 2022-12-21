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
    try:
        categories = crud.get_category(db=db)

        return categories
    except Exception as e:
        LOG.error(str(e))
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
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

@router.get("/product")
async def read_all_products(
    db : Session = Depends(databases.get_db)
):
    try:
        return crud.get_all_products(db=db)
    
    except Exception as e:
        LOG.error(str(e))
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
@router.post("/product")
async def create_product(
    items : schema.ProductCreate,
    productcolor : schema.ProductColorCreate,
    db : Session = Depends(databases.get_db)
):
    try:
        item = crud.create_product(db=db,item=items)
        productcolors = crud.create_product_color(db=db, item =productcolor)
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
        
@router.post("/color")
async def create_color(
    items : schema.ColorCreate,
    db : Session = Depends(databases.get_db)
):
    try:
        color = crud.create_color(db=db, item=items)
        return color
    
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

@router.get("/color")
async def read_all_colors(
    db : Session = Depends(databases.get_db)
):
    try:
        return crud.get_all_colors(db=db)
    
    except Exception as e:
        LOG.error(str(e))
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
