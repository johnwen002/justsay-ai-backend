from fastapi import APIRouter

api = APIRouter()


@api.get("/list")
async def filter():
    pass
