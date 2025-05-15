from src.main import app


@app.get("/health-check")
async def health_check():
    return {"status": "OK"}
