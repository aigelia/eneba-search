from pydantic import BaseModel


class GameOfferResponse(BaseModel):
    id: int
    title: str
    image_url: str
    platform: str
    platform_icon_url: str
    region: str
    edition: str | None = None
    likes_count: int = 0
    full_price: float
    final_price: float | None = None
    discount_percent: int | None = None
    cashback_amount: float | None = None
