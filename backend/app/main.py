from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .database import engine, Base
from .routers import auth_router, tasks_router, categories_router
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(categories_router)

BASE_DIR = Path(__file__).parent.parent.parent

@app.get("/")
def serve_frontend():
    return FileResponse(str(BASE_DIR / "frontend" / "index.html"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend")), name="static")
