from src.main import app
from src.rss.router import api


@app.get("/health-check")
async def health_check():
    return {"status": "OK"}


app.include_router(api)
