from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import GameOfferResponse
from app.services import GameService
from app.database.connection import get_db

router = APIRouter()


@router.get("/", response_model=list[GameOfferResponse])
async def list_offers(search: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    """
    List all game offers or search by game name (fuzzy matching).
    """
    service = GameService(db)
    if search:
        return await service.search_offers(search)
    return await service.get_all_offers()
