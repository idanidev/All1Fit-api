from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from entrenamientos import router

app = FastAPI()

# Configuración CORS para permitir acceso desde tu frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas desde el router
app.include_router(router)
