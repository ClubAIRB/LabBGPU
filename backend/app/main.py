from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, organizations, heads, admin, content, testing

app = FastAPI(
    title="ИИ-Эксперт: Диагностика руководителей",
    description="Платформа для автоматизированной диагностики компетенций руководителей образовательных организаций",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(organizations.router, prefix="/api/v1")
app.include_router(heads.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(content.router, prefix="/api/v1")
app.include_router(testing.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Добро пожаловать в платформу ИИ-Эксперт",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
