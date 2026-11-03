from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException
from models import Book
from pydantic import BaseModel

app_router = APIRouter(prefix="/book", tags=["book"])

class BookModel(BaseModel):
    id: Optional[int] = None  # noqa: UP045
    title: Optional[str] = None  # noqa: UP045
    author: Optional[str] = None  # noqa: UP045
    ISBN: Optional[str] = None  # noqa: UP045
    publisher: Optional[str] = None  # noqa: UP045
    publish_date: Optional[datetime] = None  # noqa: UP045
    price: Optional[Decimal] = None  # noqa: UP045
    category: Optional[str] = None  # noqa: UP045
    location: Optional[str] = None  # noqa: UP045
    stock: Optional[int] = 0  # noqa: UP045
    created_at: Optional[datetime] = None  # noqa: UP045

@app_router.get("/selectPage")
async def get(title: str = "", author: str = "", page: int = 1, pageSize: int = 5):
    book_list = Book.filter(title__contains=title, author__contains=author)
    total = await book_list.count()
    res = await book_list.offset(pageSize * (page - 1)).limit(pageSize)
    return {
        "message": res,
        "total": total
    }

@app_router.post("/", description="新增书籍")
async def create(book: BookModel):
    existing = await Book.get_or_none(title=book.title)
    if existing:
        existing.stock += 1 
        await existing.save()
        return {
            "message": "书名已存在",
            "data": existing
        }
    
    existing = await Book.get_or_none(ISBN=book.ISBN)
    if existing:
        raise HTTPException(status_code=400, detail="ISBN已存在")
    
    data = book.model_dump(exclude={"id", "created_at"}, exclude_unset=True)
    new_book = await Book.create(**data)
    return {
        "message": "新增成功",
        "data": new_book
    }
    
@app_router.put("/", description="根据id修改书籍")
async def updata(book: BookModel):
    if book.id is None:
        raise HTTPException(status_code=400, detail="缺少id参数")
    # 根据id查询
    book_obj = await Book.get_or_none(id=book.id)
    if book_obj is None:
        raise HTTPException(status_code=404, detail="未找到修改对象")
    data = book.model_dump(exclude={"id", "created_at"}, exclude_unset=True)
    await Book.filter(id=book.id).update(**data)
    return {
        "message": "修改成功",
        "data": data
    }
    
@app_router.delete("/", description="根据id删除书籍")
async def delete(id: int):
    book_obj = await Book.get_or_none(id=id)
    if book_obj is None:
        raise HTTPException(status_code=404, detail="该id对象不存在")    
    await Book.filter(id=id).delete()
    return {
        "message": "删除成功",
        "data": book_obj
    }