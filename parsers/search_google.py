from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio
from typing import List, Dict
import re
import logging
import requests

logger = logging.getLogger(__name__)

class GoogleSearchParser:
    def __init__(self):
        self.base_url = "https://www.google.com/search"
        self.results_per_page = 10
        
    async def init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
    async def close(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
        
    async def search(self, query: str, site: str = None, max_pages: int = 3) -> List[Dict]:
        """
        Выполняет поиск по Google с опциональным ограничением по сайту
        """
        results = []
        
        if site:
            query = f"site:{site} {query}"
            
        try:
            await self.init_browser()
            page = await self.context.new_page()
            
            for page_num in range(max_pages):
                start = page_num * self.results_per_page
                search_url = f"{self.base_url}?q={query}&start={start}"
                
                await page.goto(search_url)
                await page.wait_for_selector("div#search")
                
                content = await page.content()
                soup = BeautifulSoup(content, "html.parser")
                
                # Парсим результаты
                for result in soup.select("div.g"):
                    try:
                        title = result.select_one("h3").text
                        link = result.select_one("a")["href"]
                        snippet = result.select_one("div.VwiC3b").text
                        
                        results.append({
                            "title": title,
                            "url": link,
                            "description": snippet
                        })
                    except Exception as e:
                        logger.error(f"Error parsing result: {e}")
                        continue
                
                await asyncio.sleep(2)  # Задержка между страницами
                
        except Exception as e:
            logger.error(f"Search error: {e}")
        finally:
            await self.close()
            
        return results

    @staticmethod
    def extract_domain(url: str) -> str:
        """Извлекает домен из URL"""
        pattern = r"https?://(?:www\.)?([^/]+)"
        match = re.search(pattern, url)
        return match.group(1) if match else url 

def get_sites(query: str) -> list:
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.google.com/search?q=site:+{query}"
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for tag in soup.select("a"):
        href = tag.get("href")
        if href and "/url?q=" in href:
            link = href.split("/url?q=")[1].split("&")[0]
            links.append(link)

    return links[:10]  # ограничим для начала 