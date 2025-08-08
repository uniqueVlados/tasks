import uvicorn
from fastapi import FastAPI, HTTPException, Query, Body, Header
from typing import List, Optional

import logging
from schemas import Person, PersonOut, SortField, SortOrder
from config import API_HOST, API_PORT
from functions import parse_csv_string, normalize_data


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task 1-3")


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

app.middleware("http")(log_requests)


@app.post("/parse-csv/", response_model=List[PersonOut])
async def parse_csv(
    request_body: str = Body(..., media_type="text/csv"),
    sort_by: Optional[SortField] = Query(None),
    sort_order: SortOrder = Query(SortOrder.asc),
    content_type: str = Header(..., alias="Content-Type") 
):
    if not content_type.startswith("text/csv"):
        raise HTTPException(
            status_code=415,
            detail="Unsupported Media Type. Use 'text/csv'"
        )

    if not request_body.strip():
        raise HTTPException(status_code=400, detail="Empty CSV data")

    try:
        parsed = parse_csv_string(request_body)
        normalized = normalize_data(parsed)

        if sort_by:
            reverse = (sort_order == SortOrder.desc)
            key = sort_by.value
            if key in ("amount", "rating"):
                normalized.sort(key=lambda x: x[key], reverse=reverse)
            else:
                normalized.sort(key=lambda x: x[key].lower(), reverse=reverse)

        return normalized

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=True)
