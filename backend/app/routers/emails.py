from fastapi import APIRouter, Query
from parsers.extract_emails import extract_emails_from_site

router = APIRouter()

@router.get("/emails")
async def get_emails(url: str = Query(..., description="URL сайта")):
    emails = extract_emails_from_site(url)
    return {"url": url, "emails": emails} 