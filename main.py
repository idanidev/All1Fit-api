from fastapi import FastAPI
from entrenamientos import router as entrenamientos_router

app = FastAPI()

app.include_router(entrenamientos_router)
