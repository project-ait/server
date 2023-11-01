from fastapi import APIRouter

from service.location import get_location

router = APIRouter()


@router.get("/")
async def read_ipinfo(address: str):
    return get_location(address)
