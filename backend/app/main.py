from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import beans, master, reviews, roasters, users

app = FastAPI(
    title="BeanLog API",
    description="コーヒー豆のレビュー＆発見プラットフォーム",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(beans.router, prefix="/api/v1", tags=["Beans"])
app.include_router(reviews.router, prefix="/api/v1", tags=["Reviews"])
app.include_router(roasters.router, prefix="/api/v1", tags=["Roasters"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(master.router, prefix="/api/v1", tags=["Master"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
