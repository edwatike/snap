from fastapi import APIRouter, BackgroundTasks
from app.services.search_service import run_search
from pydantic import BaseModel

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

@router.post("/search")
async def search_suppliers(data: SearchRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_search, data.query)
    return {"message": "Поиск запущен"} 