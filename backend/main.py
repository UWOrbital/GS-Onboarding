from backend.api.endpoint import resource
from fastapi import FastAPI

app = FastAPI()
app.include_router(router=resource)
