from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .logging_config import setup_logging
from .mcp.server import server as mcp_server
from .models import FlashCard
from app.routers.book_router import router as book_router
from app.routers.question_router import router as question_router
from app.routers.flash_cards_router import router as flash_cards_router

setup_logging()

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.enable_mcp:
        async with mcp_server.session_manager.run():
            yield
    else:
        yield


app = FastAPI(lifespan=lifespan)

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

if settings.enable_mcp:
    app.mount(settings.mcp_path, mcp_server.streamable_http_app(streamable_http_path="/"))


init_db()


@app.get("/")
def read_root():
    return {"message": "Hello World"}
