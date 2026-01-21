from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import router

app = FastAPI(title="Eneba Game Search", version="1.0.0")
app.include_router(router)


@app.get("/")
async def root():
    """Redirect to /list"""
    return RedirectResponse(url="/list")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
