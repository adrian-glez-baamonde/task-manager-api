from fastapi import APIRouter, Depends
from app.schemas import CategoryCreate, CategoryResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Category


router = APIRouter()


@router.post("/categories", response_model=CategoryResponse)                                     
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):                 
    new_category = Category(                                                                    
        name=category.name
    )                                                                                   
    db.add(new_category)                                                                    
    db.commit()                                                                         
    db.refresh(new_category)                                                                

    return new_category


@router.get("/categories", response_model=list[CategoryResponse])
async def show_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()

    return categories