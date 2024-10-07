import asyncio
import re
from asyncio import Semaphore
import pandas as pd
import playwright.async_api
from playwright.async_api import async_playwright, BrowserContext
from bs4 import BeautifulSoup
from dataclasses import dataclass
import math


@dataclass
class ScrapeInfo:
    checkin_date: str
    checkout_date: str

class HotelsScraper:
    def __init__(self, browsers: int, tabs: int, cities: list, hotels_csv: str):
        self.browsers = browsers
        self.tabs = tabs
        self.cities = cities
        self.hotels_csv = hotels_csv
        self.order_params = [
            "review_score_and_price",
            "class_asc",
            "popularity",
            "class",
        ]
        self.scrape_info = ScrapeInfo(
            checkin_date="2024-09-10", checkout_date="2024-09-11"
        )

    def extract_text(self, value):
        if value is None:
            return value
        else:
            return value.text

    def process_reviews(self, html):
        soup = BeautifulSoup(html, "html.parser")
        individual_reviews = []
        review_containers = soup.find_all(attrs={"data-testid": "review-card"})
        for review in review_containers:
            review_dict = {}
            review_dict["review_date"] = self.extract_text(
                review.find(attrs={"data-testid": "review-date"})
            )
            review_dict["review_title"] = self.extract_text(
                review.find(attrs={"data-testid": "review-title"})
            )
            review_dict["positive"] = self.extract_text(
                review.find(attrs={"data-testid": "review-positive-text"})
            )
            review_dict["negative"] = self.extract_text(
                review.find(attrs={"data-testid": "review-negative-text"})
            )
            individual_reviews.append(review_dict)
        return individual_reviews

    async def get_individual_reviews(self, page, link):
        try:
            await page.goto(f"{link}#tab-reviews")
            review_locator = page.locator('[data-testid="review-card"]')
            await review_locator.first.wait_for(state="visible", timeout=10000)
            html = await page.inner_html("*", timeout=600000)
            individual_reviews = self.process_reviews(html=html)
            return individual_reviews
        except playwright.async_api.TimeoutError as e:
            print(e)

    def process_specific_hotel_info(self, html):
        hotel_dict = {}
        soup = BeautifulSoup(html, "html.parser")
        hotel_dict["title"] = self.extract_text(soup.find(class_="pp-header__title"))
        review_score = soup.find(attrs={"data-testid": "review-score-right-component"})
        if review_score is not None:
            ratings = review_score.find_all(class_="ac4a7896c7")
            if len(ratings) >= 2:
                hotel_dict["num_rating"] = self.extract_text(ratings[0])
                hotel_dict["subjective_rating"] = self.extract_text(ratings[1])
                hotel_dict["num_of_reviews"] = self.extract_text(
                    review_score.find(class_="abf093bdfe")
                )
        if not all(
            k in hotel_dict
            for k in ["num_rating", "subjective_rating", "num_of_reviews"]
        ):  # if conditions above are not met
            hotel_dict["num_rating"] = None
            hotel_dict["subjective_rating"] = None
            hotel_dict["num_of_reviews"] = None
        hotel_dict["address"] = self.extract_text(
            soup.find(attrs={"data-node_tt_id": "location_score_tooltip"})
        )
        image = soup.find(class_="bh-photo-grid").find("img")
        hotel_dict["image"] = image.get("src") if image is not None else image
        hotel_dict["amenities"] = [
            self.extract_text(span)
            for span in soup.find(class_="e50d7535fa").find_all("span")
        ]
        hotel_dict["description"] = self.extract_text(
            soup.find(attrs={"data-testid": "property-description"})
        )
        rooms = []
        room_table_rows = soup.find(class_="hprt-table")
        if room_table_rows is not None:
            room_table_rows = room_table_rows.find_all("tr")[1:]
            for row in room_table_rows:
                td = row.find_all("td")
                room_type, guest_count, price = td[:3]
                rooms.append(
                    {
                        "room_type": self.extract_text(room_type),
                        "guest_count": self.extract_text(guest_count),
                        "price": self.extract_text(price),
                    }
                )
        house_rules = {}
        house_rule_containers = soup.find(attrs={"data-testid": "HouseRules-wrapper"})
        if house_rule_containers is not None:
            house_rule_containers = house_rule_containers.find_all(class_="a26e4f0adb")
        else:
            house_rule_containers = []
        for house_rule in house_rule_containers:
            header = house_rule.find(class_="e1eebb6a1e")
            description = house_rule.find(class_="f565581f7e")
            house_rules[self.extract_text(header)] = self.extract_text(description)
        hotel_dict["house_rules"] = house_rules
        hotel_dict["rooms"] = rooms
        guest_reviews = {}
        general_review_containers = soup.find_all(
            attrs={"data-testid": "review-subscore"}
        )
        for review in general_review_containers:
            review_category, rating = review.find_all(class_="c72df67c95")
            guest_reviews[self.extract_text(review_category)] = self.extract_text(
                rating
            )
        hotel_dict["guest_reviews"] = guest_reviews
        return hotel_dict

    async def scrape_specific_hotel_info(self, sem, context, link):
        async with sem:
            hotel_dict = {}
            try:
                page = await context.new_page()
                await page.goto(link, timeout=600000)
                html = await page.inner_html("*", timeout=600000)
                hotel_dict = self.process_specific_hotel_info(html=html)
                individual_reviews = await self.get_individual_reviews(
                    page=page, link=link
                )
                hotel_dict["individual_reviews"] = individual_reviews
            except Exception as e:
                print(e)
            await page.close()
            return hotel_dict

    def scrape_listing_pages_with_different_ordering(
        self, sem, context, hotel_count: int, city
    ):
        """
        determines how many different types of params will be used
        when scraping (more hotel counts means more types of orderings
        to get more data in a specific city)
        """
        order_limit_by_hotel_count = math.ceil(hotel_count / 40)
        orders = self.order_params[
            1:order_limit_by_hotel_count  # first listing page has already been scraped
        ]
        """
            same sem as the one that was used to scrape the hotel listing containers (at the browser level)
        """
        for order in orders:
            asyncio.create_task(
                self.scrape_hotel_listing_containers_and_save_to_csv(
                    sem=sem, context=context, city=city, order=order, first_search=False
                )
            )

    def get_hotel_count(self, soup: BeautifulSoup):
        hotel_count = self.extract_text(soup.find(class_="efdb2b543b"))
        hotel_count = re.findall(r"\d+", hotel_count)
        if hotel_count:
            hotel_count = int(hotel_count[0])
        return hotel_count

    def get_hotel_links(self, soup: BeautifulSoup):
        hotels = soup.find_all(class_="c066246e13")
        links = []
        for hotel in hotels:
            try:
                link = hotel.find(attrs={"data-testid": "review-score-link"})["href"]
                links.append(link)
            except Exception as e:
                print(e)
        return links

    def process_hotel_listings(self, html):
        soup = BeautifulSoup(html, "html.parser")
        hotel_count = self.get_hotel_count(soup=soup)
        links = self.get_hotel_links(soup=soup)
        return hotel_count, links

    async def get_all_hotel_listings_specific_info(self, context, links):
        sem = asyncio.Semaphore(2)  # child tabs
        tasks = []
        for link in links:
            tasks.append(
                self.scrape_specific_hotel_info(sem=sem, context=context, link=link)
            )
        hotel_data = await asyncio.gather(*tasks)
        return hotel_data

    async def scrape_hotel_listing_containers_and_save_to_csv(
        self, sem, context, city, order, first_search: bool
    ):
        async with sem:
            try:
                page = await context.new_page()
                await page.goto(
                    f"https://www.booking.com/searchresults.html?ss={city}&checkin={self.scrape_info.checkin_date}&checkout={self.scrape_info.checkout_date}&order={order}",
                    timeout=600000,
                )
                html = await page.inner_html("*", timeout=600000)
                hotel_count, links = self.process_hotel_listings(html=html)
                if hotel_count and first_search:
                    self.scrape_listing_pages_with_different_ordering(
                        city=city, hotel_count=hotel_count, context=context, sem=sem
                    )
            except Exception as e:
                print(e)
            finally:
                await page.close()
            try:
                hotel_data = await self.get_all_hotel_listings_specific_info(
                    context=context, links=links
                )
                hotel_data = [dict(data, city=city) for data in hotel_data]
                df = pd.DataFrame(hotel_data)
                df.to_csv(self.hotels_csv, mode="a", index=False, header=False)
            except Exception as e:
                print(e)

    async def launch_browser_tasks(self, context: BrowserContext, cities):
        sem = Semaphore(self.tabs)
        tasks = []
        for city in cities:
            tasks.append(
                self.scrape_hotel_listing_containers_and_save_to_csv(
                    sem=sem,
                    context=context,
                    city=city,
                    order=self.order_params[0],
                    first_search=True,
                )
            )
        await asyncio.gather(*tasks)

    async def run(self):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(headless=False)
            contexts = [await browser.new_context() for _ in range(self.browsers)]
            chunk = len(self.cities) / len(contexts)
            tasks = [
                self.launch_browser_tasks(
                    context=context,
                    cities=self.cities[int(i * chunk) : int((i + 1) * chunk)],
                )
                for i, context in enumerate(contexts)
            ]
            await asyncio.gather(*tasks)
            unfinished_tasks = asyncio.all_tasks()
            await asyncio.gather(*unfinished_tasks)
            await browser.close()


async def main():
    cities = ["London", "Paris"]
    bookings_scraper = HotelsScraper(
        browsers=1,
        tabs=3,
        cities=cities,
        hotels_csv="hotels_uncleaned_production_copy.csv",
    )
    await bookings_scraper.run()


if __name__ == "__main__":
    asyncio.run(main())
