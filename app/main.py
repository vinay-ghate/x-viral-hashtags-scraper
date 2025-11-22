from fastapi import FastAPI, HTTPException
from app.models import TrendResponse
from app.services import fetch_trends

app = FastAPI(title="Trends24 Scraper API")

@app.get("/trends/{country}", response_model=TrendResponse)
async def get_trends(country: str):
    """
    Get trending topics for a specific country.
    """
    trends = fetch_trends(country)
    
    if not trends:
        raise HTTPException(status_code=404, detail=f"No trends found for country: {country}")
    
    return TrendResponse(country=country, trends=trends)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
