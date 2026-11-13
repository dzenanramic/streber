from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.book_router import router as book_router
from app.routers.question_router import router as question_router
from app.routers.flash_cards_router import router as flash_cards_router
from .database import init_db
from .models import FlashCard

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(book_router)
app.include_router(question_router)
app.include_router(flash_cards_router)


init_db()


@app.get("/")
def read_root():
    return {"message": "Hello World"}
