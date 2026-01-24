from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import GameService
from app.database.connection import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("")
async def list_offers(
        request: Request,
        search: str | None = Query(None),
        db: AsyncSession = Depends(get_db)
):
    """
    List all game offers or search by game name (fuzzy matching).
    """
    service = GameService(db)
    if search:
        offers = await service.search_offers(search)
    else:
        offers = await service.get_all_offers()

    return templates.TemplateResponse(
        "list.html",
        {
            "request": request,
            "games": offers,
            "search_query": search or "",
            "results_count": len(offers)
        }
    )