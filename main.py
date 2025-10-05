from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from entrenamientos import router as entrenamientos_router
import os

app = FastAPI(
    title="All1Fit API",
    docs_url="/docs",
    redoc_url=None,
)

# —— CORS ——
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://all1fit.com",
        "https://www.all1fit.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)


# —— Rutas base útiles ——
@app.get("/")
def root():
    return {"ok": True, "service": "All1Fit API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# —— Registrar routers de la API ——
app.include_router(entrenamientos_router)

# —— Arranque local (útil si ejecutas sin uvicorn a través de Dockerfile) ——
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        reload=True
    )
