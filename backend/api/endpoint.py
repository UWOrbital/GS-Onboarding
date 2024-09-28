from fastapi import APIRouter

resource = APIRouter()


@resource.get("/")
async def get():
    return {"Hello": "World"}
