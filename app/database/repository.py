from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from rapidfuzz import fuzz

from app.database.models import Games, GameOffers, GamePlatforms


async def get_all_offers(db: AsyncSession):
    query = select(GameOffers).options(
        joinedload(GameOffers.game), joinedload(GameOffers.platform)
    )
    result = await db.execute(query)
    return result.scalars().unique().all()


async def search_offers(db: AsyncSession, search_query: str):
    normalized_query = search_query.lower().strip()

    # Load all offers with relationships (fuzzy search needs to check everything)
    stmt = (
        select(GameOffers)
        .options(joinedload(GameOffers.game), joinedload(GameOffers.platform))
    )
    result = await db.execute(stmt)
    all_offers = result.scalars().unique().all()

    # Fuzzy scoring with multiple algorithms
    scored_offers = []
    for offer in all_offers:
        offer_title = offer.game.title.lower().strip()

        # Try multiple fuzzy algorithms and take the best score
        scores = [
            fuzz.partial_ratio(normalized_query, offer_title),      # substring match
            fuzz.token_set_ratio(normalized_query, offer_title),    # token-based (ignores word order)
            fuzz.ratio(normalized_query, offer_title),              # full string similarity
        ]
        best_score = max(scores)

        # Lower threshold for better recall
        if best_score > 60:
            scored_offers.append((best_score, offer))

    # Sort by best match first
    scored_offers.sort(key=lambda x: x[0], reverse=True)
    return [offer for score, offer in scored_offers]
