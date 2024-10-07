from enum import Enum


class TestHotelCsvFiles(Enum):
    UNCLEANED = "./apps/scraper/data/hotels_uncleaned_sample.csv"
    CLEANED = "./apps/scraper/data/hotels_cleaned_sample.csv"
