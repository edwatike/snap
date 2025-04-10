from app.parsers.search_google import get_sites
from app.parsers.extract_emails import extract_emails_from_site
from app.models.result import save_result

async def run_search(query: str):
    """
    Запускает поиск поставщиков по заданному запросу
    """
    sites = get_sites(query)
    for url in sites:
        emails = extract_emails_from_site(url)
        save_result(url, emails) 