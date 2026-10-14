import asyncio
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests
import aiohttp

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False
            if normalized_url not in self.visited:
                self.visited.add(normalized_url)
                return True
            return False

    async def get_html(self, url):
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            if response.status >= 400:
                raise Exception(f"Failed to fetch {url}: {response.status}")
            if "text/html" not in response.headers.get("Content-Type", ""):
                raise Exception(f"Failed to fetch {url}: Content-Type is not text/html")
            return await response.text()

    async def crawl_page(self, current_url=None):
        if self.should_stop:
            return
        
        if current_url is None:
            current_url = self.base_url

        if urlsplit(current_url).netloc != self.base_domain:
            return

        normalized_current_url = normalize_url(current_url)

        added = await self.add_page_visit(normalized_current_url)
        if not added:
            return

        async with self.semaphore:
            current_html = await self.get_html(current_url)
        print(f"crawling: {current_url}")
        extracted_data = extract_page_data(current_html, current_url)
    
        async with self.lock:
            self.page_data[normalized_current_url] = extracted_data

        if self.should_stop:
            return
        
        tasks = [
            asyncio.create_task(self.crawl_page(link))
            for link in extracted_data["outgoing_links"]
        ]

        self.all_tasks.update(tasks)
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            for task in tasks:
                self.all_tasks.discard(task)


    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url, max_pages=100, max_concurrency=5):
    async with AsyncCrawler(base_url, max_concurrency=max_concurrency, max_pages=max_pages) as crawler:
        return await crawler.crawl()

def normalize_url(url: str) -> str:
    parsed_url = urlsplit(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    return full_path.rstrip("/").lower()

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1")
    return heading.get_text(separator="", strip=False) if isinstance(heading, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    paragraph = soup.find("p")
    return paragraph.get_text(separator="", strip=False) if isinstance(paragraph, Tag) else ""

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for link in soup.find_all("a"):
        href = link.get("href")
        try:
            if href:
                urls.append(urljoin(base_url, href))
        except Exception:
            pass
    return urls

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        try:
            if src:
                images.append(urljoin(base_url, src))
        except Exception:
            pass
    return images

def extract_page_data(html: str, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }