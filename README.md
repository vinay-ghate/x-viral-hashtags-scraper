# Trends24 Scraper API

A modular FastAPI application to scrape trending topics from [trends24.in](https://trends24.in/).

## Features
- **Dynamic Country Support**: Scrape trends for any country supported by the site (e.g., `india`, `united-states`).
- **FastAPI**: High-performance, easy-to-use API.
- **Modular Design**: Clean separation of concerns.

## Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (Fast Python package installer and resolver)

## Installation & Running with `uv`

1. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   uv run python -m uvicorn app.main:app --reload --port 8000
   ```

## API Usage

**Endpoint**: `GET /trends/{country}`

**Example**:
```bash
curl http://localhost:8000/trends/india
```

**Response**:
```json
{
  "country": "india",
  "trends": [
    {
      "rank": "1",
      "text": "Example Trend",
      "link": "...",
      "duration": "N/A"
    }
  ]
}
```
