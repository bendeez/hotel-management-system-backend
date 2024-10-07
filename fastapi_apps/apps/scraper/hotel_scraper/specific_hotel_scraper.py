import asyncio
from playwright.async_api import async_playwright, Playwright, BrowserContext
import pandas as pd
from bs4 import BeautifulSoup
from typing import Coroutine
from urllib.parse import urlparse
import re


class HotelWebCrawler:
    def __init__(self, hotel: dict):
        self.hotel = hotel

    async def scrape_page(self, context: BrowserContext, url):
        page = await context.new_page()
        await page.goto(url)
        html = await page.inner_html("*", timeout=600000)
        await page.close()
        return html

    def find_website_url(self, html) -> str:
        soup = BeautifulSoup(html, "html.parser")
        website = soup.find(attrs={"jsname": "UWckNb"})
        website_url = website["href"]
        return website_url

    def extract_urls_from_website(self, html):
        soup = BeautifulSoup(html, "html.parser")
        extracted_url = [a.get("href") for a in soup.find_all("a")]
        urls = [url for url in extracted_url if url is not None]
        return urls

    async def task_with_semaphore(self, sem, task: Coroutine):
        async with sem:
            result = await task
            return result

    async def scrape_bulk_urls(
        self, context: BrowserContext, tabs_limit: int, urls: list[str]
    ) -> list[str]:
        sem = asyncio.Semaphore(tabs_limit)
        tasks = []
        for url in urls:
            tasks.append(
                self.task_with_semaphore(
                    sem=sem, task=self.scrape_page(context=context, url=url)
                )
            )
        html_list = await asyncio.gather(*tasks)
        return html_list

    def extract_text_from_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()

    async def run(self):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(headless=False)
            context = await browser.new_context()
            address = self.hotel["address"]
            google_suggestions_url = f"https://www.google.com/search?q={address}"
            google_suggestions_html = await self.scrape_page(
                context=context, url=google_suggestions_url
            )
            main_hotel_website_url = self.find_website_url(html=google_suggestions_html)
            main_hotel_website_html = await self.scrape_page(
                context=context, url=main_hotel_website_url
            )
            main_hotel_website_a_tag_urls = self.extract_urls_from_website(
                html=main_hotel_website_html
            )
            parsed_url = urlparse(main_hotel_website_url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            main_hotel_website_absolute_paths = list(
                set(
                    [
                        url
                        for url in main_hotel_website_a_tag_urls
                        if re.match("^/", url)
                    ]
                )
            )
            urls_to_scrape = [
                f"{base_url}{path}" for path in main_hotel_website_absolute_paths
            ]
            hotel_htmls = await self.scrape_bulk_urls(
                context=context, tabs_limit=5, urls=urls_to_scrape
            )
            hotel_texts = [
                self.extract_text_from_html(html=html) for html in hotel_htmls
            ]
            await context.close()


if __name__ == "__main__":
    df = pd.read_csv("development/data/hotels_cleaned_sample.csv")
    hotel = df.iloc[7]
    hotel_web_crawler = HotelWebCrawler(hotel=hotel)
    asyncio.run(hotel_web_crawler.run())
