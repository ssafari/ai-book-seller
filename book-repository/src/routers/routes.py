import logging
from fastapi import APIRouter, Depends
from src.models.book import Book
from src.dependencies import get_book_service
from src.service.book_service import BookService


router = APIRouter(
    prefix="/api/v1/books"
)

@router.get("/{isbn}", status_code=200)
async def find_book(isbn: str, book_service: BookService = Depends(get_book_service)):
    return await book_service.get_book(isbn=isbn)


@router.post("/", status_code=201)
async def add_book(book: Book, book_service: BookService = Depends(get_book_service)):
    logging.info("====> add book, %s", book )
    return await book_service.add_book(book)

@router.put("/{isbn}", status_code=201)
async def update_book(book: Book, book_service: BookService = Depends(get_book_service)):
    return await book_service.update_book(book)


@router.delete("/{isbn}", status_code=201)
async def delete_book(isbn: str, book_service: BookService = Depends(get_book_service)):
    return await book_service.delete_book(isbn=isbn)