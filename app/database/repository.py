from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from rapidfuzz import fuzz

from app.database.models import Games, GameOffers, GamePlatforms


async def get_all_offers(db: AsyncSession):
    query = (
        select(GameOffers, Games, GamePlatforms)
        .join(Games, GameOffers.game_id == Games.id)
        .join(GamePlatforms, GameOffers.platform_id == GamePlatforms.id)
    )
    result = await db.execute(query)
    return result.all()


async def search_offers(db: AsyncSession, search_query: str):
    normalized_query = search_query.lower().strip()

    stmt = (
        select(GameOffers)
        .join(Games)
        .options(joinedload(GameOffers.game), joinedload(GameOffers.platform))
        .where(Games.title.ilike(f"%{normalized_query}%"))
    )
    result = await db.execute(stmt)
    candidates = result.scalars().unique().all()

    scored_offers = []
    for offer in candidates:
        offer_title = offer.game.title.lower().strip()
        score = fuzz.partial_ratio(normalized_query, offer_title)

        if score > 75:
            scored_offers.append((score, offer))

    scored_offers.sort(key=lambda x: x[0], reverse=True)
    return [offer for score, offer in scored_offers]
