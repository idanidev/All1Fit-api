from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from entrenamientos import router

app = FastAPI()

# CORS como antes
origins = [
    "http://localhost:4200",
    "https://app.all1fit.com",
    "https://www.app.all1fit.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prefijo /api para todas las rutas del router
app.include_router(router, prefix="/api")
